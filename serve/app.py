import streamlit as st
from modules.media_processor import MediaProcessor
from modules.model_handler import ModelHandler
from modules.text_to_speech import TextToSpeech
from config import MODEL_PATH, ADAPTER_PATH, STATIC_FOLDER

import streamlit as st
st.set_page_config(layout="wide")  # Set the layout to wide mode
# Project Description
st.title("ASL to English Speech Converter")
st.markdown("""
Welcome to the ASL to English Speech Converter! This innovative tool is designed to bridge the communication gap by translating videos in American Sign Language (ASL) into spoken English.

### How It Works:
1. **Upload a Video**: Simply upload a video file where the communication is in American Sign Language.
2. **Process the Video**: Our advanced AI model analyzes the video to understand and translate the ASL gestures into English text.
3. **Listen to the Translation**: The translated English text is then converted into speech, allowing you to listen to the message as if it were spoken in English.

### Why Use This Tool?
- **Accessibility**: Enhance accessibility for individuals who communicate through ASL by providing them with a voice in English.
- **Communication**: Facilitate better communication in diverse settings such as educational institutions, workplaces, and social interactions.
- **Innovation**: Experience the blend of cutting-edge AI technology with practical language translation solutions.

### Get Started:
Please use the sidebar to upload your ASL video file and see the magic unfold!

**Note**: For best results, ensure that the video is clear and well-lit, with visible signing.

---

""")

# Streamlit App Layout


st.sidebar.title("Upload Media")
st.sidebar.write("Upload a video or image for processing")

media_processor = MediaProcessor(STATIC_FOLDER)
model_handler = ModelHandler(MODEL_PATH, ADAPTER_PATH)
text_to_speech = TextToSpeech(STATIC_FOLDER)

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["mp4", "jpg", "jpeg", "png"])

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.header("Examples")
    st.video("examples/_2FBDaOPYig_1-3-rgb_front.mp4")
    st.video("examples/_2FBDaOPYig_1-5-rgb_front.mp4")
    st.video("examples/_2FBDaOPYig_2-3-rgb_front.mp4")

with col2:
    st.header("Results")
    if uploaded_file is not None:
        try:
            file_path, file_type = media_processor.save_uploaded_file(uploaded_file)
            if file_type.startswith("video/"):
                st.video(file_path)
            elif file_type.startswith("image/"):
                st.image(file_path, width=640)

            # Process the media file and display the result
            media_path, media_type = media_processor.get_media_path_and_type()
            if media_path:
                result = model_handler.process_media(media_path, media_type)
                st.subheader("Generated Text")
                st.markdown(result, unsafe_allow_html=True)

                if st.button("Speak"):
                    text_to_speech.convert_and_save(result)
                    audio_bytes = text_to_speech.get_audio_bytes()
                    if audio_bytes:
                        st.audio(audio_bytes, format='audio/ogg', start_time=0)
                    else:
                        st.error("Audio file not found.")
            else:
                st.error("Media file not found.")
        except ValueError as e:
            st.error(str(e))
    else:
        st.info("Upload a file to see results here.")
