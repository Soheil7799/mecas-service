from fastapi import APIRouter
router = APIRouter()

# To get the video for streaming
@router.get("/{video_id}")
async def stream(video_id: str):
    # TODO : make the processed video stream on webpage
    return ""