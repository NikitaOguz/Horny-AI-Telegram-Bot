import asyncio
import openai
from aiogram import Bot, Dispatcher, types

TELEGRAM_TOKEN = "8122559931:AAEJpYB1UuXKsq5KHMOXlBvjY_qydnff6MI"
OPENAI_API_KEY = "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"  # твой ключ

openai.api_key = OPENAI_API_KEY
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message()
async def chat(message: types.Message):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "Ты — Джейн Доу, игривая и флиртовая собеседница, "
                        "которая любит кокетничать и использовать эмодзи. "
                        "Отвечай с лёгкой провокацией, но уважительно и без оскорблений."
                    )
                },
                {"role": "user", "content": message.text}
            ]
        )
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

