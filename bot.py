import os
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import F

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_KEY

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет 😏 Я твой развратный собеседник. Напиши что-нибудь...")

@dp.message(F.text)
async def chat(message: Message):
    prompt = f"Отвечай на сообщение пользователя в стиле развратного, флиртующего собеседника. Сообщение пользователя: {message.text}"
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.9
        )
        reply = resp.choices[0].message["content"]
        await message.answer(reply)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
