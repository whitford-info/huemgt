from urllib.parse import urlparse, urlencode
from ipaddress import IPv4Address, IPv6Address
from typing import Union, Optional
from pydantic import BaseModel, Field, validator, root_validator

__all__ = ["HueBridgeInputBase"]

# TODO: Turn this into a pydantic model.


class HueBridgeFields:
    username = Field(description="This is the username for the API.")
    name = Field(description="Name of the bridge.")
    ip = Field(description="IP for the API.")
    all_ip_address = Field(description="IP for the API.")
    bridge_type = Field(description="IP for the API.")
    port = Field(description="IP for the API.")
    model = Field(description="IP for the API.")
    mac = Field(description="IP for the API.")
    base_url = Field(description="IP for the API.")

class HueBridgeInputBase(BaseModel):
    username: str = HueBridgeFields.username
    name: str = HueBridgeFields.name
    ip: IPv4Address = HueBridgeFields.ip
    all_ip_address: list[IPv4Address | IPv6Address] = HueBridgeFields.all_ip_address
    bridge_type: str = HueBridgeFields.bridge_type
    port: int = HueBridgeFields.port
    model: str = HueBridgeFields.model
    mac: str = HueBridgeFields.mac
    base_url: str = HueBridgeFields.base_url
