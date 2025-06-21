GPT-4o Telegram Bot
A Telegram bot powered by OpenAI's GPT-4o with support for advanced text and image processing.

🚀 Features
🔁 Multi-model support: gpt-4o, gpt-4o-vision, gpt-4, gpt-3.5-turbo

💬 Natural text conversation

🖼️ Image description and analysis

📲 Model selection via inline buttons

📦 Dockerized deployment for convenience

🧰 Prerequisites
Python 3.9+

Docker (optional)

Telegram bot token via @BotFather

OpenAI API key

🛠️ Installation
Clone and Set Up
bash
git clone <repo-url>
cd telegram_gpt4o_bot
cp .env.example .env
# Then update your .env file with your bot token and API key
Install Dependencies
bash
pip install -r requirements.txt
Run Locally
bash
python src/bot.py
🐳 Docker Deployment
Build & Run
bash
docker-compose build
docker-compose up -d
🧑‍💻 Usage
Telegram Commands
/models – List and switch between available models

⚙️ Configuration
Modify the .env file as needed:

Variable	Description
BOT_TOKEN	Your Telegram bot token
OPENAI_API_KEY	Your OpenAI API key
MODEL_NAME	Default model to start with
MAX_IMAGE_SIZE	Max image size (in pixels or bytes)
TEMP_IMAGE_DIR	Directory for temporary image storage
📄 License
MIT License — feel free to use, modify, and distribute.
