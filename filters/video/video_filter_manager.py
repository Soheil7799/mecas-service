import subprocess
import os
import shutil


def remove_temp_file(file):
    if os.path.exists(file):
        try:
            os.remove(file)
            return True
        except Exception as e:
            print(f"Error removing file {file}: {e}")
            return False
    return True


def ffmpeg_command_runner(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg command failed: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running FFmpeg command: {e}")
        return False


def make_temp_file(input_file):
    """Create a temporary copy of the file for processing"""
    temp_dir = "./files/temp"
    os.makedirs(temp_dir, exist_ok=True)

    input_path = os.path.join(temp_dir, input_file)
    temp_output = f"./temp_{input_file}"

    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} does not exist")
        return None, None

    try:
        # Copy instead of moving the file
        shutil.copy2(input_path, temp_output)
        print(f"Copied {input_path} to {temp_output}")
        return temp_output, input_path
    except Exception as e:
        print(f"Error in make_temp_file: {e}")
        return None, None


def apply_grayscale(input_file):
    temp_file, output_path = make_temp_file(input_file)
    if not temp_file or not output_path:
        return False

    command = [
        "ffmpeg", "-i", temp_file,
        "-vf", "format=gray",
        "-c:a", "copy",
        "-y",  # Overwrite output file if it exists
        output_path
    ]

    success = ffmpeg_command_runner(command)
    remove_temp_file(temp_file)
    return success


def apply_color_inversion(input_file):
    temp_file, output_path = make_temp_file(input_file)
    if not temp_file or not output_path:
        return False

    command = [
        "ffmpeg", "-i", temp_file,
        "-vf", "negate",
        "-c:a", "copy",
        "-y",  # Overwrite output file if it exists
        output_path
    ]

    success = ffmpeg_command_runner(command)
    remove_temp_file(temp_file)
    return success


def apply_frame_interpolation(input_file, target_fps):
    temp_file, output_path = make_temp_file(input_file)
    if not temp_file or not output_path:
        return False

    command = [
        "ffmpeg", "-i", temp_file,
        "-vf", f"minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps={target_fps}'",
        "-c:a", "copy",
        "-y",  # Overwrite output file if it exists
        output_path
    ]

    success = ffmpeg_command_runner(command)
    remove_temp_file(temp_file)
    return success


def apply_upscaling(input_file, target_width, target_height):
    temp_file, output_path = make_temp_file(input_file)
    if not temp_file or not output_path:
        return False

    command = [
        "ffmpeg", "-i", temp_file,
        "-vf", f"scale={target_width}:{target_height}",
        "-c:a", "copy",
        "-y",  # Overwrite output file if it exists
        output_path
    ]

    success = ffmpeg_command_runner(command)
    remove_temp_file(temp_file)
    return success