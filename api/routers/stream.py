from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import os

router = APIRouter()
OUTPUT = "./files/output"


# based on this we need a generator
# https://fastapi.tiangolo.com/advanced/custom-response/#using-streamingresponse-with-file-like-objects
def iterfile(some_file_path):  # (1)
    with open(some_file_path, mode="rb") as file_like:  # (2)
        yield from file_like  # (3)


MEDIA_TYPES = {
    ".mp4": "video/mp4",
    ".avi": "video/x-msvideo",
    ".mkv": "video/x-matroska",
    ".webm": "video/webm",
    ".mov": "video/quicktime",
    ".wmv": "video/x-ms-wmv",
    ".flv": "video/x-flv",
    ".3gp": "video/3gpp",
    ".m4v": "video/x-m4v",
    ".ts": "video/mp2t",
    ".ogg": "video/ogg",
    ".ogv": "video/ogg",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".aac": "audio/aac",
    ".m4a": "audio/mp4",
}


# To get the video for streaming
@router.get("/stream/")
async def stream():
    # Find the output file
    files = os.listdir(OUTPUT)
    if not files:
        return {"error": "No processed video found"}

    output_path = f"{OUTPUT}/{files[0]}"
    _, ext = os.path.splitext(output_path)
    ext = ext.lower()

    # Set the correct content type based on file extension
    content_type = "application/octet-stream"
    if ext in MEDIA_TYPES:
        content_type = MEDIA_TYPES[ext]

    # Return the streaming response with the correct content type
    return StreamingResponse(
        iterfile(output_path),
        media_type=content_type,
        headers={
            "Accept-Ranges": "bytes",
            "Content-Disposition": f"inline; filename={os.path.basename(output_path)}"
        }
    )