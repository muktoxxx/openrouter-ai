import os
from dotenv import load_dotenv
from typing import Dict, List

class Config:
    AVAILABLE_MODELS = ["gpt-4o", "gpt-4o-vision", "gpt-4", "gpt-3.5-turbo"]
    DEFAULT_MODEL = "gpt-4o"
    USER_SETTINGS = {}  # In-memory storage for user settings

    def __init__(self):
        load_dotenv()
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.MAX_IMAGE_SIZE = os.getenv("MAX_IMAGE_SIZE", "4096")
        self.TEMP_IMAGE_DIR = os.path.join("static", os.getenv("TEMP_IMAGE_DIR", "temp_images"))

        # Initialize GPT client
        from gpt_client import GPTClient
        self.gpt_client = GPTClient(self)

        # Create temp directory if it doesn't exist
        os.makedirs(self.TEMP_IMAGE_DIR, exist_ok=True)

    def get_user_settings(self, chat_id: str) -> Dict:
        """Get settings for a specific user/chat"""
        return self.USER_SETTINGS.get(str(chat_id), {})

    def update_user_settings(self, chat_id: str, new_settings: Dict):
        """Update settings for a specific user/chat"""
        chat_id = str(chat_id)
        if chat_id not in self.USER_SETTINGS:
            self.USER_SETTINGS[chat_id] = {}

        self.USER_SETTINGS[chat_id].update(new_settings)

        # Also update GPT client
        if new_settings.get("current_model"):
            self.gpt_client.set_user_model(chat_id, new_settings.get("current_model"))
