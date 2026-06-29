"""Update entity for the MyHome integration."""

from __future__ import annotations

import asyncio
import json
from datetime import timedelta
from pathlib import Path

from aiohttp import ClientError
from homeassistant.components.update import DOMAIN as PLATFORM, UpdateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MAC
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_ENTITY, DOMAIN, LOGGER

GITHUB_REPOSITORY = "Tarobleo/Zmart-Home-BT-MyHome-main"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPOSITORY}"
GITHUB_REPOSITORY_URL = f"https://github.com/{GITHUB_REPOSITORY}"
SCAN_INTERVAL = timedelta(hours=6)


def _installed_version() -> str:
    manifest_path = Path(__file__).with_name("manifest.json")
    with manifest_path.open(encoding="utf-8") as manifest_file:
        return str(json.load(manifest_file).get("version", "0.0.0"))


def _clean_version(version: str) -> str:
    return str(version or "").strip().removeprefix("v").removeprefix("V")


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities,
) -> None:
    """Set up the update entity."""
    gateway = hass.data[DOMAIN][config_entry.data[CONF_MAC]][CONF_ENTITY]
    installed_version = await hass.async_add_executor_job(_installed_version)
    async_add_entities(
        [
            MyHOMEUpdateEntity(
                gateway=gateway,
                installed_version=installed_version,
            )
        ],
        True,
    )


class MyHOMEUpdateEntity(UpdateEntity):
    """Represent the integration update status."""

    _attr_has_entity_name = True
    _attr_name = "Integration Update"
    _attr_title = "Zmart Home BT MyHome"
    _attr_entity_registry_enabled_default = True

    def __init__(self, gateway, installed_version: str) -> None:
        self._gateway = gateway
        self._attr_unique_id = f"{gateway.mac}-integration-update"
        self._attr_installed_version = _clean_version(installed_version)
        self._attr_latest_version = self._attr_installed_version
        self._attr_release_url = GITHUB_REPOSITORY_URL
        self._attr_device_info = {
            "identifiers": {(DOMAIN, gateway.unique_id)},
            "name": gateway.name,
            "manufacturer": gateway.manufacturer,
            "model": gateway.model,
            "sw_version": gateway.firmware,
        }

    async def async_update(self) -> None:
        """Fetch the newest available release or tag from GitHub."""
        session = async_get_clientsession(self.hass)
        try:
            latest = await self._async_latest_release(session)
            if latest is None:
                latest = await self._async_latest_tag(session)
        except (ClientError, asyncio.TimeoutError, ValueError) as err:
            LOGGER.debug(
                "%s Could not check for integration updates: %s",
                self._gateway.log_id,
                err,
            )
            return

        if latest is None:
            return

        self._attr_latest_version = _clean_version(latest["version"])
        self._attr_release_url = latest["url"]

    async def _async_latest_release(self, session):
        async with session.get(
            f"{GITHUB_API_URL}/releases/latest",
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "Zmart-Home-BT-MyHome",
            },
            timeout=10,
        ) as response:
            if response.status == 404:
                return None
            response.raise_for_status()
            payload = await response.json()
        version = payload.get("tag_name") or payload.get("name")
        if not version:
            return None
        return {
            "version": version,
            "url": payload.get("html_url") or GITHUB_REPOSITORY_URL,
        }

    async def _async_latest_tag(self, session):
        async with session.get(
            f"{GITHUB_API_URL}/tags",
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "Zmart-Home-BT-MyHome",
            },
            timeout=10,
        ) as response:
            response.raise_for_status()
            payload = await response.json()
        if not payload:
            return None
        version = payload[0].get("name")
        if not version:
            return None
        return {
            "version": version,
            "url": f"{GITHUB_REPOSITORY_URL}/releases/tag/{version}",
        }
