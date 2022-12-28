import requests
from os import environ
from ipaddress import IPv4Address
from app.models.enums import *

__all__ = ["HueBridge"]


class HueBridge:
    def __init__(
        self,
        name: str,
        ip: IPv4Address,
        all_ip_address: list,
        bridge_type: str,
        port: int,
        model: str,
        mac: str,
    ):
        # TODO Better username mgt
        self.user_name = environ.get("BRIDGE_UN")

        self.name = name
        self.ip = ip
        self.all_ip_address = all_ip_address
        self.bridge_type = bridge_type
        self.port = port
        self.model = model
        self.mac = mac
        self.base_url = f"http://{str(ip)}/api/{self.user_name}/"

    def base_api_request(
        self,
        endpoint: str,
        method: RequestMethodEnum,
    ) -> requests.Response:

        full_url = f"{self.base_url}{endpoint}"
        print(full_url)
        try:
            match method:
                case "GET":
                    response = requests.get(url=full_url)

        except requests.exceptions.HTTPError as err:
            raise err
        else:
            return response
