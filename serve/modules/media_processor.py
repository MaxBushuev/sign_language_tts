import os

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