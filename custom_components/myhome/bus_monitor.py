from aiohttp import web
from homeassistant.const import CONF_NAME
from homeassistant.components.http import HomeAssistantView

from .const import (
    CONF_BUS_INTERFACE,
    CONF_DEVICE_CLASS,
    CONF_DEVICE_MODEL,
    CONF_ENTITY_NAME,
    CONF_PLATFORMS,
    CONF_WHERE,
    CONF_WHO,
    DOMAIN,
)

MONITOR_VERSION = "20260629-13"


PLATFORM_TYPES = {
    "light": "Licht",
    "switch": "Schalter",
    "cover": "Rollladen",
    "binary_sensor": "Binärsensor",
    "sensor": "Sensor",
    "climate": "Heizung",
}

WHO_TYPES = {
    "1": "Licht/Schalter",
    "2": "Rollladen",
    "4": "Heizung",
    "9": "Aux",
    "18": "Energie",
    "25": "Kontakt",
}

WHO_PLATFORMS = {
    "1": "light",
    "2": "cover",
    "4": "climate",
    "18": "sensor",
    "25": "binary_sensor",
}


def _as_text(value):
    if value is None:
        return ""
    return getattr(value, "value", str(value))


def _friendly_address(where):
    if not where or not where.isdigit() or len(where) not in (2, 4):
        return where or ""
    split_at = len(where) // 2
    return f"{int(where[:split_at])}.{int(where[split_at:])}"


def _normalize_lighting_where(where):
    """Normalize short OWN light addresses such as 41 to configured 0401."""
    if not where or not where.isdigit() or len(where) != 2:
        return where
    return f"0{where[0]}0{where[1]}"


def _full_where(device):
    where = device.get(CONF_WHERE, "")
    interface = device.get(CONF_BUS_INTERFACE)
    return f"{where}#4#{interface}" if interface else where


def _device_type(platform, device):
    device_class = _as_text(device.get(CONF_DEVICE_CLASS)).lower()
    if platform == "switch" and device_class == "outlet":
        return "Steckdose"
    if platform == "binary_sensor" and device_class:
        return device_class.replace("_", " ").capitalize()
    if platform == "sensor" and device_class:
        return device_class.replace("_", " ").capitalize()
    return PLATFORM_TYPES.get(platform, platform)


def _configured_devices(hass):
    devices = []
    domain_data = hass.data.get(DOMAIN, {})
    for gateway_mac, gateway_data in domain_data.items():
        if str(gateway_mac).startswith("_") or not isinstance(gateway_data, dict):
            continue
        platforms = gateway_data.get(CONF_PLATFORMS, {})
        for platform, platform_devices in platforms.items():
            if platform == "button" or not isinstance(platform_devices, dict):
                continue
            for device_id, device in platform_devices.items():
                if not isinstance(device, dict):
                    continue
                where = _full_where(device)
                who = str(device.get(CONF_WHO, "") or str(device_id).split("-", 1)[0])
                name = device.get(CONF_ENTITY_NAME) or device.get(CONF_NAME) or ""
                description = device.get(CONF_NAME) or device.get(CONF_ENTITY_NAME) or ""
                devices.append(
                    {
                        "gateway_mac": gateway_mac,
                        "platform": platform,
                        "domain": platform,
                        "type": _device_type(platform, device),
                        "device_class": _as_text(device.get(CONF_DEVICE_CLASS)),
                        "model": _as_text(device.get(CONF_DEVICE_MODEL)),
                        "who": who,
                        "where": where,
                        "base_where": device.get(CONF_WHERE, ""),
                        "address": _friendly_address(device.get(CONF_WHERE, "")),
                        "name": name,
                        "room": name,
                        "description": description,
                    }
                )
    return devices


def _message_parts(raw):
    message = str(raw or "").strip().strip("`")
    if message.endswith("##"):
        message = message[:-2]
    if message.startswith("*#"):
        message = message[2:]
    elif message.startswith("*"):
        message = message[1:]
    return [part for part in message.split("*") if part]


def _candidate_where(who, parts, raw):
    raw_text = str(raw or "")
    where_parts = parts[1:] if raw_text.startswith("*#") else parts[2:]
    for part in where_parts:
        if not part or part in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            continue
        return _normalize_lighting_where(part) if who == "1" else part
    return ""


def _find_device(hass, who, parts, raw):
    raw_text = str(raw or "")
    where_parts = parts[1:] if raw_text.startswith("*#") else parts[2:]
    candidates = [
        device
        for device in _configured_devices(hass)
        if not who or device["who"] == who
    ]

    for part in where_parts:
        normalized_part = _normalize_lighting_where(part) if who == "1" else part
        for device in candidates:
            if part in (device["where"], device["base_where"]):
                return device
            if normalized_part in (device["where"], device["base_where"]):
                return device

    for device in sorted(candidates, key=lambda item: len(item["where"]), reverse=True):
        if device["where"] and device["where"] in raw_text:
            return device
        if device["base_where"] and device["base_where"] in raw_text:
            return device

    return None


def _telegram_action(who, parts, is_status):
    action = ""
    value = ""
    what = parts[1] if len(parts) > 1 else ""

    if is_status:
        action = "Statusantwort" if len(parts) > 2 else "Statusabfrage"
    elif who == "1":
        action = {
            "0": "Aus",
            "1": "Ein",
            "2": "20%",
            "3": "30%",
            "4": "40%",
            "5": "50%",
            "6": "60%",
            "7": "70%",
            "8": "80%",
            "9": "Dimmer/Level",
        }.get(what, f"Licht {what}" if what else "")
    elif who == "2":
        action = {
            "0": "Stopp",
            "1": "Öffnen/Hoch",
            "2": "Schließen/Runter",
        }.get(what, f"Rollladen {what}" if what else "")
    elif who == "4":
        action = "Temperatur/Heizung"
    elif who == "18":
        action = "Energie"
    elif who:
        action = f"WHO {who}"

    if is_status and len(parts) > 2:
        status_value = parts[-1]
        if who == "1" and status_value.isdigit():
            numeric = int(status_value)
            if numeric == 100:
                value = "Aus"
            elif 101 <= numeric <= 200:
                value = f"{numeric - 100}%"
            else:
                value = status_value
        else:
            value = status_value

    return action, value


def _decode_light_level(value):
    if not value or not str(value).isdigit():
        return value or ""
    numeric = int(value)
    if numeric == 0:
        return "Aus"
    if numeric == 1:
        return "Ein"
    if numeric == 100:
        return "Aus"
    if 101 <= numeric <= 200:
        return f"{numeric - 100}%"
    if 2 <= numeric <= 9:
        return f"{numeric * 10}%"
    return str(value)


def _decoded_values(label, where, dimension, values):
    details = []
    if where:
        details.append(f"Where {where}")
    if dimension:
        details.append(f"Dimension {dimension}")
    if values:
        details.append(f"Werte {'/'.join(values)}")
    return f"{label}: {', '.join(details)}" if details else label


def _decode_telegram(who, parts, raw, action, value, where):
    if not parts:
        return ""

    is_status = str(raw or "").startswith("*#")

    if who == "1":
        if is_status:
            dimension = parts[2] if len(parts) > 2 else ""
            values = parts[3:]
            if dimension == "1" and values:
                return f"Lichtstatus {where or parts[1]}: {_decode_light_level(values[0])}"
            if dimension == "2" and values:
                return _decoded_values("Lichtstatus", where or parts[1], dimension, values)
            return _decoded_values("Lichtstatus", where, dimension, values)
        if len(parts) > 1:
            return f"Lichtbefehl {where}: {_decode_light_level(parts[1])}"

    if who == "2":
        if is_status:
            dimension = parts[2] if len(parts) > 2 else ""
            values = parts[3:]
            return _decoded_values("Rollladenstatus", where, dimension, values)
        if action:
            return f"Rollladenbefehl {where}: {action}"

    if who == "4":
        dimension = parts[2] if is_status and len(parts) > 2 else ""
        values = parts[3:] if is_status else parts[2:]
        return _decoded_values("Heizung", where, dimension, values)

    if who == "13":
        if len(parts) >= 5 and parts[1] == "#0":
            return f"Gateway-Zeit: {parts[2]}:{parts[3]}:{parts[4]}"
        if len(parts) >= 6 and parts[1] == "#1":
            return f"Gateway-Datum: {'/'.join(parts[2:])}"
        return _decoded_values("Gateway", "", parts[1] if len(parts) > 1 else "", parts[2:])

    if who == "18":
        dimension = parts[2] if is_status and len(parts) > 2 else ""
        values = parts[3:] if is_status else parts[2:]
        return _decoded_values("Energie", where, dimension, values)

    if who == "25":
        dimension = parts[2] if is_status and len(parts) > 2 else ""
        values = parts[3:] if is_status else parts[2:]
        return _decoded_values("Kontakt", where, dimension, values)

    if value:
        return value
    if action:
        return action
    return f"WHO {who}: {'/'.join(parts[1:])}" if who else "/".join(parts)


def _parse_telegram(hass, raw):
    raw_text = str(raw or "")
    is_status = raw_text.startswith("*#")
    parts = _message_parts(raw_text)
    who = parts[0] if parts else ""
    where = _candidate_where(who, parts, raw_text)
    device = _find_device(hass, who, parts, raw_text)
    action, value = _telegram_action(who, parts, is_status)
    decoded = _decode_telegram(who, parts, raw_text, action, value, where)

    parsed = {
        "who": who,
        "where": where,
        "type": WHO_TYPES.get(who, f"WHO {who}" if who else ""),
        "domain": "",
        "suggested_domain": WHO_PLATFORMS.get(who, ""),
        "model": "",
        "room": "",
        "description": "",
        "address": _friendly_address(where),
        "action": action,
        "value": value,
        "decoded": decoded,
        "matched": False,
    }
    if device:
        parsed.update(device)
        parsed["matched"] = True
    return parsed


def _enrich_entry(hass, entry):
    enriched = dict(entry)
    enriched["monitor_version"] = MONITOR_VERSION
    enriched["parsed"] = _parse_telegram(hass, enriched.get("raw"))
    return enriched


class MyHomeBusMonitorView(HomeAssistantView):
    url = "/api/myhome/bus_monitor"
    name = "api:myhome:bus_monitor"
    requires_auth = True

    async def get(self, request):
        html = """
        <html>
        <head>
            <title>Zmart-Home Bus Monitor</title>
            <style>
                body { font-family: Arial; background:#111; color:#eee; padding:20px; }
                h1 { color:#38bdf8; }
                a { color:#38bdf8; }
            </style>
        </head>
        <body>
            <h1>Zmart-Home Live Bus Monitor</h1>
            <p>Der Live-Monitor ist im Home-Assistant-Seitenpanel verfügbar.</p>
            <p><a href="/zmart-myhome">Zmart Home Panel öffnen</a></p>
        </body>
        </html>
        """
        return web.Response(text=html, content_type="text/html")


class MyHomeBusMonitorDataView(HomeAssistantView):
    url = "/api/myhome/bus_monitor/data"
    name = "api:myhome:bus_monitor:data"
    requires_auth = True

    async def get(self, request):
        hass = request.app["hass"]
        data = hass.data.get(DOMAIN, {}).get("_bus_monitor", [])
        return web.json_response([_enrich_entry(hass, entry) for entry in data])


class MyHomeBusMonitorClearView(HomeAssistantView):
    url = "/api/myhome/bus_monitor/clear"
    name = "api:myhome:bus_monitor:clear"
    requires_auth = True

    async def post(self, request):
        hass = request.app["hass"]
        hass.data.setdefault(DOMAIN, {})["_bus_monitor"] = []
        hass.data.setdefault(DOMAIN, {})["_bus_monitor_seen"] = {}
        return web.json_response({"cleared": True, "monitor_version": MONITOR_VERSION})
