import logging
from datetime import datetime, timezone
from pathlib import Path
from os import mkdir
from tomli import load as tomli_load
from os import environ
from app.components import HueBridgeSetup
from app.models import *
from app.api import Light

"""
Required Enviromental Variables:
    BRIDGE_UN: str, username for the bridge...
"""


if __name__ == "__main__":
    with open("./config.toml", mode="rb") as cf:
        config = tomli_load(cf)

    if config.get("log_level"):
        log_level = int(environ.get("LOG_LEVEL"))
    else:
        log_level = 10

    log_path = Path("./logs/")
    log_name = f"{datetime.now(timezone.utc).strftime('%d%m%Y')}.log"
    log_name = Path(log_path, log_name)
    if not log_path.is_dir():
        mkdir(log_path)

    log = logging.getLogger("hbridge")
    log.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(log_level)
    log.addHandler(console)

    bc = HueBridgeSetup(config)

    # First we need to find the bridge units.
    bridge_units = bc.discover_bridge_units()

    if len(bridge_units) == 1:
        bridge_unit = bridge_units[0]

    print(bridge_unit)
    lights = Light(bridge_unit)
    get_all_lights = lights.get_all_lights()
    print(f"Light List: {get_all_lights}")
    light_info = lights.get_light_status(target_device="3")
    print(f"Light 3 Info: {light_info}")

    # light_id = 3
    # light = bc.api_get(target_bridge=bridge_unit, endpoint="lights", device=light_id)
    # print(f"type={type(light)},Light: {light}")
    # if light:
    #     test = LightDataInputBase(id=light_id, **light)
    #     print(f"Test: {test}")
