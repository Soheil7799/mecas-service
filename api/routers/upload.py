from fastapi import APIRouter, File, UploadFile
import os
router = APIRouter()
FILEPATH = "./files/input"

# To upload a video into server
@router.post("/uploadfile/", status_code=201)
async def upload_video(video_file: UploadFile = File(...)):
    #TODO : get a video/audio file from user
    files = os.listdir(".")
    if not files == []:
        return {"message" : "first delete previously uploaded files"}
    file_type = video_file.content_type
    file_path = f"{FILEPATH}/{video_file.filename}"
    with open(file_path,"wb+") as file_object:
        file_object.write(video_file.file.read())
    return {"filename" : video_file.content_type}

# To delete a previously uploaded file
@router.delete("/{file_name}")
async def delete_video(file_name: str):
    #TODO : delete the uploaded file
    file_path = f"{FILEPATH}/{file_name}"
    # open(file_path , "w").close()
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"File {file_name} deleted successfully"}
    else:
        return {"message": f"File {file_name} not found"}

@router.delete("/")
async def delete_content():
    directory_path = FILEPATH
    files = os.listdir(directory_path)
    if not files:
        return {"message" : "no file detected"}
    for file in files:
        file_path = f"{directory_path}/{file}"
        os.remove(file_path)

    return {"message" : "all uploaded files deleted"}