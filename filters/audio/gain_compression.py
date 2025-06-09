import numpy as np
import scipy.io.wavfile as wav
import os
import shutil

def db_to_linear(db_value):
    """Convert decibels to linear scale"""
    return 10 ** (db_value / 20.0)

def cubic_hermite_spline(t, p0, p1, m0, m1):
    """Cubic hermite spline interpolation"""
    x1 = 2*t**3 - 3*t**2 + 1
    x2 = t**3 - 2*t**2 + t 
    x3 = -2*t**3 + 3*t**2 
    x4 = t**3 - t**2
    pt = (x1 * p0) + (x2 * m0) + (x3 * p1) + (x4 * m1)
    return pt

def analyze_audio_properties(input_file):
    """Analyze audio file and return its properties"""
    try:
        sample_rate, audio_data = wav.read(input_file)
        
        print(f"\n=== AUDIO ANALYSIS ===")
        print(f"File: {input_file}")
        print(f"Sample rate: {sample_rate} Hz")
        print(f"Data type: {audio_data.dtype}")
        print(f"Shape: {audio_data.shape}")
        
        # Determine format
        if len(audio_data.shape) == 1:
            channels = 1
            samples = len(audio_data)
            print(f"Format: MONO (1 channel)")
        else:
            samples, channels = audio_data.shape
            print(f"Format: MULTI-CHANNEL ({channels} channels)")
            
            # Identify common channel layouts
            if channels == 2:
                print("Layout: STEREO (L/R)")
            elif channels == 4:
                print("Layout: QUADRAPHONIC or 4.0 SURROUND")
            elif channels == 6:
                print("Layout: 5.1 SURROUND")
            elif channels == 8:
                print("Layout: 7.1 SURROUND")
        
        print(f"Duration: {samples / sample_rate:.2f} seconds")
        print(f"Total samples: {samples}")
        
        return True
        
    except Exception as e:
        print(f"Error analyzing audio: {e}")
        return False

def apply_universal_gain_compression(input_file, output_file, compressor_threshold_db=-60, limiter_threshold_db=-30, compressor_ratio=4, limiter_ratio=10):
    """
    Universal gain compression that works with ANY audio format:
    - Mono, Stereo, Surround (4.0, 5.1, 7.1, etc.)
    - Any sample rate
    - Any bit depth
    """
    
    print(f"\n=== UNIVERSAL GAIN COMPRESSION ===")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Compressor threshold: {compressor_threshold_db} dB")
    print(f"Limiter threshold: {limiter_threshold_db} dB")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"ERROR: Input file does not exist: {input_file}")
        return False
    
    # Analyze the audio first
    if not analyze_audio_properties(input_file):
        return False
    
    try:
        # Read audio file
        sample_rate, audio_data = wav.read(input_file)
        original_dtype = audio_data.dtype
        original_shape = audio_data.shape
        
        # CREATE BACKUP
        backup_file = input_file.replace('.wav', '_backup_original.wav')
        try:
            if not os.path.exists(backup_file):
                shutil.copy2(input_file, backup_file)
                print(f"✅ Backup created: {backup_file}")
        except Exception as e:
            print(f"⚠️ Warning: Could not create backup: {e}")
        
        # Convert to float for processing
        if audio_data.dtype != np.float64:
            scale = np.iinfo(original_dtype).max + 1.0
            audio_float = audio_data.astype(np.float64) / scale
        else:
            audio_float = audio_data.copy()
        
        # Handle different audio formats uniformly
        if len(audio_float.shape) == 1:
            # Mono audio: reshape to [samples, 1] for uniform processing
            audio_float = audio_float.reshape(-1, 1)
            was_mono = True
        else:
            was_mono = False
        
        samples, channels = audio_float.shape
        print(f"Processing: {samples} samples, {channels} channels")
        
        # Convert thresholds to linear scale
        compressor_threshold = db_to_linear(compressor_threshold_db)
        limiter_threshold = db_to_linear(limiter_threshold_db)
        
        print(f"Compressor threshold (linear): {compressor_threshold:.6f}")
        print(f"Limiter threshold (linear): {limiter_threshold:.6f}")
        
        # Process audio using vectorized operations (much faster!)
        processed_audio = np.copy(audio_float)
        
        # Get absolute values and signs for each channel
        signs = np.sign(audio_float)
        abs_audio = np.abs(audio_float)
        
        # Count samples that will be affected
        samples_above_compressor = np.sum(abs_audio > compressor_threshold)
        samples_above_limiter = np.sum(abs_audio > limiter_threshold)
        
        print(f"Samples above compressor threshold: {samples_above_compressor} ({100*samples_above_compressor/(samples*channels):.2f}%)")
        print(f"Samples above limiter threshold: {samples_above_limiter} ({100*samples_above_limiter/(samples*channels):.2f}%)")
        
        if samples_above_compressor == 0:
            print("⚠️ WARNING: No samples above compressor threshold. Audio may be too quiet for compression.")
        
        # Apply compression using vectorized operations
        print("Applying compression...")
        
        # 1. Apply limiter (hard clipping)
        limiter_mask = abs_audio >= limiter_threshold
        abs_audio[limiter_mask] = limiter_threshold
        
        # 2. Apply compressor (smooth compression between thresholds)
        compressor_mask = (abs_audio > compressor_threshold) & (abs_audio < limiter_threshold)
        
        if np.any(compressor_mask):
            # Calculate compression curve for samples in compression range
            t_values = (abs_audio[compressor_mask] - compressor_threshold) / (limiter_threshold - compressor_threshold)
            
            # Apply cubic hermite spline for smooth compression
            compressed_values = np.array([
                cubic_hermite_spline(t, compressor_threshold, limiter_threshold, -1, 0)
                for t in t_values
            ])
            
            # Ensure compressed magnitudes are not negative
            compressed_values = np.maximum(0, compressed_values)
            
            abs_audio[compressor_mask] = compressed_values
        
        # Restore signs
        processed_audio = signs * abs_audio
        
        # --- BEGIN DEBUG PRINT ---
        # Check max absolute value in the float processed_audio before type conversion
        max_abs_float_val = np.max(np.abs(processed_audio))
        print(f"DEBUG: Max abs value in processed_audio (float): {max_abs_float_val:.6f}")
        print(f"DEBUG: Limiter threshold (float): {limiter_threshold:.6f}")
        if max_abs_float_val > limiter_threshold:
            print(f"DEBUG: WARNING! Processed float audio EXCEEDS limiter threshold by {max_abs_float_val - limiter_threshold:.6e}")
        # --- END DEBUG PRINT ---
        
        # Convert back to original format
        if was_mono:
            # Convert back to mono (1D array)
            processed_audio = processed_audio.reshape(-1)
        
        # Convert back to original data type
        if original_dtype != np.float64:
            processed_audio = (processed_audio * scale).astype(original_dtype)
        else:
            processed_audio = processed_audio.astype(original_dtype)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Write processed audio
        wav.write(output_file, sample_rate, processed_audio)
        
        # Verify output file was created
        if os.path.exists(output_file):
            print(f"✅ Compression completed successfully!")
            print(f"📁 Original: {input_file}")
            print(f"💾 Backup: {backup_file}")
            print(f"🎵 Processed: {output_file}")
            
            # Compare file sizes
            original_size = os.path.getsize(input_file)
            processed_size = os.path.getsize(output_file)
            print(f"📊 File sizes - Original: {original_size} bytes, Processed: {processed_size} bytes")
            
            return True
        else:
            print(f"❌ ERROR: Output file was not created")
            return False
            
    except Exception as e:
        print(f"❌ ERROR in gain compression: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_compression_on_file(input_file, compressor_threshold_db=-25, limiter_threshold_db=-12):
    """Test compression on a specific file"""
    
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return False
    
    # Generate output filename
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_compressed{ext}"
    
    # Apply compression
    success = apply_universal_gain_compression(
        input_file, 
        output_file, 
        compressor_threshold_db, 
        limiter_threshold_db
    )
    
    if success:
        print(f"\n✅ Test completed! Compare these files:")
        print(f"Original: {input_file}")
        print(f"Compressed: {output_file}")
        
        # You can now use these files with the visualizer
        print(f"\nTo visualize the results, use:")
        print(f"visualize_audio_compression('{input_file}', '{output_file}')")
    
    return success

# if __name__ == "__main__":
#     # Example usage - update this path to your audio file
#     test_file = "SampleVideo_1280x720_5mb_backup.wav"
    
#     print("Universal Gain Compression Test")
#     print("=" * 50)
    
#     # Test with your file
#     test_compression_on_file(test_file, -60, -30)