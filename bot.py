import os
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def chat_with_ai(message: types.Message):
    try:
        prompt = (
            f"Ты Джейн Доу, отвечай на сообщение пользователя в стиле развратного, флиртующего собеседника. "
            f"Будь слегка провокационной, используй намёки, эмодзи. "
            f"Сообщение пользователя: {message.text}"
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты развратный, флиртующий собеседник, отвечай с намёками и эмодзи."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=150,
            temperature=0.9,
        )
        answer = response['choices'][0]['message']['content']
        await message.answer(answer)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
