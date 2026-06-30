"""Code to handle a MyHome Gateway."""
import asyncio
from typing import Dict, List
from datetime import datetime
from homeassistant.const import (
    CONF_ENTITIES,
    CONF_HOST,
    CONF_PORT,
    CONF_PASSWORD,
    CONF_NAME,
    CONF_MAC,
    CONF_FRIENDLY_NAME,
)
from homeassistant.components.light import DOMAIN as LIGHT
from homeassistant.components.switch import (
    SwitchDeviceClass,
    DOMAIN as SWITCH,
)
from homeassistant.components.button import DOMAIN as BUTTON
from homeassistant.components.cover import DOMAIN as COVER
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    DOMAIN as BINARY_SENSOR,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    DOMAIN as SENSOR,
)
from homeassistant.components.climate import DOMAIN as CLIMATE

from OWNd.connection import OWNSession, OWNEventSession, OWNCommandSession, OWNGateway
from OWNd.message import (
    OWNMessage,
    OWNLightingEvent,
    OWNLightingCommand,
    OWNEnergyEvent,
    OWNAutomationEvent,
    OWNDryContactEvent,
    OWNAuxEvent,
    OWNHeatingEvent,
    OWNHeatingCommand,
    OWNCENPlusEvent,
    OWNCENEvent,
    OWNGatewayEvent,
    OWNGatewayCommand,
    OWNCommand,
)

from .const import (
    CONF_PLATFORMS,
    CONF_FIRMWARE,
    CONF_SSDP_LOCATION,
    CONF_SSDP_ST,
    CONF_DEVICE_TYPE,
    CONF_MANUFACTURER,
    CONF_MANUFACTURER_URL,
    CONF_UDN,
    CONF_SHORT_PRESS,
    CONF_SHORT_RELEASE,
    CONF_LONG_PRESS,
    CONF_LONG_RELEASE,
    DOMAIN,
    LOGGER,
)
from .myhome_device import MyHOMEEntity
from .button import (
    DisableCommandButtonEntity,
    EnableCommandButtonEntity,
)


EVENT_SESSION_IDLE_TIMEOUT = 300
RECONNECT_DELAY = 10


def _human_readable_log(message) -> str:
    """Return a safe human readable log string for OWNd messages."""
    log_text = getattr(message, "human_readable_log", None)
    if callable(log_text):
        try:
            return str(log_text())
        except TypeError:
            return str(message)
    return str(log_text if log_text is not None else message)


def _socket_telegram(message) -> str:
    """Return the most complete socket telegram available for a message."""
    for attr in (
        "telegram",
        "raw_telegram",
        "raw_message",
        "raw",
        "message",
        "frame",
        "data",
    ):
        value = getattr(message, attr, None)
        if value is None:
            continue
        if callable(value):
            try:
                value = value()
            except TypeError:
                continue
        if isinstance(value, bytes):
            value = value.decode(errors="replace")
        value = str(value)
        if value:
            return value
    return str(message)


def _normalize_short_lighting_where(where: str) -> str:
    """Normalize short lighting addresses like 43 or 415 to 0403 or 0415."""
    where = str(where or "")
    if not where.isdigit():
        return where
    if len(where) == 2:
        return f"0{where[0]}0{where[1]}"
    if len(where) == 3:
        return f"0{where[0]}{where[1:]}"
    return where


def _lighting_entity_ids(message) -> list[str]:
    """Return possible entity ids for a lighting message."""
    entity_ids = [message.entity]
    normalized_where = _normalize_short_lighting_where(getattr(message, "where", ""))
    normalized_entity = f"{message.who}-{normalized_where}"
    if normalized_entity not in entity_ids:
        entity_ids.append(normalized_entity)
    return entity_ids


def _normalize_short_point_to_point_where(where: str) -> str:
    """Normalize short automation addresses like 21 or 313 to 0201 or 0313."""
    where = str(where or "")
    if not where.isdigit():
        return where
    if len(where) == 2:
        return f"0{where[0]}0{where[1]}"
    if len(where) == 3:
        return f"0{where[0]}{where[1:]}"
    return where


def _automation_entity_ids(message) -> list[str]:
    """Return possible entity ids for an automation message."""
    entity_ids = [message.entity]
    normalized_where = _normalize_short_point_to_point_where(getattr(message, "where", ""))
    normalized_entity = f"{message.who}-{normalized_where}"
    if normalized_entity not in entity_ids:
        entity_ids.append(normalized_entity)
    return entity_ids


def _json_safe(value):
    """Return a JSON-safe representation for monitor diagnostics."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    return str(value)


def _message_details(message) -> dict:
    """Collect additional information exposed by OWNd message objects."""
    details = {
        "class": type(message).__name__,
        "repr": repr(message),
        "text": str(message),
        "human_readable": _human_readable_log(message),
    }
    event_content = getattr(message, "event_content", None)
    if event_content:
        details["event_content"] = _json_safe(event_content)

    attributes = {}
    for attr in dir(message):
        if attr.startswith("_") or attr in ("event_content", "human_readable_log"):
            continue
        try:
            value = getattr(message, attr)
        except Exception:  # noqa: BLE001
            continue
        if callable(value):
            continue
        attributes[attr] = _json_safe(value)
    if attributes:
        details["attributes"] = attributes
    return details


def _append_bus_monitor_entry(hass, gateway: str, message, direction: str) -> None:
    """Store a bounded bus monitor entry."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    telegram = _socket_telegram(message)
    if direction == "in":
        dedupe_key = (gateway, direction, telegram)
        now = datetime.now().timestamp()
        seen = domain_data.setdefault("_bus_monitor_seen", {})
        if now - seen.get(dedupe_key, 0) < 10:
            return
        seen[dedupe_key] = now
        if len(seen) > 1000:
            domain_data["_bus_monitor_seen"] = {
                key: value
                for key, value in seen.items()
                if now - value < 60
            }

    store = domain_data.setdefault("_bus_monitor", [])
    store.append(
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "gateway": gateway,
            "direction": direction,
            "telegram": telegram,
            "raw": str(message),
            "details": _message_details(message),
        }
    )
    if len(store) > 500:
        del store[:-500]


class MyHOMEGatewayHandler:
    """Manages a single MyHOME Gateway."""

    def __init__(self, hass, config_entry, generate_events=False):
        build_info = {
            "address": config_entry.data[CONF_HOST],
            "port": config_entry.data[CONF_PORT],
            "password": config_entry.data[CONF_PASSWORD],
            "ssdp_location": config_entry.data[CONF_SSDP_LOCATION],
            "ssdp_st": config_entry.data[CONF_SSDP_ST],
            "deviceType": config_entry.data[CONF_DEVICE_TYPE],
            "friendlyName": config_entry.data[CONF_FRIENDLY_NAME],
            "manufacturer": config_entry.data[CONF_MANUFACTURER],
            "manufacturerURL": config_entry.data[CONF_MANUFACTURER_URL],
            "modelName": config_entry.data[CONF_NAME],
            "modelNumber": config_entry.data[CONF_FIRMWARE],
            "serialNumber": config_entry.data[CONF_MAC],
            "UDN": config_entry.data[CONF_UDN],
        }
        self.hass = hass
        self.config_entry = config_entry
        self.generate_events = generate_events
        self.gateway = OWNGateway(build_info)
        self._terminate_listener = False
        self._terminate_sender = False
        self.is_connected = False
        self.listening_worker: asyncio.tasks.Task = None
        self.sending_workers: List[asyncio.tasks.Task] = []
        self.send_buffer = asyncio.Queue()

    @property
    def mac(self) -> str:
        return self.gateway.serial

    @property
    def unique_id(self) -> str:
        return self.mac

    @property
    def log_id(self) -> str:
        return self.gateway.log_id

    @property
    def manufacturer(self) -> str:
        return self.gateway.manufacturer

    @property
    def name(self) -> str:
        return f"{self.gateway.model_name} Gateway"

    @property
    def model(self) -> str:
        return self.gateway.model_name

    @property
    def firmware(self) -> str:
        return self.gateway.firmware

    async def test(self) -> Dict:
        return await OWNSession(gateway=self.gateway, logger=LOGGER).test_connection()

    async def listening_loop(self):
        self._terminate_listener = False

        LOGGER.debug("%s Creating listening worker.", self.log_id)

        try:
            while not self._terminate_listener:
                _event_session = OWNEventSession(gateway=self.gateway, logger=LOGGER)
                try:
                    await _event_session.connect()
                    self.is_connected = True
                    LOGGER.info("%s Event listener connected.", self.log_id)

                    while not self._terminate_listener:
                        try:
                            message = await asyncio.wait_for(
                                _event_session.get_next(),
                                timeout=EVENT_SESSION_IDLE_TIMEOUT,
                            )
                        except asyncio.TimeoutError:
                            LOGGER.warning(
                                "%s Event listener idle for %ss, reconnecting.",
                                self.log_id,
                                EVENT_SESSION_IDLE_TIMEOUT,
                            )
                            break

                        await self._handle_message(message)
                except asyncio.CancelledError:
                    LOGGER.debug("%s Listening worker cancelled.", self.log_id)
                    raise
                except Exception as err:  # noqa: BLE001
                    LOGGER.warning(
                        "%s Event listener stopped unexpectedly, reconnecting in %ss: %s",
                        self.log_id,
                        RECONNECT_DELAY,
                        err,
                    )
                finally:
                    await _event_session.close()
                    self.is_connected = False

                if not self._terminate_listener:
                    await asyncio.sleep(RECONNECT_DELAY)
        finally:
            LOGGER.debug("%s Destroying listening worker.", self.log_id)

    async def _handle_message(self, message):
        LOGGER.debug("%s Message received: `%s`", self.log_id, message)
        try:
            _append_bus_monitor_entry(self.hass, self.log_id, message, "in")
        except Exception:  # noqa: BLE001
            pass
        if self.generate_events:
            if isinstance(message, OWNMessage):
                _event_content = {"gateway": str(self.gateway.host)}
                _event_content.update(message.event_content)
                self.hass.bus.async_fire("myhome_message_event", _event_content)
            else:
                self.hass.bus.async_fire("myhome_message_event", {"gateway": str(self.gateway.host), "message": str(message)})

        if not isinstance(message, OWNMessage):
            LOGGER.warning(
                "%s Data received is not a message: `%s`",
                self.log_id,
                message,
            )
        elif isinstance(message, OWNEnergyEvent):
            if SENSOR in self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS] and message.entity in self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS][SENSOR]:
                for _entity in self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS][SENSOR][message.entity][CONF_ENTITIES]:
                    if isinstance(
                        self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS][SENSOR][message.entity][CONF_ENTITIES][_entity],
                        MyHOMEEntity,
                    ):
                        self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS][SENSOR][message.entity][CONF_ENTITIES][_entity].handle_event(message)
            else:
                return
        elif (
            isinstance(message, OWNLightingEvent)
            or isinstance(message, OWNAutomationEvent)
            or isinstance(message, OWNDryContactEvent)
            or isinstance(message, OWNAuxEvent)
            or isinstance(message, OWNHeatingEvent)
        ):
            if not message.is_translation:
                is_event = False
                if isinstance(message, OWNLightingEvent):
                    if message.is_general:
                        is_event = True
                        event = "on" if message.is_on else "off"
                        self.hass.bus.async_fire(
                            "myhome_general_light_event",
                            {"message": str(message), "event": event},
                        )
                    elif message.is_area:
                        is_event = True
                        event = "on" if message.is_on else "off"
                        self.hass.bus.async_fire(
                            "myhome_area_light_event",
                            {
                                "message": str(message),
                                "area": message.area,
                                "event": event,
                            },
                        )
                    elif message.is_group:
                        is_event = True
                        event = "on" if message.is_on else "off"
                        self.hass.bus.async_fire(
                            "myhome_group_light_event",
                            {
                                "message": str(message),
                                "group": message.group,
                                "event": event,
                            },
                        )
                elif isinstance(message, OWNAutomationEvent):
                    if message.is_general:
                        is_event = True
                        if message.is_opening and not message.is_closing:
                            event = "open"
                        elif message.is_closing and not message.is_opening:
                            event = "close"
                        else:
                            event = "stop"
                        self.hass.bus.async_fire(
                            "myhome_general_automation_event",
                            {"message": str(message), "event": event},
                        )
                    elif message.is_area:
                        is_event = True
                        if message.is_opening and not message.is_closing:
                            event = "open"
                        elif message.is_closing and not message.is_opening:
                            event = "close"
                        else:
                            event = "stop"
                        self.hass.bus.async_fire(
                            "myhome_area_automation_event",
                            {
                                "message": str(message),
                                "area": message.area,
                                "event": event,
                            },
                        )
                    elif message.is_group:
                        is_event = True
                        if message.is_opening and not message.is_closing:
                            event = "open"
                        elif message.is_closing and not message.is_opening:
                            event = "close"
                        else:
                            event = "stop"
                        self.hass.bus.async_fire(
                            "myhome_group_automation_event",
                            {
                                "message": str(message),
                                "group": message.group,
                                "event": event,
                            },
                        )
                if not is_event:
                    if isinstance(message, OWNLightingEvent) and message.brightness_preset:
                        entity = None
                        for entity_id in _lighting_entity_ids(message):
                            if entity_id in self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS][LIGHT]:
                                entity = self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS][LIGHT][entity_id][CONF_ENTITIES][LIGHT]
                                break
                        if isinstance(entity, MyHOMEEntity):
                            if getattr(entity, "_skip_status_request", False):
                                entity.handle_event(message)
                            else:
                                await entity.async_update()
                    else:
                        for _platform in self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS]:
                            if isinstance(message, OWNLightingEvent):
                                message_entities = _lighting_entity_ids(message)
                            elif isinstance(message, OWNAutomationEvent):
                                message_entities = _automation_entity_ids(message)
                            else:
                                message_entities = [message.entity]
                            for message_entity in message_entities:
                                if _platform == BUTTON or message_entity not in self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS][_platform]:
                                    continue
                                for _entity in self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS][_platform][message_entity][CONF_ENTITIES]:
                                    if (
                                        isinstance(
                                            self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS][_platform][message_entity][CONF_ENTITIES][_entity],
                                            MyHOMEEntity,
                                        )
                                        and not isinstance(
                                            self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS][_platform][message_entity][CONF_ENTITIES][_entity],
                                            DisableCommandButtonEntity,
                                        )
                                        and not isinstance(
                                            self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS][_platform][message_entity][CONF_ENTITIES][_entity],
                                            EnableCommandButtonEntity,
                                        )
                                    ):
                                        self.hass.data[DOMAIN][self.mac][CONF_PLATFORMS][_platform][message_entity][CONF_ENTITIES][_entity].handle_event(message)
                                break

            else:
                LOGGER.debug(
                    "%s Ignoring translation message `%s`",
                    self.log_id,
                    message,
                )
        elif isinstance(message, OWNHeatingCommand) and message.dimension is not None and message.dimension == 14:
            where = message.where[1:] if message.where.startswith("#") else message.where
            LOGGER.debug(
                "%s Received heating command, sending query to zone %s",
                self.log_id,
                where,
            )
            await self.send_status_request(OWNHeatingCommand.status(where))
        elif isinstance(message, OWNCENPlusEvent):
            event = None
            if message.is_short_pressed:
                event = CONF_SHORT_PRESS
            elif message.is_held or message.is_still_held:
                event = CONF_LONG_PRESS
            elif message.is_released:
                event = CONF_LONG_RELEASE
            else:
                event = None
            self.hass.bus.async_fire(
                "myhome_cenplus_event",
                {
                    "object": int(message.object),
                    "pushbutton": int(message.push_button),
                    "event": event,
                },
            )
            LOGGER.info(
                "%s %s",
                self.log_id,
                _human_readable_log(message),
            )
        elif isinstance(message, OWNCENEvent):
            event = None
            if message.is_pressed:
                event = CONF_SHORT_PRESS
            elif message.is_released_after_short_press:
                event = CONF_SHORT_RELEASE
            elif message.is_held:
                event = CONF_LONG_PRESS
            elif message.is_released_after_long_press:
                event = CONF_LONG_RELEASE
            else:
                event = None
            self.hass.bus.async_fire(
                "myhome_cen_event",
                {
                    "object": int(message.object),
                    "pushbutton": int(message.push_button),
                    "event": event,
                },
            )
            LOGGER.info(
                "%s %s",
                self.log_id,
                _human_readable_log(message),
            )
        elif isinstance(message, OWNGatewayEvent) or isinstance(message, OWNGatewayCommand):
            LOGGER.info(
                "%s %s",
                self.log_id,
                _human_readable_log(message),
            )
        else:
            LOGGER.info(
                "%s Unsupported message type: `%s`",
                self.log_id,
                message,
            )

    async def sending_loop(self, worker_id: int):
        self._terminate_sender = False

        LOGGER.debug(
            "%s Creating sending worker %s",
            self.log_id,
            worker_id,
        )

        try:
            while not self._terminate_sender:
                _command_session = OWNCommandSession(gateway=self.gateway, logger=LOGGER)
                try:
                    await _command_session.connect()
                    LOGGER.info(
                        "%s Sending worker %s connected.",
                        self.log_id,
                        worker_id,
                    )

                    while not self._terminate_sender:
                        task = await self.send_buffer.get()
                        LOGGER.debug(
                            "%s Message `%s` was successfully unqueued by worker %s.",
                            self.log_id,
                            task["message"],
                            worker_id,
                        )
                        try:
                            await _command_session.send(
                                message=task["message"],
                                is_status_request=task["is_status_request"],
                            )
                        except Exception:  # noqa: BLE001
                            await self.send_buffer.put(task)
                            self.send_buffer.task_done()
                            raise
                        self.send_buffer.task_done()
                except asyncio.CancelledError:
                    LOGGER.debug(
                        "%s Sending worker %s cancelled.",
                        self.log_id,
                        worker_id,
                    )
                    raise
                except Exception as err:  # noqa: BLE001
                    LOGGER.warning(
                        "%s Sending worker %s stopped unexpectedly, reconnecting in %ss: %s",
                        self.log_id,
                        worker_id,
                        RECONNECT_DELAY,
                        err,
                    )
                finally:
                    await _command_session.close()

                if not self._terminate_sender:
                    await asyncio.sleep(RECONNECT_DELAY)
        except asyncio.CancelledError:
            LOGGER.debug(
                "%s Sending worker %s cancelled.",
                self.log_id,
                worker_id,
            )
            raise
        finally:
            LOGGER.debug(
                "%s Destroying sending worker %s",
                self.log_id,
                worker_id,
            )

    async def close_listener(self) -> bool:
        LOGGER.info("%s Closing event listener", self.log_id)
        self._terminate_sender = True
        self._terminate_listener = True

        workers = [
            worker
            for worker in [self.listening_worker, *self.sending_workers]
            if worker is not None and not worker.done()
        ]
        for worker in workers:
            worker.cancel()
        if workers:
            await asyncio.gather(*workers, return_exceptions=True)

        return True

    async def send(self, message: OWNCommand):
        await self.send_buffer.put({"message": message, "is_status_request": False})
        _append_bus_monitor_entry(self.hass, self.log_id, message, "out")
        LOGGER.debug(
            "%s Message `%s` was successfully queued.",
            self.log_id,
            message,
        )

    async def send_status_request(self, message: OWNCommand):
        await self.send_buffer.put({"message": message, "is_status_request": True})
        _append_bus_monitor_entry(self.hass, self.log_id, message, "status")
        LOGGER.debug(
            "%s Message `%s` was successfully queued.",
            self.log_id,
            message,
        )
