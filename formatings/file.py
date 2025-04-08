from enum import IntEnum
from .audio import *
from .video import *

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