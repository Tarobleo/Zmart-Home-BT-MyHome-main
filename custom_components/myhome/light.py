"""Support for MyHome lights."""
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_BRIGHTNESS_PCT,
    ATTR_FLASH,
    FLASH_LONG,
    FLASH_SHORT,
    ATTR_TRANSITION,
    DOMAIN as PLATFORM,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.const import (
    CONF_NAME,
    CONF_MAC,
)

from OWNd.message import (
    OWNCommand,
    OWNLightingEvent,
    OWNLightingCommand,
    MESSAGE_TYPE_MOTION,
    MESSAGE_TYPE_PIR_SENSITIVITY,
    MESSAGE_TYPE_MOTION_TIMEOUT,
)

from .const import (
    CONF_PLATFORMS,
    CONF_ENTITY,
    CONF_ENTITY_NAME,
    CONF_ICON,
    CONF_ICON_ON,
    CONF_WHO,
    CONF_WHERE,
    CONF_BUS_INTERFACE,
    CONF_MANUFACTURER,
    CONF_DEVICE_MODEL,
    CONF_DIMMABLE,
    DOMAIN,
    LOGGER,
)
from .myhome_device import MyHOMEEntity
from .gateway import MyHOMEGatewayHandler

DIMMER_MODELS = {"F418", "F430R8"}
NO_STATUS_REQUEST_DIMMER_MODELS = {"F418"}
SIMPLE_DIMMER_COMMAND_MODELS = {"F418"}


def _short_point_to_point_where(where: str) -> str:
    """Return the short OWN A/PL form used by simple dimmers."""
    if not where or not where.isdigit() or len(where) != 4:
        return where
    return f"{int(where[:2])}{int(where[2:])}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    if PLATFORM not in hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_PLATFORMS]:
        return True

    _lights = []
    _configured_lights = hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_PLATFORMS][PLATFORM]

    for _light in _configured_lights.keys():
        _light = MyHOMELight(
            hass=hass,
            device_id=_light,
            who=_configured_lights[_light][CONF_WHO],
            where=_configured_lights[_light][CONF_WHERE],
            icon=_configured_lights[_light][CONF_ICON],
            icon_on=_configured_lights[_light][CONF_ICON_ON],
            interface=_configured_lights[_light][CONF_BUS_INTERFACE] if CONF_BUS_INTERFACE in _configured_lights[_light] else None,
            name=_configured_lights[_light][CONF_NAME],
            entity_name=_configured_lights[_light][CONF_ENTITY_NAME],
            dimmable=_configured_lights[_light][CONF_DIMMABLE],
            manufacturer=_configured_lights[_light][CONF_MANUFACTURER],
            model=_configured_lights[_light][CONF_DEVICE_MODEL],
            gateway=hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_ENTITY],
        )
        _lights.append(_light)

    async_add_entities(_lights)


async def async_unload_entry(hass, config_entry):
    if PLATFORM not in hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_PLATFORMS]:
        return True

    _configured_lights = hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_PLATFORMS][PLATFORM]

    for _light in _configured_lights.keys():
        del hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_PLATFORMS][PLATFORM][_light]


def eight_bits_to_percent(value: int) -> int:
    return int(round(100 / 255 * value, 0))


def percent_to_eight_bits(value: int) -> int:
    return int(round(255 / 100 * value, 0))


class MyHOMELight(MyHOMEEntity, LightEntity):
    def __init__(
        self,
        hass,
        name: str,
        entity_name: str,
        icon: str,
        icon_on: str,
        device_id: str,
        who: str,
        where: str,
        interface: str,
        dimmable: bool,
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

        self._attr_supported_features = 0
        self._attr_supported_color_modes: set[ColorMode] = set()
        dimmable = dimmable or self._model_matches(DIMMER_MODELS)

        if dimmable:
            self._attr_supported_color_modes.add(ColorMode.BRIGHTNESS)
            self._attr_color_mode = ColorMode.BRIGHTNESS
            self._attr_supported_features |= LightEntityFeature.TRANSITION
        else:
            self._attr_supported_color_modes.add(ColorMode.ONOFF)
            self._attr_color_mode = ColorMode.ONOFF
            self._attr_supported_features |= LightEntityFeature.FLASH

        self._attr_extra_state_attributes = {
            "A": where[: len(where) // 2],
            "PL": where[len(where) // 2 :],
        }
        if self._interface is not None:
            self._attr_extra_state_attributes["Int"] = self._interface

        self._on_icon = icon_on
        self._off_icon = icon

        if self._off_icon is not None:
            self._attr_icon = self._off_icon

        self._attr_is_on = None
        self._attr_brightness = None
        self._attr_brightness_pct = None

    @property
    def _model_name(self):
        return str(self._model or "").upper()

    def _model_matches(self, models: set[str]):
        model_name = self._model_name
        return any(model in model_name for model in models)

    @property
    def _skip_status_request(self):
        return self._model_matches(NO_STATUS_REQUEST_DIMMER_MODELS)

    @property
    def _use_simple_dimmer_commands(self):
        return self._model_matches(SIMPLE_DIMMER_COMMAND_MODELS)

    @property
    def _simple_dimmer_where(self):
        where = _short_point_to_point_where(self._where)
        return f"{where}#4#{self._interface}" if self._interface is not None else where

    def _set_optimistic_state(self, is_on: bool, brightness_percent=None):
        """Reflect a local command immediately while waiting for bus feedback."""
        self._attr_is_on = is_on
        if brightness_percent is not None:
            self._attr_brightness_pct = brightness_percent
            self._attr_brightness = percent_to_eight_bits(brightness_percent)
        if self._off_icon is not None and self._on_icon is not None:
            self._attr_icon = self._on_icon if self._attr_is_on else self._off_icon
        self.async_write_ha_state()

    async def _send_simple_dimmer_level(self, brightness_percent: int):
        level = max(2, min(10, round(brightness_percent / 10)))
        command = OWNCommand.parse(f"*1*{level}*{self._simple_dimmer_where}##")
        if command is not None and command.is_valid:
            await self._gateway_handler.send(command)
            self._set_optimistic_state(True, brightness_percent)
            return
        LOGGER.error(
            "%s Could not build simple dimmer command for %s at %s%%.",
            self._gateway_handler.log_id,
            self._full_where,
            brightness_percent,
        )
        return None

    async def async_update(self):
        """Update the entity.

        Only used by the generic entity update service.
        """
        if self._skip_status_request:
            LOGGER.debug(
                "%s Requesting simple status for model %s.",
                self._gateway_handler.log_id,
                self._model,
            )
            await self._gateway_handler.send_status_request(OWNLightingCommand.status(self._simple_dimmer_where))
            return
        if ColorMode.BRIGHTNESS in self._attr_supported_color_modes:
            await self._gateway_handler.send_status_request(OWNLightingCommand.get_brightness(self._full_where))
        else:
            await self._gateway_handler.send_status_request(OWNLightingCommand.status(self._full_where))

    async def async_turn_on(self, **kwargs):
        """Turn the device on."""

        if ATTR_FLASH in kwargs and self._attr_supported_features & LightEntityFeature.FLASH:
            if kwargs[ATTR_FLASH] == FLASH_SHORT:
                return await self._gateway_handler.send(OWNLightingCommand.flash(self._full_where, 0.5))
            elif kwargs[ATTR_FLASH] == FLASH_LONG:
                return await self._gateway_handler.send(OWNLightingCommand.flash(self._full_where, 1.5))

        if ((ATTR_BRIGHTNESS in kwargs or ATTR_BRIGHTNESS_PCT in kwargs) and ColorMode.BRIGHTNESS in self._attr_supported_color_modes) or (
            ATTR_TRANSITION in kwargs and self._attr_supported_features & LightEntityFeature.TRANSITION
        ):
            if ATTR_BRIGHTNESS in kwargs or ATTR_BRIGHTNESS_PCT in kwargs:
                _percent_brightness = eight_bits_to_percent(kwargs[ATTR_BRIGHTNESS]) if ATTR_BRIGHTNESS in kwargs else None
                _percent_brightness = kwargs[ATTR_BRIGHTNESS_PCT] if ATTR_BRIGHTNESS_PCT in kwargs else _percent_brightness

                if _percent_brightness == 0:
                    return await self.async_turn_off(**kwargs)
                if self._use_simple_dimmer_commands:
                    return await self._send_simple_dimmer_level(_percent_brightness)
                else:
                    return (
                        await self._gateway_handler.send(
                            OWNLightingCommand.set_brightness(
                                self._full_where,
                                _percent_brightness,
                                int(kwargs[ATTR_TRANSITION]),
                            )
                        )
                        if ATTR_TRANSITION in kwargs
                        else await self._gateway_handler.send(OWNLightingCommand.set_brightness(self._full_where, _percent_brightness))
                    )
            else:
                if self._use_simple_dimmer_commands:
                    await self._gateway_handler.send(OWNLightingCommand.switch_on(self._simple_dimmer_where))
                    self._set_optimistic_state(True)
                    return
                return await self._gateway_handler.send(OWNLightingCommand.switch_on(self._full_where, int(kwargs[ATTR_TRANSITION])))
        else:
            if self._use_simple_dimmer_commands:
                await self._gateway_handler.send(OWNLightingCommand.switch_on(self._simple_dimmer_where))
                self._set_optimistic_state(True)
                return
            await self._gateway_handler.send(OWNLightingCommand.switch_on(self._full_where))
            if ColorMode.BRIGHTNESS in self._attr_supported_color_modes:
                await self.async_update()

    async def async_turn_off(self, **kwargs):
        """Turn the device off."""

        if ATTR_TRANSITION in kwargs and self._attr_supported_features & LightEntityFeature.TRANSITION:
            if self._use_simple_dimmer_commands:
                await self._gateway_handler.send(OWNLightingCommand.switch_off(self._simple_dimmer_where))
                self._set_optimistic_state(False, 0)
                return
            return await self._gateway_handler.send(OWNLightingCommand.switch_off(self._full_where, int(kwargs[ATTR_TRANSITION])))

        if ATTR_FLASH in kwargs and self._attr_supported_features & LightEntityFeature.FLASH:
            if kwargs[ATTR_FLASH] == FLASH_SHORT:
                return await self._gateway_handler.send(OWNLightingCommand.flash(self._full_where, 0.5))
            elif kwargs[ATTR_FLASH] == FLASH_LONG:
                return await self._gateway_handler.send(OWNLightingCommand.flash(self._full_where, 1.5))

        if self._use_simple_dimmer_commands:
            await self._gateway_handler.send(OWNLightingCommand.switch_off(self._simple_dimmer_where))
            self._set_optimistic_state(False, 0)
            return
        await self._gateway_handler.send(OWNLightingCommand.switch_off(self._full_where))

    def handle_event(self, message: OWNLightingEvent):
        """Handle an event message."""
        if message.message_type in [
            MESSAGE_TYPE_MOTION,
            MESSAGE_TYPE_MOTION_TIMEOUT,
            MESSAGE_TYPE_PIR_SENSITIVITY,
        ]:
            return True

        LOGGER.info(
            "%s %s",
            self._gateway_handler.log_id,
            message.human_readable_log,
        )
        self._attr_is_on = message.is_on
        if ColorMode.BRIGHTNESS in self._attr_supported_color_modes and message.brightness is not None:
            self._attr_brightness_pct = message.brightness
            self._attr_brightness = percent_to_eight_bits(message.brightness)
        elif ColorMode.BRIGHTNESS in self._attr_supported_color_modes and message.brightness_preset is not None:
            brightness_percent = min(100, int(message.brightness_preset) * 10)
            self._attr_brightness_pct = brightness_percent
            self._attr_brightness = percent_to_eight_bits(brightness_percent)

        if self._off_icon is not None and self._on_icon is not None:
            self._attr_icon = self._on_icon if self._attr_is_on else self._off_icon

        self.async_schedule_update_ha_state()
