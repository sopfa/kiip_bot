import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from datetime import datetime, timedelta
import json

API_TOKEN = '7832882030:AAHRw7sa2yFisyv5SAypaExIeTt2-oKl1Ss'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Загрузка слов из файла
with open("lessons.json", "r", encoding="utf-8") as f:
    lessons = json.load(f)

user_data = {}

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(KeyboardButton("📖 Учить слова"), KeyboardButton("🔁 Повторение"))
main_keyboard.add(KeyboardButton("📚 Выбрать урок"))

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    user_data[message.from_user.id] = {"mode": "learn", "lesson": "1", "index": 0}
    await message.answer("👋 Привет! Я помогу тебе учить слова из KIIP 3. Выбери, что хочешь делать:", reply_markup=main_keyboard)

@dp.message_handler(lambda m: m.text == "📚 Выбрать урок")
async def choose_lesson(message: types.Message):
    lesson_list = "\n".join([f"Урок {i}" for i in range(1, 19)])
    await message.answer(f"Напиши номер урока, который хочешь учить (1–18):\n{lesson_list}")

@dp.message_handler(lambda m: m.text.isdigit() and 1 <= int(m.text) <= 18)
async def set_lesson(message: types.Message):
    user_data[message.from_user.id] = {"mode": "learn", "lesson": message.text, "index": 0}
    await message.answer(f"✅ Урок {message.text} выбран. Напиши '📖 Учить слова', чтобы начать.")

@dp.message_handler(lambda m: m.text == "📖 Учить слова")
async def learn_words(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.answer("Сначала выбери урок с помощью команды '📚 Выбрать урок'.")
        return
    data = user_data[user_id]
    lesson = data["lesson"]
    index = data["index"]
    word_list = lessons[lesson]
    if index >= len(word_list):
        await message.answer("🎉 Ты выучил все слова в этом уроке!")
        return
    entry = word_list[index]
    question = f"📌 Слово: {entry['word']}

💬 Пример: {entry['example']}

(Ответ появится через 5 секунд...)"
    await message.answer(question)
    await asyncio.sleep(5)
    answer = f"📖 Перевод: {entry['translation']}
📘 Перевод примера: {entry['example_translation']}"
    user_data[user_id]["index"] += 1
    await message.answer(answer)

@dp.message_handler(lambda m: m.text == "🔁 Повторение")
async def review_words(message: types.Message):
    await message.answer("🔁 Функция повторения будет добавлена в следующей версии.")

if __name__ == '__main__':
    import asyncio
    asyncio.run(dp.start_polling())