import os, subprocess

def merge(audio_file , video_file , file_name):
    output_video = f"./files/output/{file_name}"
    command = [
        "ffmpeg",
        "-i", video_file,
        "-i", audio_file,
        "-c:v", "copy",  # Copy video without re-encoding
        "-c:a", "aac",  # Use AAC for audio in final file
        output_video
    ]
    result = subprocess.run(command)
    return

def extract_audio(input_file , input_base):
    """
    :param input_base: base file name without extension
    :param input_file: input file name
    :return: audio file path , video file path
    """
    input_path = f"./files/input/{input_file}"
    output_audio = f"./files/temp/{input_base}.wav"
    output_video = f"./files/temp/{input_file}"
    command = [
        "ffmpeg",
        "-i", input_path,  # Input file
        "-vn",  # No video (extract audio only)
        "-acodec", "pcm_s16le",  # Set codec to WAV format (PCM 16-bit)
        output_audio
    ]
    result = subprocess.run(command)
    print(f"audio separation was {result}")
    command = [
        "mv",
        input_path,
        output_video
    ]
    result = subprocess.run(command)
    print(f"moving video was {result}")
    return output_audio , output_video