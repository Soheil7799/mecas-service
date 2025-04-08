from enum import IntEnum
from fastapi import FastAPI
from typing import List, Optional
from pydantic import  BaseModel, Field
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
# To get the video for streaming
@app.get("/{video_id}")
async def analyze_file(video_id: str):
    # TODO : make the processed video stream on webpage
    return ""
# To upload a video into server
@app.post("", status_code=201)
async def upload_video():
    #TODO : get a video/audio file from user
    return ""
# To delete a previously uploaded file
@app.delete("/{video_id}")
async def delete_video(video_id: str):
    #TODO : delete the uploaded file
    return ""
# To get only the configs needed for the filters to apply
@app.post("/{video_id}/configure")
async def configure_filters(video_id: str):
    #TODO : make the commands strings here for videos
    #TODO : list the appropriate functions for audio
    return ""
# to apply the configured filters
@app.post("/{video_id}/apply")
async def apply_filters(video_id: str):
    #TODO : apply the video and audio filters
    return ""

