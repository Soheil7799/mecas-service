import numpy as np
import scipy.io.wavfile as wav
# to convert decibels
def db_to_linear(db_value):
    return 10 ** (db_value / 20.0)

def apply_gain_compression(input_file = "input.wav", output_file="output.wav", compressor_threshold_db=-3, limiter_threshold_db=1):

    compressor_threshold = db_to_linear(compressor_threshold_db)
    limiter_threshold = db_to_linear(limiter_threshold_db)

    # Read the audio file
    sample_rate, sample_original = wav.read(input_file)
    # changing the format numpy int16
    sample_int = sample_original.astype(np.int16)
    
    print (f"{sample_int} \n {sample_original}")


apply_gain_compression()