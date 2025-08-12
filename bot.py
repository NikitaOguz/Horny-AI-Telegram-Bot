import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram import F
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет 😏 Я твой развратный собеседник. Напиши что-нибудь...")

@dp.message(F.text)
async def chat(message: types.Message):
    prompt = f"Отвечай на сообщение пользователя в стиле развратного, флиртующего собеседника. Сообщение пользователя: {message.text}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты развратный, флиртующий собеседник с намёками и эмодзи."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=300,
            temperature=0.9,
        )
        reply = response.choices[0].message.content
        await message.answer(reply)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
