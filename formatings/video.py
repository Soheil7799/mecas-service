from pydantic import  BaseModel, Field
# Video Filters declaration
class GrayScaleModel(BaseModel):
    enabled: bool = Field(default=False)
class ColorInvertModel(BaseModel):
    enabled: bool = Field(default=False)
class FrameIntpModel(BaseModel):
    enabled: bool = Field(default=False)
    targetFPS: int = Field(default=60)
class UpScalingModel(BaseModel):
    enabled: bool = Field(default=False)
    width: int = Field(default=1280)
    height: int = Field(default=720)