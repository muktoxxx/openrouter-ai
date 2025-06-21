import os
import openai
from config import Config
from typing import Optional, Dict, Any

class GPTClient:
    def __init__(self, config: Config):
        self.config = config
        self.api_key = config.OPENAI_API_KEY
        openai.api_key = self.api_key
        self.user_settings = {}

    def set_user_model(self, chat_id: str, model: str):
        """Set the model for a specific user/chat"""
        self.user_settings[chat_id] = self.user_settings.get(chat_id, {})
        self.user_settings[chat_id]["current_model"] = model

    def get_user_model(self, chat_id: str) -> str:
        """Get the current model for a specific user/chat"""
        return self.user_settings.get(chat_id, {}).get("current_model", self.config.DEFAULT_MODEL)

    async def process_text(self, prompt: str, model: Optional[str] = None) -> str:
        """Process text input using the specified model"""
        if model is None:
            model = self.config.DEFAULT_MODEL

        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error processing text with GPT: {e}")

    async def process_image(self, image_path: str, model: Optional[str] = None) -> Dict[str, Any]:
        """Process image input using the specified model"""
        if model is None:
            model = self.config.DEFAULT_MODEL

        try:
            with open(image_path, "rb") as image_file:
                response = await openai.ChatCompletion.acreate(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Describe this image."},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"file-{image_path}",
                                        "detail": "low"
                                    }
                                }
                            ]
                        }
                    ]
                )

                # Format the response appropriately
                response_content = response.choices[0].message.content.strip()

                return {
                    "text": response_content,
                    "confidence": response.choices[0].finish_reason
                }
        except Exception as e:
            raise Exception(f"Error processing image with GPT: {e}")
