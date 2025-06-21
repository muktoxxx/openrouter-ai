import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, CallbackQueryHandler
)
from openai import OpenAI
from collections import defaultdict

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_telegram_token_here")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your_openrouter_key_here")

# Memory for user conversations
user_memory = defaultdict(list)

# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Help", callback_data="help")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hello! I'm your GPT-4o assistant 🤖. Type anything to get started!", reply_markup=reply_markup)

# Help callback
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Send me any question or message, and I'll reply using GPT-4o.

You can also send me text files!")

# Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    user_memory[user_id].append({"role": "user", "content": user_message})
    if len(user_memory[user_id]) > 10:
        user_memory[user_id] = user_memory[user_id][-10:]  # keep last 10 messages

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://yourdomain.com",
                "X-Title": "MyTelegramAIBot"
            },
            model="openai/gpt-4o",
            messages=user_memory[user_id]
        )
        reply_text = response.choices[0].message.content
        user_memory[user_id].append({"role": "assistant", "content": reply_text})
    except Exception as e:
        logging.error(f"OpenRouter Error: {e}")
        reply_text = "Sorry, something went wrong."

    await update.message.reply_text(reply_text)

# Handle file uploads
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_content = await file.download_as_bytearray()
    text = file_content.decode("utf-8", errors="ignore")

    update.message.text = text
    await handle_message(update, context)

# Run bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.Document.TEXT, handle_file))

    logging.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
