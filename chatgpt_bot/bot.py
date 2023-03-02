from enum import Enum

import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from chatgpt_bot.settings import BOT_TOKEN, MODEL_NAME, logger, BOT_HISTORY_LENGTH

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logger.info("Bot has started")


class Role(Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class MessageHistory:
    def __init__(self):
        self.history = []

    def add_message(self, role: Role, message):
        message = {"role": role.value, "content": message}
        self.history.append(message)

    def clear(self):
        self.history = []
        logger.info("Message History was cleared")

    def get_history(self, history_length=BOT_HISTORY_LENGTH):
        return self.history[-history_length:]


MESSAGE_HISTORY = MessageHistory()


class Form(StatesGroup):
    open_ai_token = State()
    continue_chat = State()
    ready_to_end = State()


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    logger.info("/start command was invoked")
    await message.answer(
        "Hi! I pretend to be a ChatGPT :)\n" "Commands:\n" "/set_token\n" "/new_chat"
    )


@dp.message_handler(commands=["set_token"])
async def set_token(message: types.Message):
    """Set OpenAI token"""
    logger.info("/set_token command was invoked")
    await Form.open_ai_token.set()
    await message.answer("Hi! Please send your OpenAI Token")


@dp.message_handler(state=Form.open_ai_token)
async def process_open_ai_token(message: types.Message, state: FSMContext):
    """Add OpenAI token to the library settings"""
    await state.finish()
    openai.api_key = message.text
    await message.reply(f"Token was set. To start the chat use /new_chat")
    logger.info("OpenAI token was set")


@dp.message_handler(commands=["new_chat"])
async def new_chat(message: types.Message):
    """Start a new chat, the previous history will be removed from the bot's memory"""
    logger.info("/new_chat command was invoked")
    MESSAGE_HISTORY.clear()
    start_message = "Hi! I'm your own ChatGPT in Telegram :) How can I help you?"
    MESSAGE_HISTORY.add_message(Role.SYSTEM, start_message)
    await Form.continue_chat.set()
    await message.answer(start_message)


@dp.message_handler(state=Form.continue_chat)
async def continue_conversation(message: types.Message, state: FSMContext):
    """Continue conversation after the chat was started"""

    await state.finish()
    user_answer = message.text
    if user_answer == "/new_chat":
        await new_chat(message)
        return
    elif user_answer == "/set_token":
        await set_token(message)
        return

    MESSAGE_HISTORY.add_message(Role.USER, user_answer)
    gpt_response = get_chatgpt_response(MESSAGE_HISTORY)
    MESSAGE_HISTORY.add_message(Role.ASSISTANT, gpt_response)

    await Form.continue_chat.set()
    await message.answer(gpt_response, parse_mode=types.ParseMode.MARKDOWN)


def get_chatgpt_response(
    message_history: MessageHistory, history_length=BOT_HISTORY_LENGTH
) -> str:
    """
    Main function that communicates with the ChatGPT API
    """
    logger.info("Query GhatGPT API")
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=message_history.get_history(history_length=history_length),
    )
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
