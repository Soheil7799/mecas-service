from fastapi import APIRouter
router = APIRouter()

# To upload a video into server
@router.post("/", status_code=201)
async def upload_video():
    #TODO : get a video/audio file from user
    return ""

# To delete a previously uploaded file
@router.delete("/{video_id}")
async def delete_video(video_id: str):
    #TODO : delete the uploaded file
    return ""