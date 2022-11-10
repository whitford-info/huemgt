from ipaddress import IPv4Address, IPv6Address
from typing import Union
from dataclasses import dataclass

__all__ = ["HueBridgeUnit"]


@dataclass
class HueBridgeUnit:
    bridge_name: str
    bridge_ip: IPv4Address
    all_ip_address: [Union[IPv4Address, IPv6Address]]
    bridge_api_url: str
    bridge_type: str
    bridge_port: int
    bridge_model: str
    bridge_mac: str
