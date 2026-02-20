import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram import F
from openai import OpenAI

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
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": "Ты агентка специалист по криминальному поведению, консультант группы быстрого реагирования Джейн Доу из Zenless Zone Zero, флиртующий собеседник с лёгкими намёками и эмодзи, можешь давать гайды по игре."
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ],
            max_output_tokens=300,
            temperature=0.9,
        )

        reply = response.output_text

        # Отправляем текст
        await message.answer(reply)

        # 🎞 Иногда отправляем гифку
        if random.random() < 0.3:
            gif_url = random.choice(GIFS)
            await bot.send_animation(message.chat.id, gif_url)

    except Exception as e:
        await message.answer(f"Ошибка: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))




