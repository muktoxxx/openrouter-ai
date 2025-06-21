# GPT-4o Telegram Bot

A Telegram bot powered by GPT-4o for advanced conversational AI with support for text and images.

## Setup

### Prerequisites
- Python 3.9+
- [Docker](https://docs.docker.com/get-docker/) (optional)
- A Telegram bot token (from [@BotFather](https://t.me/BotFather))
- OpenAI API key

### Local Installation
1. Clone the repository.
   ```sh
   git clone <repo-url>
   cd telegram_gpt4o_bot

Set up the environment:

sh

cp .env.example .env
Update .env with your credentials.


Install dependencies:

sh

pip install -r requirements.txt

Run the bot:

sh

python src/bot.py

Docker Deployment

Build the Docker image:

sh

docker-compose build

Start the bot:

sh

docker-compose up -d

Usage
Commands

/models - List available models and change the current one

Features

Multi-model support (GPT-4o, GPT-4, GPT-3.5-turbo)

Text processing

Image description and analysis

Model selection via interactive buttons

Configuration
Edit .env to configure:


BOT_TOKEN - Your Telegram bot token

OPENAI_API_KEY - Your OpenAI API key

MODEL_NAME - Default model to use

MAX_IMAGE_SIZE - Maximum image size to process

TEMP_IMAGE_DIR - Directory for temporary image storage

License
MIT License
