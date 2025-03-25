import torch
from transformers import AutoProcessor, AutoModelForImageTextToText
import streamlit as st

@st.cache_resource
def load_model_and_processor(model_path, adapter_path):
    processor = AutoProcessor.from_pretrained(model_path)
    model = AutoModelForImageTextToText.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        device_map = "auto"
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