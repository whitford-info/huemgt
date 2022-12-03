import json
import tomli

from os import environ
from app.components import BridgeComm
from app.models import *

"""
Required Enviromental Variables:
    BRIDGE_UN: str, username for the bridge...
"""


if __name__ == "__main__":
    with open("./config.toml", mode="rb") as cf:
        config = tomli.load(cf)

    bc = BridgeComm(config)

    # First we need to find the bridge units.
    bridge_units = bc.discover_bridge_units()

    if len(bridge_units) == 1:
        bridge_unit = bridge_units[0]

    print(bridge_unit)
    light_id = 3
    light = bc.api_get(target_bridge=bridge_unit, endpoint="lights", device=light_id)
    print(f"type={type(light)},Light: {light}")
    if light:
        test = LightDataInputBase(id=light_id, **light)
        print(f"Test: {test}")
