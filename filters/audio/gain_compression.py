import numpy as np
import scipy.io.wavfile as wav

# to convert decibels
def db_to_linear(db_value):
    return 10 ** (db_value / 20.0)

def cubic_hermite_spline(t, p0, p1, m0, m1):
    x1 = 2*t**3 - 3*t**2 + 1
    x2 = t**3 - 2*t**2 + t 
    x3 = -2*t**3 + 3*t**2 
    x4 = t**3 - t**2
    pt = (x1 * p0) + (x2 * m0) + (x3 * p1) + (x4 * m1)
    return pt



def apply_gain_compression(input_file = "../../files/input/input.wav", output_file="../../files/temp/output.wav", compressor_threshold_db=-25, limiter_threshold_db=-12 , compressor_ratio=4 , limiter_ratio=10):

    compressor_threshold = db_to_linear(compressor_threshold_db)
    limiter_threshold = db_to_linear(limiter_threshold_db)

    sample_rate, sample_original = wav.read(input_file)
    print(f"Data type of the audio: {sample_original.dtype}")
    
    original_dtype = sample_original.dtype
    scale = np.iinfo(original_dtype).max + 1.0
    sample_float = sample_original.astype(float) / scale

    signs = np.sign(sample_float)
    abs_sample = np.abs(sample_float)

    converted = np.copy(abs_sample)
    
    # Apply compression algorithm
    for i in range(len(abs_sample)):
        for j in range(len(abs_sample[i])):
            if abs_sample[i][j] >= limiter_threshold:
                converted[i][j] = limiter_threshold
            elif abs_sample[i][j] > compressor_threshold and abs_sample[i][j] < limiter_threshold:
                t = (abs_sample[i][j] - compressor_threshold) / (limiter_threshold - compressor_threshold)
                converted[i][j] = cubic_hermite_spline(t, compressor_threshold, limiter_threshold, 1, 0)
                # converted[i][j] = cubic_hermite_spline(abs_sample[i][j], compressor_threshold, limiter_threshold, 1, 0)
                print(f"is t:{t} = {abs_sample[i][j]} :absolute ?")
        


    # mask_compression = (abs_sample > compressor_threshold ) & (abs_sample < limiter_threshold )

    # if np.any(mask_compression):
    #     abs_sample[mask_compression] = cubic_hermite_spline(mask_compression , compressor_threshold , limiter_threshold, 1, 0)
    
    # mask_limit = abs_sample > limiter_threshold
    # if np.any(mask_limit):
    #     abs_sample[mask_limit] = limiter_threshold

    # Restore signs
    final_sample = signs * converted
    
    # Convert back to original data type for saving
    if np.issubdtype(original_dtype, np.integer):
        final_sample = (final_sample * scale).astype(original_dtype)
    
    # Write the output file
    wav.write(output_file, sample_rate, final_sample)

apply_gain_compression()