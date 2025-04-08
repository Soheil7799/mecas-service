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