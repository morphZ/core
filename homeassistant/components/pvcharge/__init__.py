"""The pvcharge integration."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN
from .pvcharger import PVCharger

_LOGGER = logging.getLogger(__name__)

CONF_BALANCE = "balance_entity"
CONF_BALANCE_TEMPLATE = "balance_template"
CONF_CHARGE_ENTITY = "charge_entity"
CONF_SWITCH = "charge_switch"
CONF_MIN = "charge_min"
CONF_MAX = "charge_max"
CONF_THRESHOLD = "pv_threshold"
CONF_HYSTERESIS = "pv_hysteresis"
CONF_DURATION = "boost_duration"
CONF_SOC = "soc_template"
CONF_LOW_VALUE = "soc_low_value"
CONF_REFRESH = "refresh_interval"

DEFAULT_DURATION = 30

PVCHARGE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_BALANCE_TEMPLATE): cv.template,
        # vol.Required(CONF_CHARGE_ENTITY): cv.entity_id,
        vol.Optional(CONF_SWITCH): cv.entity_id,
        vol.Required(CONF_MIN): vol.Coerce(float),
        vol.Required(CONF_MAX): vol.Coerce(float),
        vol.Optional(CONF_THRESHOLD): vol.Coerce(float),
        vol.Optional(CONF_HYSTERESIS): vol.Coerce(float),
        vol.Required(CONF_DURATION, default=DEFAULT_DURATION): vol.Coerce(int),
        vol.Optional(CONF_SOC): cv.template,
        vol.Optional(CONF_LOW_VALUE): vol.Coerce(float),
        vol.Optional(CONF_REFRESH): vol.Coerce(int),
    }
)

CONFIG_SCHEMA = vol.Schema({DOMAIN: PVCHARGE_SCHEMA}, extra=vol.ALLOW_EXTRA)

# CONFIG_SCHEMA = vol.Schema(
#     {DOMAIN: cv.schema_with_slug_keys(PVCHARGE_SCHEMA)}, extra=vol.ALLOW_EXTRA
# )


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up pvcharge from a config entry."""
    # pylint: disable=no-member
    _LOGGER.warning("Enter async_setup")

    # hass.data.setdefault(DOMAIN, {})
    params = [config[DOMAIN].get(k, None) for k in PVCHARGE_SCHEMA.schema.keys()]

    pvc = PVCharger(hass, *params)
    await pvc.auto()  # type: ignore

    return True
