from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import Config
from handlers import MessageHandlers
import logging

class TelegramBot:
    def __init__(self):
        config = Config()
        self.application = Application.builder().token(config.BOT_TOKEN).build()
        self.handlers = MessageHandlers(config)
        self.setup_handlers()

    def setup_handlers(self):
        # Commands
        self.application.add_handler(CommandHandler("models", self.handlers.list_models))

        # Text messages
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_text))

        # Model selection callbacks
        self.application.add_handler(MessageHandler(
            filters.Text(regex=r'^model_'),
            self.handlers.select_model_callback
        ))

        # Media messages
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handlers.handle_image))
        self.application.add_handler(MessageHandler(
            filters.VIDEO | filters.Document.category("image"),
            self.handlers.handle_video_or_document
        ))

    async def run(self):
        await self.application.run_polling()

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    bot = TelegramBot()
    await bot.run()
