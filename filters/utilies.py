import os, subprocess

def merge(audio_file , video_file):
    command = [

    ]
    return

def extract_audio(input_file):
    command = [
        "ffmpeg",
        "-i", input_file,  # Input file
        "-vn",  # No video (extract audio only)
        "-acodec", "pcm_s16le",  # Set codec to WAV format (PCM 16-bit)
        output_audio
    ]
    return