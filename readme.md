# Telegram bot with ChatGPT official API
Blog post about it: https://medium.com/@galperovich/put-chatgpt-right-into-your-messenger-build-a-telegram-bot-with-the-new-official-openai-api-84f7c005de7f 

OpenAI [announced](https://openai.com/blog/introducing-chatgpt-and-whisper-apis) they are opening the official ChatGPT model API for all developers. 
The model is named `gpt-3.5-turbo` and achieved a 90% cost reduction compared to the December'22 version. Truly cutting-edge AI development is now available to anyone, and the price is more than reasonable! 

Let's build a Telegram bot with the official ChatGPT API under the hood. Accessing the chat right from your messenger is much more convenient and better than going into OpenAI UI, logging in, etc. You can search by chat, forward to a friend, or even add to the group conversation.

We will use the openai and aiogram python packages. We will also learn how to use a Finite State Machine functionality in the bot to wait for the user's reply.

## Usage

1. Create a Telegram bot with [BotFather](https://t.me/botfather)
2. Get the OpenAI token https://platform.openai.com/account/api-keys 
3. Run the bot locally or deploy with Docker
4. Set the OpenAI token with /set_token
5. Start the chat with /new_chat

## Tools under the hood

1. Telegram bot and `aiogram` library
2. OpenAI API with `gpt-3.5-turbo` model (the same that is used by ChatGPT)

## How to run

### Environment variables

1. `BOT_TOKEN` - Telegram bot token. Get it by creating in [@BotFather](https://t.me/BotFather)
2. `LOG_LEVEL` - Logging level (options: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"). By default "INFO"

### Run locally

```shell
export BOT_TOKEN=<TELEGRAM_BOT_TOKEN>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Run the bot

```shell
python chatgpt_bot/bot.py
```

Send to your Telegram bot a link to the article and get the summary!

### Run with Docker

Warning: It won't work on arm86 (Apple Silicon), I wasn't able to make Pypeteer work in Docker.

But it works on Linux/Debian 10, x86-64.

```shell
docker build -t gpt_bot:latest .

docker run --rm --init -it --name gpt_bot \
  --env BOT_TOKEN="<TELEGRAM_BOT_TOKEN>" \
  gpt_bot:latest

# in case it is not killed by Ctrl+C
docker kill gpt_bot
```

