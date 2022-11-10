from ipaddress import IPv4Address
from typing import Optional
import requests
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener, IPVersion

from app.models import HueBridgeUnit
from app.models.enums import RequestMethodEnum
__all__ = ["HueBridgeComm"]


class BridgeDiscoveryListener(ServiceListener):
    name: list = []

    def add_service(self, zc: "Zeroconf", type_: str, name: str) -> None:
        self.name.append(name)

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.name.append(name)

class HueBridgeComm:
    bridge_units: list[HueBridgeUnit] = []

    def __init__(self, config):
        self.base_discovery_url = config["huebridge"]["base_discovery_url"]
        self.service_type = config["huebridge"]["mdns_service_type"]

    def get_bridge_data_from_url(self):
        """
        This is still needing to be worked on. I think what i will do is use this as a backup method if the normal
        discover_bridge_units method does not work.
        :return:
        """
        try:
            response = requests.get(self.base_discovery_url)
        except requests.exceptions.ConnectionError as err:
            raise err
        else:
            response.raise_for_status()

        res_body = response.json()

        if len(res_body) >= 1:
            self.id = res_body["id"]
            self.bridge_ip = res_body["internalipaddress"]

    def discover_bridge_units(self) -> list[HueBridgeUnit]:
        """
        This method will discover any Hue Bridges that are on the network via the mDNS service. This method will return
        a list of the HueBridgeUnits dataclass, which contain all the useful information about the bridge unit.
        :return: List[HueBridgeUnit]
        """
        zc = Zeroconf()
        listener = BridgeDiscoveryListener()

        # TODO: We should add in a method to do a service discovery here, so we are not only reliant on the config.
        ServiceBrowser(zc, self.service_type, listener)
        # Clear current units for rediscovery.
        self.bridge_units.clear()
        while len(listener.name) < 1:
            pass
        else:
            # TODO: This section is only theoretically how i think multiple bridges work. I will need to test with a
            #  second bridge..
            for item in listener.name:
                bridges = zc.get_service_info(self.service_type, item)
                bridge_ip = IPv4Address(
                    bridges.parsed_addresses(version=IPVersion.V4Only)[0]
                )
                bridge_unit_data = HueBridgeUnit(
                    bridge_name=item,
                    bridge_ip=bridge_ip,
                    all_ip_address=bridges.parsed_addresses(),
                    bridge_api_url=f"https://{bridge_ip}",
                    bridge_port=bridges.port,
                    bridge_type=bridges.type,
                    bridge_model=bridges.properties.get(
                        "modelid".encode("utf-8")
                    ).decode("utf-8"),
                    bridge_mac=bridges.properties.get(
                        "bridgeid".encode("utf-8")
                    ).decode("utf-8"),
                )
                self.bridge_units.append(bridge_unit_data)

        return self.bridge_units

    def api_request(self, target_bridge: HueBridgeUnit, target_device: Optional[str], method:RequestMethodEnum):
        pass