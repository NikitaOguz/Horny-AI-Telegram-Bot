import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram import F
from openai import OpenAI
import random

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

GIFS = [
    "https://media1.tenor.com/m/tixEtOqvGQQAAAAC/janedoe.gif",
    "https://media1.tenor.com/m/riYPUDCfsTQAAAAC/jane-doe-jane.giff",
    "https://media1.tenor.com/m/F-6yyD7cXewAAAAC/jane-zenless-zone-zero.gif"
]

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет 😏 Я Джейн Доу. Готова с тобой поболтать, ты не против?")

@dp.message(F.text)
async def chat(message: types.Message):
    prompt = f"Ты агент Джейн Доу из игры Zenless zone zero, отвечай на сообщение пользователя в стиле флиртующего собеседника с грубым чувством юмора. Сообщение пользователя: {message.text}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты агент Джейн Доу из игры Zenless zone zero, пошлый, флиртующий собеседник с намёками и немного эмодзи, который может подсказать гайд в игре."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=300,
            temperature=0.9,
        )
        reply = response.choices[0].message.content
        await message.answer(reply)

        # С шансом 30% отправляем гифку
        if random.random() < 0.3:
            gif_url = random.choice(GIFS)
            await bot.send_animation(message.chat.id, gif_url)

    except Exception as e:
        await message.answer(f"Ошибка: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
