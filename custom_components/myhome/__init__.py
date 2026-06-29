""" MyHOME integration. """

import copy
import aiofiles
import re
import yaml

from OWNd.message import OWNCommand, OWNGatewayCommand
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.update import DOMAIN as UPDATE
from .panel import async_register_panel
from homeassistant.config_entries import SOURCE_REAUTH, ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr, entity_registry as er, config_validation as cv
from homeassistant.const import CONF_MAC
from .bus_monitor import MyHomeBusMonitorView, MyHomeBusMonitorDataView, MyHomeBusMonitorClearView
from .const import (
    ATTR_GATEWAY,
    ATTR_MESSAGE,
    CONF_ADVANCED_SHUTTER,
    CONF_BUS_INTERFACE,
    CONF_DEVICE_CLASS,
    CONF_DEVICE_MODEL,
    CONF_DIMMABLE,
    CONF_ENTITY_NAME,
    CONF_PLATFORMS,
    CONF_ENTITY,
    CONF_ENTITIES,
    CONF_CENTRAL,
    CONF_COOLING_SUPPORT,
    CONF_FAN_SUPPORT,
    CONF_HEATING_SUPPORT,
    CONF_STANDALONE,
    CONF_WHERE,
    CONF_WORKER_COUNT,
    CONF_FILE_PATH,
    CONF_GENERATE_EVENTS,
    CONF_ZONE,
    DOMAIN,
    LOGGER,
)
from .validate import config_schema, format_mac
from .gateway import MyHOMEGatewayHandler

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
PLATFORMS = ["light", "switch", "cover", "climate", "binary_sensor", "sensor", "update"]
CREATE_ENTITY_PLATFORMS = {"light", "switch", "cover", "climate", "binary_sensor", "sensor"}
DEVICE_MODEL_OPTIONS = {
    "067219",
    "BMSW1005",
    "F411/4",
    "F417U2",
    "F418",
    "F422",
    "F430R8",
    "H4652/2",
    "HC/HS/HD4659",
    "LN4652",
    "LN4691",
}
DEFAULT_DEVICE_MODEL_BY_PLATFORM = {
    "light": {False: "F417U2", True: "F430R8"},
}


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9_]+", "_", value.lower().strip())
    return re.sub(r"_+", "_", slug).strip("_") or "myhome_entity"


def _next_device_id(devices: dict, requested_id: str) -> str:
    if requested_id not in devices:
        return requested_id

    counter = 2
    while f"{requested_id}_{counter}" in devices:
        counter += 1
    return f"{requested_id}_{counter}"


def _entity_exists(devices: dict, entity: dict) -> bool:
    requested_where = str(entity.get(CONF_WHERE, ""))
    requested_zone = str(entity.get(CONF_ZONE, ""))
    requested_interface = str(entity.get(CONF_BUS_INTERFACE, ""))
    for device in devices.values():
        if not isinstance(device, dict):
            continue
        existing_where = str(device.get(CONF_WHERE, ""))
        existing_zone = str(device.get(CONF_ZONE, ""))
        existing_interface = str(device.get(CONF_BUS_INTERFACE, ""))
        if requested_zone and existing_zone == requested_zone:
            return True
        if requested_where and existing_where == requested_where and existing_interface == requested_interface:
            return True
    return False


def _find_raw_gateway_key(config: dict, gateway_mac=None):
    if not config:
        return None

    if gateway_mac is None:
        return next(iter(config))

    formatted_gateway = format_mac(gateway_mac)
    if formatted_gateway is None:
        return None

    for gateway_key, gateway_config in config.items():
        if format_mac(str(gateway_config.get(CONF_MAC, ""))) == formatted_gateway:
            return gateway_key
    return None


def _normalize_climate_zone(value, central=False):
    zone = str(value or "#0").strip()
    if not zone:
        return "#0"
    while zone.startswith("#0#") and not central:
        zone = zone[3:]
    if central:
        return "#0" if zone == "#0" else zone.replace("#0#", "", 1).lstrip("#")
    if zone == "#0":
        return zone
    zone = zone.lstrip("#")
    return zone.split("#", 1)[0] if "#" in zone else zone


def _build_entity_config(platform: str, data: dict) -> dict:
    if platform == "climate":
        central = bool(data.get("central", False))
        entity = {
            CONF_ZONE: _normalize_climate_zone(data.get("zone") or data.get("where"), central),
            "name": str(data["name"]),
        }
    else:
        entity = {
            "where": str(data["where"]),
            "name": str(data["name"]),
        }

    optional_string_fields = {
        CONF_BUS_INTERFACE: "interface",
        CONF_ENTITY_NAME: "entity_name",
        CONF_DEVICE_MODEL: "model",
        "icon": "icon",
        "icon_on": "icon_on",
    }
    for config_key, service_key in optional_string_fields.items():
        value = data.get(service_key)
        if value not in (None, ""):
            entity[config_key] = str(value)

    if platform == "switch" and data.get("class") not in (None, ""):
        entity[CONF_DEVICE_CLASS] = str(data["class"])
    elif platform == "light":
        is_dimmable = bool(data.get("dimmable", False))
        entity[CONF_DIMMABLE] = is_dimmable
        if CONF_DEVICE_MODEL not in entity:
            entity[CONF_DEVICE_MODEL] = (
                DEFAULT_DEVICE_MODEL_BY_PLATFORM.get(platform, {}).get(
                    is_dimmable,
                    "F417U2",
                )
            )
    elif platform == "cover":
        entity[CONF_ADVANCED_SHUTTER] = bool(data.get("advanced", False))
    elif platform == "climate":
        entity[CONF_HEATING_SUPPORT] = bool(data.get("heat", True))
        entity[CONF_COOLING_SUPPORT] = bool(data.get("cool", False))
        entity[CONF_FAN_SUPPORT] = bool(data.get("fan", False))
        entity[CONF_STANDALONE] = bool(data.get("standalone", False))
        entity[CONF_CENTRAL] = bool(data.get("central", False))
    elif platform in ("binary_sensor", "sensor"):
        if data.get("class") not in (None, ""):
            entity[CONF_DEVICE_CLASS] = str(data["class"])

    return entity


async def async_setup(hass, config):
    """Set up the MyHOME component."""
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["_bus_monitor"] = []
    hass.http.register_view(MyHomeBusMonitorView())
    hass.http.register_view(MyHomeBusMonitorDataView())
    hass.http.register_view(MyHomeBusMonitorClearView())
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                "/myhome_static",
                hass.config.path("custom_components/myhome/frontend"),
                False,
            )
        ]
    )
    await async_register_panel(hass)

    if DOMAIN not in config:
        return True

    LOGGER.error("configuration.yaml not supported for this component!")

    return False


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    if entry.data[CONF_MAC] not in hass.data[DOMAIN]:
        hass.data[DOMAIN][entry.data[CONF_MAC]] = {}
    hass.data[DOMAIN].pop("_bus_monitor_seen", None)

    _config_file_path = (
        str(entry.options[CONF_FILE_PATH])
        if CONF_FILE_PATH in entry.options
        else "/config/myhome.yaml"
    )
    _generate_events = (
        entry.options[CONF_GENERATE_EVENTS]
        if CONF_GENERATE_EVENTS in entry.options
        else False
    )

    try:
        async with aiofiles.open(_config_file_path, mode="r") as yaml_file:
            _validated_config = config_schema(yaml.safe_load(await yaml_file.read()))
    except FileNotFoundError:
        LOGGER.error(f"Configartion file '{_config_file_path}' is not present!")
        return False

    if entry.data[CONF_MAC] in _validated_config:
        hass.data[DOMAIN][entry.data[CONF_MAC]] = _validated_config[
            entry.data[CONF_MAC]
        ]
    else:
        return False

    # Migrating the config entry's unique_id if it was not formated to the recommended hass standard
    if entry.unique_id != dr.format_mac(entry.unique_id):
        hass.config_entries.async_update_entry(
            entry, unique_id=dr.format_mac(entry.unique_id)
        )
        LOGGER.warning("Migrating config entry unique_id to %s", entry.unique_id)

    hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_ENTITY] = MyHOMEGatewayHandler(
        hass=hass, config_entry=entry, generate_events=_generate_events
    )

    gateway_handler = hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_ENTITY]
    try:
        tests_results = await gateway_handler.test()
    except OSError as ose:
        hass.data[DOMAIN][entry.data[CONF_MAC]].pop(CONF_ENTITY, None)
        _host = gateway_handler.gateway.host
        raise ConfigEntryNotReady(
            f"Gateway cannot be reached at {_host}, make sure its address is correct."
        ) from ose

    if not tests_results["Success"]:
        if (
            tests_results["Message"] == "password_error"
            or tests_results["Message"] == "password_required"
        ):
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN,
                    context={"source": SOURCE_REAUTH},
                    data=entry.data,
                )
            )
        del hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_ENTITY]
        return False

    _command_worker_count = (
        int(entry.options[CONF_WORKER_COUNT])
        if CONF_WORKER_COUNT in entry.options
        else 1
    )

    entity_registry = er.async_get(hass)
    device_registry = dr.async_get(hass)

    gateway_device_entry = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections={(dr.CONNECTION_NETWORK_MAC, entry.data[CONF_MAC])},
        identifiers={
            (DOMAIN, hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_ENTITY].unique_id)
        },
        manufacturer=hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_ENTITY].manufacturer,
        name=hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_ENTITY].name,
        model=hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_ENTITY].model,
        sw_version=hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_ENTITY].firmware,
    )

    platforms = list(hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_PLATFORMS].keys())
    if UPDATE not in platforms:
        platforms.append(UPDATE)

    await hass.config_entries.async_forward_entry_setups(entry, platforms)

    hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_ENTITY].listening_worker = (
        hass.loop.create_task(
            hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_ENTITY].listening_loop()
        )
    )
    for i in range(_command_worker_count):
        hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_ENTITY].sending_workers.append(
            hass.loop.create_task(
                hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_ENTITY].sending_loop(i)
            )
        )

    # Pruning lose entities and devices from the registry
    entity_entries = er.async_entries_for_config_entry(entity_registry, entry.entry_id)

    entities_to_be_removed = []
    devices_to_be_removed = [
        device_entry.id
        for device_entry in device_registry.devices.values()
        if entry.entry_id in device_entry.config_entries
    ]

    configured_entities = []
    configured_entities.append(f"{entry.data[CONF_MAC]}-integration-update")

    for _platform in hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_PLATFORMS].keys():
        for _device in hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_PLATFORMS][
            _platform
        ].keys():
            for _entity_name in hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_PLATFORMS][
                _platform
            ][_device][CONF_ENTITIES]:
                if _entity_name != _platform:
                    configured_entities.append(
                        f"{entry.data[CONF_MAC]}-{_device}-{_entity_name}"
                    )  # extrapolating _attr_unique_id out of the entity's place in the config data structure
                else:
                    configured_entities.append(
                        f"{entry.data[CONF_MAC]}-{_device}"
                    )  # extrapolating _attr_unique_id out of the entity's place in the config data structure

    for entity_entry in entity_entries:
        if entity_entry.unique_id in configured_entities:
            if entity_entry.device_id in devices_to_be_removed:
                devices_to_be_removed.remove(entity_entry.device_id)
            continue
        entities_to_be_removed.append(entity_entry.entity_id)

    for enity_id in entities_to_be_removed:
        entity_registry.async_remove(enity_id)

    if gateway_device_entry.id in devices_to_be_removed:
        devices_to_be_removed.remove(gateway_device_entry.id)

    for device_id in devices_to_be_removed:
        if (
            len(
                er.async_entries_for_device(
                    entity_registry, device_id, include_disabled_entities=True
                )
            )
            == 0
        ):
            device_registry.async_remove_device(device_id)

    # Defining the services
    async def handle_sync_time(call):
        gateway = call.data.get(ATTR_GATEWAY, None)
        if gateway is None:
            gateway = list(hass.data[DOMAIN].keys())[0]
        else:
            mac = format_mac(gateway)
            if mac is None:
                LOGGER.error(
                    "Invalid gateway mac `%s`, could not send time synchronisation message.",
                    gateway,
                )
                return False
            else:
                gateway = mac
        timezone = hass.config.as_dict()["time_zone"]
        if gateway in hass.data[DOMAIN]:
            await hass.data[DOMAIN][gateway][CONF_ENTITY].send(
                OWNGatewayCommand.set_datetime_to_now(timezone)
            )
        else:
            LOGGER.error(
                "Gateway `%s` not found, could not send time synchronisation message.",
                gateway,
            )
            return False

    hass.services.async_register(DOMAIN, "sync_time", handle_sync_time)

    async def handle_send_message(call):
        gateway = call.data.get(ATTR_GATEWAY, None)
        message = call.data.get(ATTR_MESSAGE, None)
        if gateway is None:
            gateway = list(hass.data[DOMAIN].keys())[0]
        else:
            mac = format_mac(gateway)
            if mac is None:
                LOGGER.error(
                    "Invalid gateway mac `%s`, could not send message `%s`.",
                    gateway,
                    message,
                )
                return False
            else:
                gateway = mac
        LOGGER.debug("Handling message `%s` to be sent to `%s`", message, gateway)
        if gateway in hass.data[DOMAIN]:
            if message is not None:
                own_message = OWNCommand.parse(message)
                if own_message is not None:
                    if own_message.is_valid:
                        LOGGER.debug(
                            "%s Sending valid OpenWebNet Message: `%s`",
                            hass.data[DOMAIN][gateway][CONF_ENTITY].log_id,
                            own_message,
                        )
                        await hass.data[DOMAIN][gateway][CONF_ENTITY].send(own_message)
                else:
                    LOGGER.error(
                        "Could not parse message `%s`, not sending it.", message
                    )
                    return False
        else:
            LOGGER.error(
                "Gateway `%s` not found, could not send message `%s`.", gateway, message
            )
            return False

    hass.services.async_register(DOMAIN, "send_message", handle_send_message)

    async def handle_create_entity(call):
        platform = str(call.data.get("platform", "")).strip()
        if platform not in CREATE_ENTITY_PLATFORMS:
            LOGGER.error("Invalid platform `%s`, could not create entity.", platform)
            return False

        where = call.data.get("where")
        zone = call.data.get("zone")
        if platform == "climate":
            where = zone or where or "#0"
        elif not where:
            LOGGER.error("Missing where, could not create entity.")
            return False

        name = call.data.get("name")
        if not name:
            default_name_prefix = {
                "cover": "Rolladen",
                "light": "Licht",
                "switch": "Schalter",
                "climate": "Thermostat",
                "binary_sensor": "Sensor",
                "sensor": "Sensor",
            }
            name = f"{default_name_prefix.get(platform, platform.title())} {where}"

        model = call.data.get("model")
        if model not in (None, "") and str(model) not in DEVICE_MODEL_OPTIONS:
            LOGGER.warning(
                "Creating MyHome entity with unknown device model `%s`.",
                model,
            )

        async with aiofiles.open(_config_file_path, mode="r") as yaml_file:
            raw_config = yaml.safe_load(await yaml_file.read()) or {}

        gateway_key = _find_raw_gateway_key(raw_config, call.data.get(ATTR_GATEWAY))
        if gateway_key is None:
            LOGGER.error(
                "Gateway `%s` not found, could not create entity.",
                call.data.get(ATTR_GATEWAY),
            )
            return False

        updated_config = copy.deepcopy(raw_config)
        gateway_config = updated_config[gateway_key]
        gateway_config.setdefault(platform, {})
        requested_id = call.data.get("device_id") or _slugify(str(name))
        device_id = _next_device_id(gateway_config[platform], _slugify(str(requested_id)))
        entity_config = _build_entity_config(platform, call.data)

        if _entity_exists(gateway_config[platform], entity_config):
            entity_location = entity_config.get(CONF_WHERE) or entity_config.get(CONF_ZONE)
            LOGGER.info(
                "MyHome %s entity `%s` already exists in %s, skipping.",
                platform,
                entity_location,
                _config_file_path,
            )
            return True

        gateway_config[platform][device_id] = entity_config

        try:
            config_schema(copy.deepcopy(updated_config))
        except Exception as err:  # noqa: BLE001
            LOGGER.error(
                "Generated entity `%s` is not valid and was not written: %s",
                device_id,
                err,
            )
            return False

        async with aiofiles.open(f"{_config_file_path}.bak", mode="w") as yaml_file:
            await yaml_file.write(yaml.safe_dump(raw_config, sort_keys=False))

        async with aiofiles.open(_config_file_path, mode="w") as yaml_file:
            await yaml_file.write(yaml.safe_dump(updated_config, sort_keys=False))

        LOGGER.info(
            "Created MyHome %s entity `%s` in %s. Reload the integration to load it.",
            platform,
            device_id,
            _config_file_path,
        )
        return True

    hass.services.async_register(DOMAIN, "create_entity", handle_create_entity)

    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""

    LOGGER.info("Unloading MyHome entry.")

    platforms = list(hass.data[DOMAIN][entry.data[CONF_MAC]][CONF_PLATFORMS].keys())
    if UPDATE not in platforms:
        platforms.append(UPDATE)

    for platform in platforms:
        await hass.config_entries.async_forward_entry_unload(entry, platform)

    hass.services.async_remove(DOMAIN, "sync_time")
    hass.services.async_remove(DOMAIN, "send_message")
    hass.services.async_remove(DOMAIN, "create_entity")

    gateway_handler = hass.data[DOMAIN][entry.data[CONF_MAC]].pop(CONF_ENTITY)
    del hass.data[DOMAIN][entry.data[CONF_MAC]]

    return await gateway_handler.close_listener()
