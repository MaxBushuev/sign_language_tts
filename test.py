import streamlit as st
import os
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText
from gtts import gTTS

# Define constants for paths and model configuration
MODEL_PATH = "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"
ADAPTER_PATH = "models/checkpoint-500"
STATIC_FOLDER = "static"

# Ensure the static folder exists
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

class MediaProcessor:
    """Handles loading and processing of media files."""
    
    def __init__(self, static_folder):
        self.static_folder = static_folder
    
    def save_uploaded_file(self, uploaded_file):
        """Save uploaded file to the static folder."""
        file_type = uploaded_file.type
        if file_type.startswith("video/"):
            filename = "current_media.mp4"
        elif file_type.startswith("image/"):
            filename = "current_media.jpg"
        else:
            raise ValueError("Unsupported file type.")
        
        file_path = os.path.join(self.static_folder, filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path, file_type

    def get_media_path_and_type(self):
        """Determine the media type and path."""
        video_path = os.path.join(self.static_folder, "current_media.mp4")
        image_path = os.path.join(self.static_folder, "current_media.jpg")
        
        if os.path.exists(video_path):
            return video_path, "video"
        elif os.path.exists(image_path):
            return image_path, "image"
        else:
            return None, None

@st.cache_resource
def load_model_and_processor(model_path, adapter_path):
    processor = AutoProcessor.from_pretrained(model_path)
    model = AutoModelForImageTextToText.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
    )
    model.load_adapter(adapter_path)
    return processor, model

class ModelHandler:
    """Handles loading and inference of the model."""
    
    def __init__(self, model_path, adapter_path):
        self.processor, self.model = load_model_and_processor(model_path, adapter_path)

    def process_media(self, media_path, media_type):
        """Process the media file through the model and return the generated text."""
        prompt = f"Translate the {media_type} from american sign language to english."
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": media_type, "path": media_path},
                ]
            },
        ]
        
        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.model.device, dtype=torch.bfloat16)
        
        generated_ids = self.model.generate(**inputs, do_sample=False, max_new_tokens=64)
        generated_texts = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
        )
        
        # Extract only the part that starts with "Assistant:"
        output_text = ""
        for text in generated_texts:
            if "Assistant:" in text:
                output_text = text[text.find("Assistant:"):]
                break
        
        # If the text is longer than 10 words, insert a line break after the 10th word
        words = output_text.split()
        if len(words) > 10:
            output_text = " ".join(words[:10]) + "\n" + " ".join(words[10:])
        
        return output_text


class TextToSpeech:
    """Handles text-to-speech conversion."""
    
    def __init__(self, static_folder):
        self.audio_path = os.path.join(static_folder, "audio.mp3")
    
    def convert_and_save(self, text):
        """Convert text to audio and save as an MP3 file."""
        tts = gTTS(text=text, lang='en')
        tts.save(self.audio_path)
    
    def get_audio_bytes(self):
        """Retrieve audio bytes for playback."""
        if os.path.exists(self.audio_path):
            with open(self.audio_path, "rb") as audio_file:
                return audio_file.read()
        else:
            return None


# --- Streamlit App Layout ---
st.title("Media Inference Model")
st.write("Upload a video or image for processing")

media_processor = MediaProcessor(STATIC_FOLDER)
model_handler = ModelHandler(MODEL_PATH, ADAPTER_PATH)
text_to_speech = TextToSpeech(STATIC_FOLDER)

uploaded_file = st.file_uploader("Choose a file", type=["mp4", "jpg", "jpeg", "png"])
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
            st.subheader("Result")
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