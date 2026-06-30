"""Support for MyHome covers."""
import asyncio
import time

from homeassistant.components.cover import (
    ATTR_POSITION,
    DOMAIN as PLATFORM,
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)

from homeassistant.const import (
    CONF_NAME,
    CONF_MAC,
)

from OWNd.message import (
    OWNCommand,
    OWNAutomationEvent,
    OWNAutomationCommand,
)

from .const import (
    CONF_PLATFORMS,
    CONF_ENTITY,
    CONF_ENTITY_NAME,
    CONF_WHO,
    CONF_WHERE,
    CONF_BUS_INTERFACE,
    CONF_MANUFACTURER,
    CONF_DEVICE_MODEL,
    CONF_ADVANCED_SHUTTER,
    DOMAIN,
    LOGGER,
)
from .myhome_device import MyHOMEEntity
from .gateway import MyHOMEGatewayHandler

SHORT_ADDRESS_COVER_MODELS = {"F411/4"}
SIMULATED_TRAVEL_TIME = 30


def _short_point_to_point_where(where: str) -> str:
    """Return the short OWN A/PL form used by some automation modules."""
    if not where or not where.isdigit() or len(where) != 4:
        return where
    return f"{int(where[:2])}{int(where[2:])}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    if PLATFORM not in hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_PLATFORMS]:
        return True

    _covers = []
    _configured_covers = hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_PLATFORMS][PLATFORM]

    for _cover in _configured_covers.keys():
        _cover = MyHOMECover(
            hass=hass,
            device_id=_cover,
            who=_configured_covers[_cover][CONF_WHO],
            where=_configured_covers[_cover][CONF_WHERE],
            interface=_configured_covers[_cover][CONF_BUS_INTERFACE] if CONF_BUS_INTERFACE in _configured_covers[_cover] else None,
            name=_configured_covers[_cover][CONF_NAME],
            entity_name=_configured_covers[_cover][CONF_ENTITY_NAME],
            advanced=_configured_covers[_cover][CONF_ADVANCED_SHUTTER],
            manufacturer=_configured_covers[_cover][CONF_MANUFACTURER],
            model=_configured_covers[_cover][CONF_DEVICE_MODEL],
            gateway=hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_ENTITY],
        )
        _covers.append(_cover)

    async_add_entities(_covers)


async def async_unload_entry(hass, config_entry):  # pylint: disable=unused-argument
    if PLATFORM not in hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_PLATFORMS]:
        return True

    _configured_covers = hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_PLATFORMS][PLATFORM]

    for _cover in _configured_covers.keys():
        del hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_PLATFORMS][PLATFORM][_cover]


class MyHOMECover(MyHOMEEntity, CoverEntity):
    device_class = CoverDeviceClass.SHUTTER

    def __init__(
        self,
        hass,
        name: str,
        entity_name: str,
        device_id: str,
        who: str,
        where: str,
        interface: str,
        advanced: bool,
        manufacturer: str,
        model: str,
        gateway: MyHOMEGatewayHandler,
    ):
        super().__init__(
            hass=hass,
            name=name,
            platform=PLATFORM,
            device_id=device_id,
            who=who,
            where=where,
            manufacturer=manufacturer,
            model=model,
            gateway=gateway,
        )

        self._attr_name = entity_name

        self._interface = interface
        self._full_where = f"{self._where}#4#{self._interface}" if self._interface is not None else self._where

        self._attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP
        self._use_simulated_position = any(model in str(model or "").upper() for model in SHORT_ADDRESS_COVER_MODELS)
        if advanced or self._use_simulated_position:
            self._attr_supported_features |= CoverEntityFeature.SET_POSITION
        self._gateway_handler = gateway

        self._attr_extra_state_attributes = {
            "A": where[: len(where) // 2],
            "PL": where[len(where) // 2 :],
        }
        if self._interface is not None:
            self._attr_extra_state_attributes["Int"] = self._interface
        if self._use_simulated_position:
            self._attr_extra_state_attributes["simulated_position"] = True

        self._attr_current_cover_position = 0 if self._use_simulated_position else None
        self._attr_is_opening = None
        self._attr_is_closing = None
        self._attr_is_closed = True if self._use_simulated_position else None
        self._simulated_target_position = None
        self._simulated_start_position = None
        self._simulated_started_at = None
        self._simulated_travel_duration = None
        self._simulated_movement_task = None

    @property
    def _model_name(self):
        return str(self._model or "").upper()

    def _model_matches(self, models: set[str]):
        model_name = self._model_name
        return any(model in model_name for model in models)

    @property
    def _use_short_address_commands(self):
        return self._model_matches(SHORT_ADDRESS_COVER_MODELS)

    @property
    def _command_where(self):
        if not self._use_short_address_commands:
            return self._full_where
        where = _short_point_to_point_where(self._where)
        return f"{where}#4#{self._interface}" if self._interface is not None else where

    async def _send_automation_command(self, action: int):
        command = OWNCommand.parse(f"*2*{action}*{self._command_where}##")
        if command is not None and command.is_valid:
            return await self._gateway_handler.send(command)
        LOGGER.error(
            "%s Could not build automation command *2*%s*%s##.",
            self._gateway_handler.log_id,
            action,
            self._command_where,
        )
        return None

    def _cancel_simulated_movement(self):
        if self._simulated_movement_task is not None:
            self._simulated_movement_task.cancel()
            self._simulated_movement_task = None

    def _estimate_simulated_position(self):
        if (
            self._simulated_started_at is None
            or self._simulated_start_position is None
            or self._simulated_target_position is None
            or not self._simulated_travel_duration
        ):
            return self._attr_current_cover_position

        elapsed = min(time.monotonic() - self._simulated_started_at, self._simulated_travel_duration)
        progress = elapsed / self._simulated_travel_duration
        delta = self._simulated_target_position - self._simulated_start_position
        return round(self._simulated_start_position + (delta * progress))

    def _set_simulated_position(self, position: int):
        self._attr_current_cover_position = max(0, min(100, int(position)))
        self._attr_is_closed = self._attr_current_cover_position == 0

    async def _finish_simulated_movement(self, position: int, stop_at_target=False):
        try:
            await asyncio.sleep(self._simulated_travel_duration)
            if stop_at_target:
                await self._send_automation_command(0)
            self._set_simulated_position(position)
            self._attr_is_opening = False
            self._attr_is_closing = False
            self._simulated_movement_task = None
            self.async_write_ha_state()
        except asyncio.CancelledError:
            pass

    async def _move_to_simulated_position(self, position: int, stop_at_target=False):
        position = max(0, min(100, int(position)))
        current_position = self._attr_current_cover_position
        if current_position is None:
            current_position = 0 if position > 0 else 100
        if position == current_position:
            self._set_simulated_position(position)
            self._attr_is_opening = False
            self._attr_is_closing = False
            self.async_write_ha_state()
            return

        self._cancel_simulated_movement()
        opening = position > current_position
        await self._send_automation_command(1 if opening else 2)
        self._simulated_start_position = current_position
        self._simulated_target_position = position
        self._simulated_started_at = time.monotonic()
        self._simulated_travel_duration = max(0.5, abs(position - current_position) / 100 * SIMULATED_TRAVEL_TIME)
        self._attr_is_opening = opening
        self._attr_is_closing = not opening
        self._attr_is_closed = False
        self.async_write_ha_state()
        self._simulated_movement_task = self._hass.async_create_task(
            self._finish_simulated_movement(position, stop_at_target)
        )

    async def async_update(self):
        """Update the entity.

        Only used by the generic entity update service.
        """
        await self._gateway_handler.send_status_request(OWNAutomationCommand.status(self._command_where))

    async def async_open_cover(self, **kwargs):  # pylint: disable=unused-argument
        """Open the cover."""
        if self._use_simulated_position:
            await self._move_to_simulated_position(100)
            return
        await self._send_automation_command(1)

    async def async_close_cover(self, **kwargs):  # pylint: disable=unused-argument
        """Close cover."""
        if self._use_simulated_position:
            await self._move_to_simulated_position(0)
            return
        await self._send_automation_command(2)

    async def async_set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        if ATTR_POSITION in kwargs:
            position = kwargs[ATTR_POSITION]
            if self._use_simulated_position:
                await self._move_to_simulated_position(position, True)
                return
            await self._gateway_handler.send(OWNAutomationCommand.set_shutter_level(self._command_where, position))

    async def async_stop_cover(self, **kwargs):  # pylint: disable=unused-argument
        """Stop the cover."""
        if self._use_simulated_position:
            position = self._estimate_simulated_position()
            self._cancel_simulated_movement()
            await self._send_automation_command(0)
            if position is not None:
                self._set_simulated_position(position)
            self._attr_is_opening = False
            self._attr_is_closing = False
            self.async_write_ha_state()
            return
        await self._send_automation_command(0)

    def handle_event(self, message: OWNAutomationEvent):
        """Handle an event message."""
        LOGGER.info(
            "%s %s",
            self._gateway_handler.log_id,
            message.human_readable_log,
        )
        self._attr_is_opening = message.is_opening
        self._attr_is_closing = message.is_closing
        if message.is_closed is not None:
            self._attr_is_closed = message.is_closed
        if message.current_position is not None:
            self._attr_current_cover_position = message.current_position

        self.async_schedule_update_ha_state()
