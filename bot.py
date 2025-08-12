import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
import openai

# Читаем токены из переменных окружения Railway
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка токенов
if not TELEGRAM_TOKEN:
    raise ValueError("❌ Ошибка: TELEGRAM_TOKEN не найден. Добавь его в Railway → Settings → Variables.")
if not OPENAI_API_KEY:
    raise ValueError("❌ Ошибка: OPENAI_API_KEY не найден. Добавь его в Railway → Settings → Variables.")

# Настраиваем бота и OpenAI
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
openai.api_key = OPENAI_API_KEY

# Характер Джейн Доу
SYSTEM_PROMPT = """
Ты — Джейн Доу из игры Zenless Zone Zero.
Ты харизматична, кокетлива, немного дерзкая.
Флиртуй игриво, с юмором, но без пошлости.
"""

# Функция генерации ответа от ИИ
async def generate_ai_reply(user_message: str) -> str:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.9
        )
        return completion.choices[0].message["content"].strip()
    except Exception as e:
        return f"Ой, кажется я запнулась… {e}"

# Команда /start
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Привет, я Джейн Доу 😏 Хочешь, я тебе подмигну или скажу что-то игривое?")

# Ответы на сообщения
@dp.message()
async def chat_handler(message: Message):
    # В группе — отвечаем только если нас тегнули
    if message.chat.type in ["group", "supergroup"]:
        if not (message.text and (f"@{(await bot.get_me()).username}" in message.text)):
            return

    ai_response = await generate_ai_reply(message.text)
    await message.reply(ai_response)

# Запуск
async def main():
    print("✅ Бот запущен как:", (await bot.get_me()).username)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
