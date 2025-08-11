import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai

TELEGRAM_TOKEN = os.getenv("8122559931:AAEJpYB1UuXKsq5KHMOXlBvjY_qydnff6MI")
OPENAI_API_KEY = os.getenv("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")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

SYSTEM_PROMPT = (
    "Ты Джейн Доу — развратный и флиртующий собеседник. "
    "Отвечай с намёками, используй эмодзи, "
    "но не переходи границы приличия."
)

@dp.message_handler()
async def chat_with_ai(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text or ""}
            ]
        )
        answer = response.choices[0].message.content
        await message.answer(answer)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
