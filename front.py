import streamlit as st
import requests
import os

# Configuration for API endpoints
BASE_URL = "http://localhost:8000"  # Update with your actual backend URL


class FilterConfig:
    def __init__(self):
        # Audio Filters
        self.gain_apply = False
        self.gain_compressor_threshold = -1
        self.limiter_threshold = 0

        self.voice_enhance_apply = False
        self.preemphasis_alpha = 3
        self.high_pass_order = 2

        self.denoise_delay_apply = False
        self.noise_power = -15
        self.delay = 100
        self.delay_gain = 50

        self.phone_like_apply = False
        self.phone_side_gain = 0
        self.phone_filter_order = 1

        self.car_like_apply = False
        self.car_side_gain = 3
        self.car_filter_order = 1

        # Video Filters
        self.gray_scale_apply = False
        self.invert_apply = False
        self.frame_interpolate_apply = False
        self.frame_target_fps = 60
        self.upscale_apply = False
        self.upscale_width = 1280
        self.upscale_height = 720


def reset_session_state():
    """Reset the session state to initial values"""
    st.session_state.uploaded_filename = None
    st.session_state.video_processed = False
    st.session_state.filter_config = FilterConfig()


def main():
    st.title("MECAS Service")

    # Initialize session state if not already done
    if 'uploaded_filename' not in st.session_state:
        st.session_state.uploaded_filename = None

    if 'video_processed' not in st.session_state:
        st.session_state.video_processed = False

    if 'filter_config' not in st.session_state:
        st.session_state.filter_config = FilterConfig()

    # File Upload Section
    uploaded_file = st.file_uploader("Choose or Drag and Drop File",
                                     type=['mp4', 'avi', 'mov'],
                                     help="Limit 200MB per file. Supported formats: MP4, AVI, MOV")

    # File Upload Process
    if uploaded_file is not None:
        # Validate file size (200MB limit)
        if uploaded_file.size > 200 * 1024 * 1024:
            st.error("File size exceeds 200MB limit")
            return

        # Upload file to backend
        files = {'video_file': (uploaded_file.name, uploaded_file, 'multipart/form-data')}
        try:
            st.info("Uploading file...")
            upload_response = requests.post(f"{BASE_URL}/uploadfile/", files=files)

            # Print full response for debugging
            st.write("Upload Response Status Code:", upload_response.status_code)
            st.write("Upload Response Content:", upload_response.text)

            if upload_response.status_code == 201:
                st.session_state.uploaded_filename = uploaded_file.name
                st.success("File uploaded successfully!")
            else:
                st.error(f"Upload failed: {upload_response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Upload error: {e}")

    # Filters Section (only show after file upload)
    if st.session_state.uploaded_filename:
        st.subheader("Audio Filters")
        col1, col2 = st.columns(2)

        with col1:
            # Gain Compressor Filter
            st.session_state.filter_config.gain_apply = st.checkbox("Gain Compressor", key="gain_checkbox")
            if st.session_state.filter_config.gain_apply:
                st.session_state.filter_config.gain_compressor_threshold = st.number_input(
                    "Compressor Threshold (dB)",
                    value=-1,
                    key="gain_compressor_threshold"
                )
                st.session_state.filter_config.limiter_threshold = st.number_input(
                    "Limiter Threshold (dB)",
                    value=0,
                    key="limiter_threshold"
                )

            # Voice Enhancement Filter
            st.session_state.filter_config.voice_enhance_apply = st.checkbox("Voice Enhancement",
                                                                             key="voice_enhance_checkbox")
            if st.session_state.filter_config.voice_enhance_apply:
                st.session_state.filter_config.preemphasis_alpha = st.number_input(
                    "Pre-emphasis Alpha",
                    value=3,
                    key="preemphasis_alpha"
                )
                st.session_state.filter_config.high_pass_order = st.number_input(
                    "High Pass Filter Order",
                    value=2,
                    key="high_pass_order"
                )

        with col2:
            # Denoise + Delay Filter
            st.session_state.filter_config.denoise_delay_apply = st.checkbox("Denoise + Delay",
                                                                             key="denoise_delay_checkbox")
            if st.session_state.filter_config.denoise_delay_apply:
                st.session_state.filter_config.noise_power = st.number_input(
                    "Noise Power (dB)",
                    value=-15,
                    max_value=0,
                    key="noise_power"
                )
                st.session_state.filter_config.delay = st.number_input(
                    "Delay (ms)",
                    value=100,
                    key="delay"
                )
                st.session_state.filter_config.delay_gain = st.number_input(
                    "Delay Gain (%)",
                    value=50,
                    min_value=0,
                    max_value=100,
                    key="delay_gain"
                )

            # Phone-like Filter
            st.session_state.filter_config.phone_like_apply = st.checkbox("Phone-like Filter",
                                                                          key="phone_like_checkbox")
            if st.session_state.filter_config.phone_like_apply:
                st.session_state.filter_config.phone_side_gain = st.number_input(
                    "Side Gain (0:mono, 1:original)",
                    value=0.0,
                    min_value=0.0,
                    max_value=1.0,
                    key="phone_side_gain"
                )
                st.session_state.filter_config.phone_filter_order = st.number_input(
                    "Filter Order",
                    value=1,
                    key="phone_filter_order"
                )

            # Car-like Filter
            st.session_state.filter_config.car_like_apply = st.checkbox("Car-like Filter", key="car_like_checkbox")
            if st.session_state.filter_config.car_like_apply:
                st.session_state.filter_config.car_side_gain = st.number_input(
                    "Side Gain (dB)",
                    value=3,
                    min_value=0,
                    key="car_side_gain"
                )
                st.session_state.filter_config.car_filter_order = st.number_input(
                    "Filter Order",
                    value=1,
                    key="car_filter_order"
                )

        st.subheader("Video Filters")
        col3, col4 = st.columns(2)

        with col3:
            # Grayscale Filter
            st.session_state.filter_config.gray_scale_apply = st.checkbox("Grayscale", key="gray_scale_checkbox")

            # Color Invert Filter
            st.session_state.filter_config.invert_apply = st.checkbox("Color Invert", key="invert_checkbox")

            # Frame Interpolation Filter
            st.session_state.filter_config.frame_interpolate_apply = st.checkbox("Frame Interpolation",
                                                                                 key="frame_interpolate_checkbox")
            if st.session_state.filter_config.frame_interpolate_apply:
                st.session_state.filter_config.frame_target_fps = st.number_input(
                    "Target FPS",
                    value=60,
                    key="frame_target_fps"
                )

        with col4:
            # Upscale Filter
            st.session_state.filter_config.upscale_apply = st.checkbox("Upscale", key="upscale_checkbox")
            if st.session_state.filter_config.upscale_apply:
                st.session_state.filter_config.upscale_width = st.number_input(
                    "Target Width (pixels)",
                    value=1280,
                    key="upscale_width"
                )
                st.session_state.filter_config.upscale_height = st.number_input(
                    "Target Height (pixels)",
                    value=720,
                    key="upscale_height"
                )

        # Apply Filters Button
        if st.button("Apply Filters"):
            try:
                # Prepare filter configuration
                filter_payload = {
                    "fileName": st.session_state.uploaded_filename,
                    "fileFormat": 1,  # VIDEO
                    "fileExtension": os.path.splitext(st.session_state.uploaded_filename)[1],
                    "filePath": "./files/input",

                    # Audio Filters
                    "gainComp": {
                        "enabled": st.session_state.filter_config.gain_apply,
                        "compressorThreshold": st.session_state.filter_config.gain_compressor_threshold,
                        "limitThreshold": st.session_state.filter_config.limiter_threshold
                    },
                    "voiceEnh": {
                        "enabled": st.session_state.filter_config.voice_enhance_apply,
                        "alpha": st.session_state.filter_config.preemphasis_alpha,
                        "highPass": st.session_state.filter_config.high_pass_order
                    },
                    "denDel": {
                        "enabled": st.session_state.filter_config.denoise_delay_apply,
                        "noisePower": st.session_state.filter_config.noise_power,
                        "delay": st.session_state.filter_config.delay,
                        "delayGain": st.session_state.filter_config.delay_gain
                    },
                    "phoneLike": {
                        "enabled": st.session_state.filter_config.phone_like_apply,
                        "sideGain": int(st.session_state.filter_config.phone_side_gain),
                        "order": st.session_state.filter_config.phone_filter_order
                    },
                    "carLike": {
                        "enabled": st.session_state.filter_config.car_like_apply,
                        "sideGain": int(st.session_state.filter_config.car_side_gain),
                        "order": st.session_state.filter_config.car_filter_order
                    },

                    # Video Filters
                    "grayScale": {"enabled": st.session_state.filter_config.gray_scale_apply},
                    "colorInvert": {"enabled": st.session_state.filter_config.invert_apply},
                    "frameTarget": {
                        "enabled": st.session_state.filter_config.frame_interpolate_apply,
                        "targetFPS": st.session_state.filter_config.frame_target_fps
                    },
                    "upscalingTarget": {
                        "enabled": st.session_state.filter_config.upscale_apply,
                        "width": st.session_state.filter_config.upscale_width,
                        "height": st.session_state.filter_config.upscale_height
                    }
                }

                # Send filter application request
                st.info("Applying filters...")
                apply_response = requests.post(f"{BASE_URL}/application", json=filter_payload)

                # Print full response for debugging
                st.write("Apply Response Status Code:", apply_response.status_code)
                st.write("Apply Response Content:", apply_response.text)

                if apply_response.status_code == 200:
                    st.success("Filters applied successfully!")
                    st.session_state.video_processed = True
                else:
                    st.error(f"Filter application failed: {apply_response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Error applying filters: {e}")

    # Video Player Section (only show after filters are applied)
    if st.session_state.video_processed:
        try:
            # Stream the processed video
            st.info("Streaming processed video...")
            stream_response = requests.get(f"{BASE_URL}/stream/")

            # Print full response for debugging
            st.write("Stream Response Status Code:", stream_response.status_code)

            if stream_response.status_code == 200:
                # Save the video temporarily to stream
                with open("processed_video.mp4", "wb") as f:
                    f.write(stream_response.content)

                st.video("processed_video.mp4")
            else:
                st.error("Failed to stream processed video")
                st.write("Response Content:", stream_response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"Streaming error: {e}")

    # Optional: Delete file button
    if st.session_state.uploaded_filename:
        if st.button("Delete File"):
            try:
                # Try deleting with full URL
                delete_response = requests.delete(f"{BASE_URL}/")

                # Print full response for debugging
                st.write("Delete Endpoint:", f"{BASE_URL}/")
                st.write("Delete Response Status Code:", delete_response.status_code)
                st.write("Delete Response Content:", delete_response.text)
                st.write("Delete Response Headers:", delete_response.headers)

                if delete_response.status_code == 200:
                    st.success("File deleted successfully!")
                    # Reset session state
                    reset_session_state()
                    # Force a rerun of the app
                    st.rerun()
                else:
                    # More detailed error information
                    st.error(f"Failed to delete file. Status Code: {delete_response.status_code}")
                    st.error(f"Response Content: {delete_response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Delete failed: {e}")
                # Print exception details
                st.error(f"Exception Type: {type(e).__name__}")
                st.error(f"Exception Details: {str(e)}")


def reset_app():
    """
    Function to reset the entire application state
    Can be called manually if needed
    """
    reset_session_state()


if __name__ == "__main__":
    main()