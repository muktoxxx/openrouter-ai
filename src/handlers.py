from telegram import Update, PhotoSize, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters, CommandHandler
from config import Config
import os
import uuid
import image_processor

class MessageHandlers:
    def __init__(self, config: Config):
        self.config = config
        self.image_processor = image_processor.ImageProcessor()

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user_message = update.message.text
        chat_id = update.message.chat_id

        user_settings = self.config.get_user_settings(chat_id)

        try:
            # Process text with selected model
            processed_response = await self.config.gpt_client.process_text(
                user_message,
                model=user_settings.get("current_model")
            )

            # Send response
            if processed_response:
                await context.bot.send_message(chat_id=chat_id, text=processed_response)
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id,
                                         text="Sorry, there was an error processing your request.")

    async def list_models(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Command to show available models"""
        chat_id = update.message.chat_id

        # Get available models from config
        available_models = self.config.AVAILABLE_MODELS

        # Create keyboard with model selection buttons
        buttons = [
            [InlineKeyboardButton(model, callback_data=f"model_{model}")]
            for model in available_models
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        # Get current model or default
        user_settings = self.config.get_user_settings(chat_id)
        current_model = user_settings.get("current_model", available_models[0])

        # Format message showing current and available models
        message_text = (
            f"Current model: {current_model}\n\n"
            "Available models: "
        )

        message_text += ", ".join([f"*{m}*" for m in available_models])

        await update.message.reply_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def select_model_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback for model selection"""
        chat_id = update.callback_query.message.chat_id
        query = update.callback_query
        await query.answer()

        callback_data = query.data.split("_")[1]

        # Update user settings
        self.config.update_user_settings(chat_id, {"current_model": callback_data})

        # Edit the original message with the new selection
        message_text = (
            f"Model changed to {callback_data}\n\n"
            "You can now send messages and they'll be processed with this model."
        )

        try:
            await query.edit_message_text(
                text=message_text,
                reply_markup=None
            )
        except:
            # If the message is too old, send a new message
            await context.bot.send_message(
                chat_id=chat_id,
                text=message_text
            )

    async def handle_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle image messages"""
        if not update.message or not update.message.photo:
            await update.message.reply_text("Please send a valid image.")
            return

        chat_id = update.message.chat_id
        file = await update.message.bot.get_file(update.message.photo[-1].file_id)
        file_path, success = self.image_processor.save_image_from_file(file)

        if not success:
            await update.message.reply_text("Failed to process the image.")
            return

        try:
            # Process image with GPT-4o
            processed_response = await self.config.gpt_client.process_image(file_path)

            # Send response
            if isinstance(processed_response, dict):
                # Handle response with both text and image
                if processed_response.get('text'):
                    await context.bot.send_message(chat_id=chat_id, text=processed_response.get('text'))

                if processed_response.get('image'):
                    await context.bot.send_photo(chat_id=chat_id, photo=processed_response.get('image'))

            elif isinstance(processed_response, str):
                # Handle text only response
                await context.bot.send_message(chat_id=chat_id, text=processed_response)

        except Exception as e:
            await context.bot.send_message(chat_id=chat_id,
                                         text="Sorry, there was an error processing your image.")
        finally:
            # Clean up temporary image
            self.image_processor.clean_temp_images()

    async def handle_video_or_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle videos or documents that might contain images"""
        chat_id = update.message.chat_id

        if update.message.video:
            file = await update.message.bot.get_file(update.message.video.file_id)
        elif update.message.document:
            file = await update.message.bot.get_file(update.message.document.file_id)
        else:
            return

        # Save file temporarily
        temp_file_path = os.path.join(self.image_processor.temp_dir, f"{uuid.uuid4()}.tmp")
        await file.download_to_drive(temp_file_path)

        try:
            # Process with GPT-4o
            processed_response = await self.config.gpt_client.process_media(temp_file_path)

            # Send response
            if processed_response:
                await context.bot.send_message(chat_id=chat_id, text=processed_response)
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id,
                                         text="Sorry, I couldn't process that format.")

        finally:
            # Clean up temporary file
            os.remove(temp_file_path)
