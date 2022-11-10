import tomli
from app.components import HueBridgeComm

with open("./config.toml", mode="rb") as cf:
    config = tomli.load(cf)

if __name__ == "__main__":
    bc = HueBridgeComm(config)

    # First we need to find the bridge units.
    bridge_units = bc.discover_bridge_units()

    for item in bridge_units:
        print(f"BU Raw Data: {item}")
        print(f"BU Name: {item.bridge_name}")
