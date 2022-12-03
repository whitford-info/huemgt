import json
import requests
from urllib.parse import urlencode
from os import environ
from ipaddress import IPv4Address
from typing import Optional, Union
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener, IPVersion

from app.models import HueBridgeInputBase
from app.models.enums import RequestMethodEnum

__all__ = ["BridgeComm"]


class BridgeDiscoveryListener(ServiceListener):
    name: list = []

    def add_service(self, zc: "Zeroconf", type_: str, name: str) -> None:
        self.name.append(name)

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.name.append(name)


class BridgeComm:

    """
    This will deal with storing the bridges and dealing with the requests to the API endpoints.

    """

    bridge_units: list[HueBridgeInputBase] = []

    def __init__(self, config):
        self.base_discovery_url = config["huebridge"]["base_discovery_url"]
        self.service_type = config["huebridge"]["mdns_service_type"]

        # TODO: This will be created and handled differntly when the first version goes live. The application will
        #  create its own username and persist that. For now well just make it an env variable.

        self.user_name = environ.get("BRIDGE_UN")

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

    def discover_bridge_units(self) -> list[HueBridgeInputBase]:
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
                base_url = f"http://{str(bridge_ip)}/api/{self.user_name}/"
                print(base_url)
                bridge_unit_data = HueBridgeInputBase(
                    username=self.user_name,
                    name=item,
                    ip=bridge_ip,
                    all_ip_address=bridges.parsed_addresses(),
                    port=bridges.port,
                    bridge_type=bridges.type,
                    model=bridges.properties.get("modelid".encode("utf-8")).decode(
                        "utf-8"
                    ),
                    mac=bridges.properties.get("bridgeid".encode("utf-8")).decode(
                        "utf-8"
                    ),
                    base_url=base_url
                )
                self.bridge_units.append(bridge_unit_data)

        return self.bridge_units

    # TODO: Perhaps API Communication should be seperated MORE from discovery and creation.
    def _base_api_request(
        self,
        target_bridge: HueBridgeInputBase,
        endpoint: str,
        method: RequestMethodEnum,
        device: str | list | int = None,
    ) -> requests.Response:

        full_url = f"{target_bridge.base_url}{endpoint}/{device}/"
        try:
            match method:
                case "GET":
                    response = requests.get(url=full_url
            )

        except requests.exceptions.HTTPError as err:
            raise err
        else:
            return response

    def api_get(self, target_bridge: HueBridgeInputBase, endpoint: str, device: int = None):
        response = self._base_api_request(target_bridge=target_bridge, endpoint=endpoint, device=device, method="GET")
        return response.json()