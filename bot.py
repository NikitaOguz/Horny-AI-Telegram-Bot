import asyncio
from aiogram import Bot, Dispatcher, types
import openai
from datetime import datetime
import os

TELEGRAM_TOKEN = os.getenv("8122559931:AAEJpYB1UuXKsq5KHMOXlBvjY_qydnff6MI") or "твой_токен_здесь"
OPENAI_API_KEY = os.getenv("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") or "твой_openai_ключ_здесь"

openai.api_key = OPENAI_API_KEY

bot = Bot(token="8122559931:AAEJpYB1UuXKsq5KHMOXlBvjY_qydnff6MI")
dp = Dispatcher()

SYSTEM_PROMPT = (
    "Ты Джейн Доу — развратный и флиртующий собеседник. "
    "Отвечай с намёками и эмодзи, но не переходи границы приличия."
)

@dp.message()
async def handle_message(message: types.Message):
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text or ""}
            ]
        )
        response_text = completion.choices[0].message.content
        await message.answer(response_text)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


