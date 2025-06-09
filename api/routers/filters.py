import filters.video.video_filter_manager as vfm
from filters import utilies
from fastapi import APIRouter, HTTPException
import os
from formatings.file import BaseVideo

router = APIRouter()
INPUTPATH = "./files/input"
TEMPPATH = "./files/temp"
OUTPUTPATH = "./files/output"


# Ensure directories exist
def ensure_directories():
	os.makedirs(INPUTPATH, exist_ok=True)
	os.makedirs(TEMPPATH, exist_ok=True)
	os.makedirs(OUTPUTPATH, exist_ok=True)


# To get only the configs needed for the filters and application
@router.post("/application")
async def configure_filters(req: BaseVideo):
	# Ensure all directories exist
	ensure_directories()

	file_name = req.fileName

	# Check if input file exists
	input_file_path = os.path.join(INPUTPATH, file_name)
	if not os.path.exists(input_file_path):
		raise HTTPException(status_code=404, detail=f"Input file {file_name} not found in {INPUTPATH}")

	# Clean temporary directories
	for directory_path in [TEMPPATH, OUTPUTPATH]:
		try:
			files = os.listdir(directory_path)
			for file in files:
				file_path = os.path.join(directory_path, file)
				if os.path.isfile(file_path):
					os.remove(file_path)
		except Exception as e:
			print(f"Error cleaning directory {directory_path}: {e}")

	# Separate audio and video
	input_base, _ = os.path.splitext(file_name)
	temp_audio, temp_video = utilies.extract_audio(file_name, input_base)

	if not temp_audio or not temp_video:
		raise HTTPException(status_code=500, detail="Failed to extract audio and video")

	# Apply audio filters
	if req.gainComp.enabled:
		print("Calling gain compression")
	from filters.audio.gain_compression import apply_universal_gain_compression

	success = apply_universal_gain_compression(
		temp_audio,  # input file path
		temp_audio,  # output file path (overwrite)
		req.gainComp.compressorThreshold,
		req.gainComp.limitThreshold,
	)
	if not success:
		raise HTTPException(status_code=500, detail="Gain compression failed")

	if req.voiceEnh.enabled:
		print("Calling voice enhancement")
		# Implement voice enhancement

	if req.denDel.enabled:
		print("Calling denoise and delay")
		# Implement denoise and delay

	if req.phoneLike.enabled:
		print("Calling phone like")
		# Implement phone-like filter

	if req.carLike.enabled:
		print("Calling car like")
		# Implement car-like filter

	# Apply video filters
	if req.grayScale.enabled:
		print("Calling gray scale")
		success = vfm.apply_grayscale(file_name)
		if not success:
			raise HTTPException(status_code=500, detail="Failed to apply grayscale filter")

	if req.colorInvert.enabled:
		print("Calling color invert")
		success = vfm.apply_color_inversion(file_name)
		if not success:
			raise HTTPException(status_code=500, detail="Failed to apply color inversion filter")

	if req.frameTarget.enabled:
		print("Calling frame interpolation")
		success = vfm.apply_frame_interpolation(file_name, req.frameTarget.targetFPS)
		if not success:
			raise HTTPException(status_code=500, detail="Failed to apply frame interpolation")

	if req.upscalingTarget.enabled:
		print("Calling upscaling")
		success = vfm.apply_upscaling(file_name, req.upscalingTarget.width, req.upscalingTarget.height)
		if not success:
			raise HTTPException(status_code=500, detail="Failed to apply upscaling")

	# Merge audio and video
	success = utilies.merge(temp_audio, temp_video, file_name)
	if not success:
		raise HTTPException(status_code=500, detail="Failed to merge audio and video")

	return {"message": "Filters applied successfully"}
