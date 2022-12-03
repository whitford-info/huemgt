from ipaddress import IPv4Address, IPv6Address
from typing import Union
from dataclasses import dataclass

__all__ = ["ConfigData"]


@dataclass
class ConfigData:
    base_discovery_url: str
    mdns_service_type: str
