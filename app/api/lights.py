import json
import operator
from pydantic import ValidationError
from app.models import HueBridgeInputBase, LightDataInputBase, SwitchDataInputBase
from .hue_bridge import HueBridge


class Light:
    """
    This will deal with all the logic related to the smart lights.
    """

    def __init__(self, hue_bridge: HueBridge):
        self.hue_bridge = hue_bridge

    def get_all_lights(self):
        full_endpoint = f"lights/"
        light_status = self.hue_bridge.base_api_request(
            endpoint=full_endpoint,
            method="GET",
        ).json()
        self.light_list = []
        for item in light_status:
            light_status[item]["id"] = item
            if light_status[item]["productname"] == "Hue smart plug":
                try:
                    valid_data = SwitchDataInputBase.parse_obj(light_status[item])
                except ValidationError as err:
                    print(err)
                else:
                    self.light_list.append(valid_data.dict())
                print(valid_data)
            else:
                try:
                    valid_data = LightDataInputBase.parse_obj(light_status[item])
                except ValidationError as err:
                    print(err)
                else:
                    self.light_list.append(valid_data.dict())

        self.light_list.sort(key=lambda k: k["id"])
        return self.light_list

    def get_light_status(self, target_device: str):
        full_endpoint = f"lights/{target_device}"
        light_status = self.hue_bridge.base_api_request(
            endpoint=full_endpoint,
            method="GET",
        )

        return light_status.json()
