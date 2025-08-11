import asyncio
from aiogram import Bot, Dispatcher, types
import openai
from datetime import datetime

TELEGRAM_TOKEN = "8122559931:AAEJpYB1UuXKsq5KHMOXlBvjY_qydnff6MI"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

SYSTEM_PROMPT = (
    "Ты — развратный и флиртующий собеседник. "
    "Отвечай с намёками и эмодзи, но не переходи границы приличия."
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
