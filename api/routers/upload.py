from fastapi import APIRouter, File, UploadFile
router = APIRouter()
FILEPATH = "./files/input"
# To upload a video into server
@router.post("/uploadfile/", status_code=201)
async def upload_video(video_file: UploadFile = File(...)):
    #TODO : get a video/audio file from user
    file_type = video_file.content_type
    file_path = f"{FILEPATH}/{video_file.filename}"
    with open(file_path,"wb+") as file_object:
        file_object.write(video_file.file.read())
    return {"filename" : video_file.content_type}

# To delete a previously uploaded file
@router.delete("/{video_id}")
async def delete_video(video_id: str):
    #TODO : delete the uploaded file
    return ""