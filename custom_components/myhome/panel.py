from homeassistant.components import frontend
from homeassistant.core import HomeAssistant

DOMAIN = "myhome"


async def async_register_panel(hass: HomeAssistant) -> None:
    frontend.async_register_built_in_panel(
        hass,
        component_name="custom",
        sidebar_title="Zmart Home",
        sidebar_icon="mdi:home-lightning-bolt",
        frontend_url_path="zmart-myhome",
        config={
            "_panel_custom": {
                "name": "zmart-myhome-panel",
                "js_url": "/myhome_static/panel.js?v=20260629-4",
                "embed_iframe": False,
                "trust_external": False,
            }
        },
        require_admin=True,
    )
