import os
import asyncio
from aiogram import Bot, Dispatcher, types
import openai

TELEGRAM_TOKEN = os.getenv("8122559931:AAEJpYB1UuXKsq5KHMOXlBvjY_qydnff6MI")
OPENAI_API_KEY = os.getenv("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")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

SYSTEM_PROMPT = (
    "Ты Джейн Доу — развратный и флиртующий агент из игры Zenless zone zero. "
    "Отвечай с намёками и немного эмодзи, грубо шути с собеседником на разные темы включая политик, но не переходи границы приличия."
)

@dp.message()
async def handle_message(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text or ""}
            ]
        )
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

