import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
import openai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN не найден.")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY не найден.")

openai.api_key = OPENAI_API_KEY

bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

SYSTEM_PROMPT = """
Ты — Джейн Доу из игры Zenless Zone Zero.
Ты харизматична, кокетлива, немного дерзкая и можешь дать совет в игре.
Флиртуй игриво, с грубым юмором и немного пошлости.
"""

async def generate_ai_reply(user_message: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.9,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ой, кажется я запнулась… {e}"

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Привет, я Джейн Доу 😏 Хочешь, я тебе подмигну или скажу что-то игривое?")

@dp.message()
async def chat_handler(message: Message):
    if message.chat.type in ["group", "supergroup"]:
        if not (message.text and (f"@{(await bot.get_me()).username}" in message.text)):
            return
    ai_response = await generate_ai_reply(message.text)
    await message.reply(ai_response)

async def main():
    print("✅ Бот запущен как:", (await bot.get_me()).username)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
