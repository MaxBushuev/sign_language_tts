import streamlit as st
from modules.media_processor import MediaProcessor
from modules.model_handler import ModelHandler
from modules.text_to_speech import TextToSpeech
from config import MODEL_PATH, ADAPTER_PATH, STATIC_FOLDER

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
Upload your ASL video file and see the magic unfold!

**Note**: For best results, ensure that the video is clear and well-lit, with visible signing.

---

""")

# Streamlit App Layout
col1, col2 = st.columns(2)

with col1:
    st.header("Upload or Select a Video")
    uploaded_file = st.file_uploader("Choose a video or image for processing", type=["mp4", "jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.video(uploaded_file)

with col2:
    st.header("Use Example Video")
    example_video = st.selectbox("Select an example video", 
                                 ["None", "example_1", "example_2", "example_3"])

    if example_video == "example_1":
        st.video("examples/3EjKvwck6ss_0-1-rgb_front.mp4")
    elif example_video == "example_2":
        st.video("examples/bb1Z5dw4N-s_7-8-rgb_front.mp4")
    elif example_video == "example_3":
        st.video("examples/Eh2AVkAQsxI_2-3-rgb_front.mp4")

    # Add the button to start processing after choosing the example
    use_example_button = st.button("Use this Example")

# Block for displaying results below the video section
st.header("Results")
if uploaded_file is not None or (example_video != "None" and use_example_button):
    media_processor = MediaProcessor(STATIC_FOLDER)
    model_handler = ModelHandler(MODEL_PATH, ADAPTER_PATH)
    text_to_speech = TextToSpeech(STATIC_FOLDER)

    try:
        # Show spinner while processing
        with st.spinner("Generating translation..."):
            if uploaded_file is not None:
                file_path, file_type = media_processor.save_uploaded_file(uploaded_file)
            elif example_video != "None" and use_example_button:
                if example_video == "example_1":
                    file_path = "examples/3EjKvwck6ss_0-1-rgb_front.mp4"
                elif example_video == "example_2":
                    file_path = "examples/bb1Z5dw4N-s_7-8-rgb_front.mp4"
                elif example_video == "example_3":
                    file_path = "examples/Eh2AVkAQsxI_2-3-rgb_front.mp4"

            # Process the media file and display the result
            media_path, media_type = media_processor.get_media_path_and_type(file_path)
            if media_path:
                result = model_handler.process_media(media_path, media_type).split("Assistant:")[-1]

                # Create two columns for text and audio
                col1, col2 = st.columns(2)

                # Display generated text in the first column
                with col1:
                    st.subheader("Generated Text")
                    st.markdown(result, unsafe_allow_html=True)

                # Generate audio immediately and provide download option in the second column
                with col2:
                    text_to_speech.convert_and_save(result)
                    audio_bytes = text_to_speech.get_audio_bytes()

                    if audio_bytes:
                        st.audio(audio_bytes, start_time=0)

                        # Allow user to download the audio file
                        st.download_button(
                            label="Download Audio",
                            data=audio_bytes,
                            file_name="translated_audio.mp3",
                            mime="audio/mp3"
                        )
                    else:
                        st.error("Audio file not found.")
            else:
                st.error("Media file not found.")
    except ValueError as e:
        st.error(str(e))
else:
    st.info("Upload a file or select a video example to see results here.")
