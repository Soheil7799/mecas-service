from filters.audio import *
from filters.video import *
from filters import utilies
from fastapi import APIRouter
import os
from formatings.file import  BaseVideo
router = APIRouter()
INPUTPATH = "./files/input"
TEMPPATH = "./files/temp"
OUTPUTPATH = "./files/output"

# To get only the configs needed for the filters and application
@router.post("/application")
async def configure_filters(req: BaseVideo):
    file_name = req.fileName
    # emptying temp and output directories for clean application
    # you can make a function out of this "remover code"
    directory_path = TEMPPATH
    files = os.listdir(directory_path)
    if not files:
        print({"message": "no file detected in temp"})
    for file in files:
        file_path = f"{directory_path}/{file}"
        os.remove(file_path)
    ####
    directory_path = OUTPUTPATH
    files = os.listdir(directory_path)
    if not files:
        print({"message": "no file detected in output"})
    for file in files:
        file_path = f"{directory_path}/{file}"
        os.remove(file_path)
    ####
    # calling the seperator function
    input_base, _ = os.path.splitext(file_name)
    temp_audio ,temp_video =  utilies.extract_audio(file_name, input_base)


    # calling the desired filters
    if req.gainComp.enabled:
        print("calling gain compression")
    if req.voiceEnh.enabled:
        print("calling voice enhancement")
    if req.denDel.enabled:
        print("calling denoise and delay")
    if req.phoneLike.enabled:
        print("calling phone like")
    if req.carLike.enabled:
        print("calling car like")
    if req.grayScale.enabled:
        print("calling gray scale")
    if req.colorInvert.enabled:
        print("calling color invert")
    if req.frameTarget.enabled:
        print("calling frame interpolation")
    if req.upscalingTarget.enabled:
        print("calling upscaling")

    # calling the merger function
    utilies.merge(temp_audio,temp_video,file_name)


    return {req.grayScale.enabled}