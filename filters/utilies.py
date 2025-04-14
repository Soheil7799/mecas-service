import os
import subprocess
import shutil


def merge(audio_file, video_file, file_name):
    """
    Merge audio and video files into a single output file
    """
    # Ensure the output directory exists
    os.makedirs("./files/output", exist_ok=True)

    output_video = f"./files/output/{file_name}"

    # Check if input files exist
    if not os.path.exists(audio_file):
        print(f"Error: Audio file {audio_file} does not exist")
        return False

    if not os.path.exists(video_file):
        print(f"Error: Video file {video_file} does not exist")
        return False

    # Merge the files
    command = [
        "ffmpeg",
        "-i", video_file,
        "-i", audio_file,
        "-c:v", "copy",
        "-c:a", "aac",
        # using aac instead of copy because i dont know if the final output will support wav format as audio
        "-y",  # Overwrite output file if it exists
        output_video
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error merging files: {result.stderr}")
            return False

        # Verify output file exists
        if not os.path.exists(output_video):
            print("Error: Output file was not created")
            return False

        return True
    except Exception as e:
        print(f"Exception during merge: {str(e)}")
        return False


def extract_audio(input_file, input_base):
    """
    Extract audio from input video file and copy video to temp directory

    :param input_base: base file name without extension
    :param input_file: input file name
    :return: audio file path, video file path
    """
    # Ensure directories exist
    os.makedirs("./files/input", exist_ok=True)
    os.makedirs("./files/temp", exist_ok=True)

    # Build full paths
    input_path = f"./files/input/{input_file}"
    output_audio = f"./files/temp/{input_base}.wav"
    output_video = f"./files/temp/{input_file}"

    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} does not exist")
        return None, None

    # Extract audio
    command = [
        "ffmpeg",
        "-i", input_path,  # Input file
        "-vn",  # No video (extract audio only)
        "-acodec", "pcm_s16le",  # Set codec to WAV format (PCM 16-bit)
        "-y",  # Overwrite output file if it exists
        output_audio
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(f"Audio separation result: {result.returncode}")
        if result.returncode != 0:
            print(f"Audio extraction error: {result.stderr}")
            return None, None
    except Exception as e:
        print(f"Exception during audio extraction: {str(e)}")
        return None, None

    # Copy video file to temp directory instead of moving it
    try:
        shutil.copy2(input_path, output_video)
        print(f"Video copied to {output_video}")

        # Verify files exist
        if not os.path.exists(output_audio):
            print(f"Error: Output audio file {output_audio} was not created")
            return None, None

        if not os.path.exists(output_video):
            print(f"Error: Output video file {output_video} was not created")
            return None, None

        return output_audio, output_video
    except Exception as e:
        print(f"Exception during video copy: {str(e)}")
        return None, None