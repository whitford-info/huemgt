from app.components import BridgeComm


class Lights:
    """
    This will deal with all the logic related to the smart lights.
    """
    def get_all_lights(self):
        pass
    def get_light_status(self, target_bridge: HueBridgeUnit, target_device: str):
        light_status = self._base_api_request(
            target_endpoint="lights",
            target_bridge=target_bridge,
            target_device=target_device,
            method="GET",
        )
        return light_status