from pydantic import Field, BaseModel, Extra
from datetime import datetime

__all__ = ["LightDataFields", "LightDataInputBase"]


class LightState(BaseModel):
    on: bool = Field(description="Is the light on(True) or off(False)?")
    bri: int = Field(description="The brightness of the light.", example=142)
    hue: int = Field(description="The hue of the light.", example=8417)
    sat: int = Field(description="the saturation of the light.", example=140)
    effect: str = Field(
        description="The effect of the light currently has applioed", example="none"
    )
    xy: list = Field(
        description="This is the XY values of the light.", example=[0.4573, 0.4100]
    )
    ct: int = Field(description="", example=366)
    alert: str = Field(description="", example="select")
    colormode: str = Field(description="", example="ct")
    mode: str = Field(description="Mode of the light.", example="homeautomation")
    reachable: bool = Field(description="Can the hue bridge access the light?")


class LightSWUpdate(BaseModel):
    state: str = Field(description="If there is an update pending")
    lastinstall: datetime = Field("Date time of the last software update.")


class LightCapabilitiesCT(BaseModel):
    min: int = Field(description="", example=153)
    max: int = Field(description="", example=500)


class LightCapabilitiesControl(BaseModel):
    mindimlevel: int = Field(description="Minimum Dim Level", example=200)
    maxlumen: int = Field(description="Maximum lumens", example=1100)
    colorgamuttype: str = (Field(description="Color gradient type", example="C"),)
    colorgamut: list[list] = Field(description="Color gamut: RGB?")
    ct: LightCapabilitiesCT = Field(description="")


class LightCapabilitiesStreaming(BaseModel):
    renderer: bool = Field(description="")
    proxy: bool = Field(description="")


class LightCapabilities(BaseModel):
    certified: bool = Field(description="Is this a certified hue product?")
    control: LightCapabilitiesControl
    streaming: LightCapabilitiesStreaming


class LightConfigStartup(BaseModel):
    mode: str = Field(
        description="What mode the light will start up in.", example="safety"
    )
    configured: bool = Field(description="If the startup mode is configured.")


class LightConfig(BaseModel):
    archetype: str = Field(
        description="Describes the arche type of the light.", example="sultanbulb"
    )
    function: str = Field(description="Function of the light", example="mixed")
    direction: str = Field(
        description="Light directionality", example="omnidirectional"
    )
    startup: LightConfigStartup = Field(
        description="Describes how the light will cold powerup."
    )


class LightDataFields:
    id = Field(description="This is the Id of the light.")
    collection_time = Field(description="When this information was collected.", default_factory=datetime.now)
    state = Field(
        description="This field contains information related to the state of the light."
    )
    swupdate: LightSWUpdate = Field(
        description="Provides information related to the lights firmware updates."
    )
    type = Field(description="The type of light.", example="Extended color light")
    name = Field(
        description="The user set name for the light.", example="Office Desk"
    )
    modelid = Field(description="The Model ID", example="LCA007")
    manufacturername: str = Field(
        description="The manufacturers name.", example="Signify Netherlands B.V."
    )
    productname = Field(description="The product name.", example="Hue color lamp")
    capabilities = Field(
        description="Describes the capabilities of the lights."
    )
    config: LightConfig = Field(description="Describes the configuration of the light.")
    uniqueid = Field(
        description="The unique id of the light.", example="00:17:88:01:0c:6d:be:66-0b"
    )
    swversion = Field(
        description="Current software version of the light.", example="1.93.11"
    )
    swconfigid = Field(
        description="Software configuration ID.", example="47270DB8"
    )
    productid = Field(
        description="Full Product ID.", example="Philips-LCA007-1-A19HECLv1"
    )


class LightDataInputBase(BaseModel):
    id: int = LightDataFields.id
    collection_time: datetime = LightDataFields.collection_time
    state: LightState = LightDataFields.state
    swupdate: LightSWUpdate = LightDataFields.swupdate
    type: str = LightDataFields.type
    name: str = LightDataFields.name
    modelid: str = LightDataFields.modelid
    manufacturername: str = LightDataFields.manufacturername
    productname: str = LightDataFields.productname
    capabilities: LightCapabilities = LightDataFields.capabilities
    config: LightConfig = LightDataFields.config
    uniqueid: str = LightDataFields.uniqueid
    swversion: str = LightDataFields.swversion
    swconfigid: str = LightDataFields.swconfigid
    productid: str = LightDataFields.productid

    class Config:
        allow_population_by_field_name = True
        # arbitrary_types_allowed = True  # required for the _id
        # json_encoders = {ObjectId: str}
        extra = Extra.forbid
