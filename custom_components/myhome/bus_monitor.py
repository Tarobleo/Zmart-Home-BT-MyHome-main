from aiohttp import web
from homeassistant.components.http import HomeAssistantView

DOMAIN = "myhome"


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
        return web.json_response(data)
