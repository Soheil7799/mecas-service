from fastapi import APIRouter, File, UploadFile, HTTPException
import os
import shutil

router = APIRouter()
FILEPATH = "./files/input"
TEMPPATH = "./files/temp"
OUTPUTPATH = "./files/output"


# Create directories if they don't exist
def ensure_directories():
    os.makedirs(FILEPATH, exist_ok=True)
    os.makedirs(TEMPPATH, exist_ok=True)
    os.makedirs(OUTPUTPATH, exist_ok=True)


def cleanup_directories():
    """
    Cleanup temporary and output directories
    Remove all files in these directories
    """
    cleanup_dirs = [FILEPATH, TEMPPATH, OUTPUTPATH]

    for directory in cleanup_dirs:
        try:
            # Ensure directory exists
            os.makedirs(directory, exist_ok=True)

            # List and remove all files
            files = os.listdir(directory)
            for file in files:
                file_path = os.path.join(directory, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        except Exception as e:
            print(f"Error cleaning directory {directory}: {e}")


# To upload a video into server
@router.post("/uploadfile/", status_code=201)
async def upload_video(video_file: UploadFile = File(...)):
    # Ensure directories exist and are cleaned
    ensure_directories()
    cleanup_directories()

    # Get file type and build path
    file_path = os.path.join(FILEPATH, video_file.filename)

    # Save the file with correct error handling
    try:
        # Using a context manager to ensure the file is closed properly
        with open(file_path, "wb") as buffer:
            # Use shutil to handle larger files efficiently
            shutil.copyfileobj(video_file.file, buffer)

        # Verify the file exists after saving
        if os.path.exists(file_path):
            return {"filename": video_file.filename}
        else:
            raise HTTPException(status_code=500, detail="File was not saved properly")
    except Exception as e:
        # Log the error and return an informative message
        print(f"Error saving file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    finally:
        # Make sure the uploaded file is closed
        video_file.file.close()


# To delete a previously uploaded file
@router.delete("/{file_name}")
async def delete_video(file_name: str):
    file_path = os.path.join(FILEPATH, file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"File {file_name} deleted successfully"}
    else:
        return {"message": f"File {file_name} not found"}


@router.delete("/")
async def delete_content():
    ensure_directories()
    cleanup_directories()
    return {"message": "All uploaded files deleted"}