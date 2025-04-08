from enum import IntEnum
from fastapi import FastAPI, APIRouter
from typing import List, Optional
from pydantic import  BaseModel, Field
from api import api
# audio filters declarations
class GainCompModel(BaseModel):
    enabled: bool = Field(default=False)
    compressorThreshold: int = Field(default=-1)
    limitThreshold: int = Field(default=0)
class VoiceEnhModel(BaseModel):
    enabled: bool = Field(default=False)
    alpha: int = Field(default=3)
    highPass: int = Field(default=2)
class DenoiseDelayModel(BaseModel):
    enabled: bool = Field(default=False)
    noisePower: int = Field(default=-15)
    delay: int = Field(default=100)
    delayGain: int = Field(default=50)
class PhoneModel(BaseModel):
    enabled: bool = Field(default=False)
    sideGain: int = Field(default=0)
    order: int = Field(default=0)
class CarLikeModel(BaseModel):
    enabled: bool = Field(default=False)
    sideGain: int = Field(default=0)
    order: int = Field(default=0)

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


class FileFormat(IntEnum):
    AUDIO = 0
    VIDEO = 1

class BaseMedia(BaseModel):
    fileName: str = Field(...,description="File name without file format" )
    fileFormat: FileFormat = Field(...,description="format of the file")
    fileExtension: str = Field(..., description="File extension")
    filePath: str = Field(..., description="Path to where the file is uploaded")

class BaseAudio(BaseMedia):
    gainComp: GainCompModel = Field(...,description="class of needed values for gain compression")
    voiceEnh: VoiceEnhModel = Field(...,description="class of needed values for voice enhancement")
    denDel: DenoiseDelayModel  = Field(...,description="class of needed values for denoise and delay")
    phoneLike: PhoneModel = Field(...,description="class of needed values for phone like filter")
    carLike: CarLikeModel = Field(...,description="class of needed values for car like filter")

class BaseVideo(BaseAudio):
    grayScale: GrayScaleModel = Field(...,description="class of needed values for gray scale filter")
    colorInvert: ColorInvertModel = Field(...,description="class of needed values for color invert filter")
    frameTarget: FrameIntpModel = Field(...,description="class of needed values for frame interpolation filter")
    upscalingTarget: UpScalingModel = Field(...,description="class of needed values for upscaling")

# Declaring endpoints
app = FastAPI()
app.include_router(api.api_router)






