import subprocess
import os
def remove_temp_file(file):
    if os.path.exists(file):
        os.remove(file)


def ffmpeg_command_runner(command: list):
    result = subprocess.run(command)
    return result

def make_temp_file(input_file):
    input_path = f"./files/temp/{input_file}"
    output_path = f"./{input_file}"
    command = [
        "mv",
        input_path,
        output_path
    ]
    subprocess.run(command)
    return output_path , input_path


def apply_grayscale(input_file):
    temp_file , output_path = make_temp_file(input_file)
    # output_path = f"./files/temp/{input_file}"
    command = [
        "ffmpeg", "-i", temp_file,
        "-vf", "format=gray",
        "-c:a", "copy",
        output_path
    ]
    ffmpeg_command_runner(command)
    remove_temp_file(temp_file)


def apply_color_inversion(input_file, ):
    temp_file , output_path = make_temp_file(input_file)

    command = [
        "ffmpeg", "-i", temp_file,
        "-vf", "negate",
        "-c:a", "copy",
        output_path
    ]
    ffmpeg_command_runner(command)
    remove_temp_file(temp_file)



def apply_frame_interpolation(input_file, target_fps):
    temp_file , output_path = make_temp_file(input_file)

    command = [
        "ffmpeg", "-i", temp_file,
        "-vf", f"minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps={target_fps}'",
        "-c:a", "copy",
        output_path
    ]
    ffmpeg_command_runner(command)
    remove_temp_file(temp_file)


def apply_upscaling(input_file, target_width, target_height):
    temp_file , output_path = make_temp_file(input_file)
    command = [
        "ffmpeg", "-i", temp_file,
        "-vf", f"scale={target_width}:{target_height}",
        "-c:a", "copy",
        output_path
    ]
    ffmpeg_command_runner(command)
    remove_temp_file(temp_file)


