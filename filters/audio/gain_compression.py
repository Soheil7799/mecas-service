import numpy as np
import scipy.io.wavfile as wav
import logging
# to convert decibels
def db_to_linear(db_value):
    return 10 ** (db_value / 20.0)

def apply_gain_compression(input_file = "../../files/input/input.wav", output_file="../../files/temp/output.wav", compressor_threshold_db=-1, limiter_threshold_db=0 , compressor_ratio=4 , limiter_ratio=10):

    compressor_threshold = db_to_linear(compressor_threshold_db)
    limiter_threshold = db_to_linear(limiter_threshold_db)

    # Read the audio file
    sample_rate, sample_original = wav.read(input_file)
    # changing the format numpy int16
    sample_int = sample_original.astype(np.int16) / 32767

    # we take the signs and make it absolute so in the "if" sections it is easier for conditions
    signs = np.sign(sample_int)
    abs_sample = np.abs(sample_int)

    # we find the values between the two thresholds to compress them (default ratio is 4 to 1 )
    mask_compression = (abs_sample > compressor_threshold ) & (abs_sample < limiter_threshold )
    # like a loop, if any need compressing, it we
    if np.any(mask_compression):
        abs_sample[mask_compression] = compressor_threshold + (abs_sample[mask_compression] - compressor_threshold) / compressor_ratio

    # we find the values surpassing the limiter thresholds to cut/compress them (default ratio is 10 to 1 )
    # any ratio above 10 is supposed to act like limiter
    mask_limit = abs_sample > limiter_threshold
    # like a loop, if any need compressing, it will do it
    if np.any(mask_limit):
        if limiter_ratio == 0 :
            abs_sample[mask_limit] = limiter_threshold
        else:
            abs_sample[mask_limit] = limiter_threshold + (abs_sample[mask_limit] - limiter_threshold) / limiter_ratio

    final_sample = signs * abs_sample
    final_sample_int = (final_sample * 32767.0).astype(np.int16)
    wav.write(output_file,sample_rate,final_sample_int)

    print (f"{sample_int}\n{final_sample_int}\n{sample_int - final_sample_int}")
    logging.info("Gain Compressed file has been made")

apply_gain_compression()