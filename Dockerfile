# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (use .env file in production)
ENV TELEGRAM_BOT_TOKEN=your_telegram_token_here
ENV OPENROUTER_API_KEY=your_openrouter_api_key_here

# Run the bot
CMD ["python", "bot.py"]
