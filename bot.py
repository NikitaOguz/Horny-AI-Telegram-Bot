import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import openai
import asyncio

# Загружаем токены из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("8122559931:AAEJpYB1UuXKsq5KHMOXlBvjY_qydnff6MI")
OPENAI_API_KEY = os.getenv("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")

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

openai.api_key = OPENAI_API_KEY

# Системная инструкция для ИИ (характер Джейн Доу)
SYSTEM_PROMPT = """
Ты — Джейн Доу из игры Zenless Zone Zero. 
Ты умная, харизматичная, слегка дерзкая и кокетливая. 
Флиртуй с собеседником, но делай это игриво, без грубости.
Отвечай кратко, эмоционально и с юмором, можно с эмодзи.
"""

async def generate_ai_reply(user_message: str) -> str:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Можно заменить на более мощный
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.9
        )
        return completion.choices[0].message["content"].strip()
    except Exception as e:
        return f"Ой, кажется я запнулась… {e}"

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Привет малыш 😏, я Джейн Доу хочешь, поговорим со мной? Мне так одиноко🥺.")

@dp.message()
async def chat_handler(message: Message):
    # В группе — отвечаем только если нас тегнули
    if message.chat.type in ["group", "supergroup"]:
        if not (message.text and (f"@{(await bot.get_me()).username}" in message.text)):
            return

    ai_response = await generate_ai_reply(message.text)
    await message.reply(ai_response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
