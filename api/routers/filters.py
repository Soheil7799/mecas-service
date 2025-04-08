from fastapi import APIRouter
router = APIRouter()


# To get only the configs needed for the filters to apply
@router.post("/{video_id}/configure")
async def configure_filters(video_id: str):
    #TODO : make the commands strings here for videos
    #TODO : list the appropriate functions for audio
    return ""
# to apply the configured filters
@router.post("/{video_id}/apply")
async def apply_filters(video_id: str):
    #TODO : apply the video and audio filters
    return ""