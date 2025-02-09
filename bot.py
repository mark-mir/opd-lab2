import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = "7539602045:AAFJLcfeVtzVsFT39DpCYN82vanDwQjxNEo"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

questions = [
    {"question": "Какая компания разработала язык Python?", "options": ["Microsoft", "Google", "Apple", "PSF"],
     "answer": "PSF"},
    {"question": "Что делает функция len()?",
     "options": ["Возвращает длину объекта", "Удаляет объект", "Клонирует объект", "Сортирует объект"],
     "answer": "Возвращает длину объекта"},
    {"question": "Какой тип данных используется для хранения целых чисел в Python?",
     "options": ["int", "float", "str", "bool"], "answer": "int"},
    {"question": "Какой тип данных используется для хранения вещественных чисел в Python?",
     "options": ["int", "float", "str", "bool"], "answer": "float"},
    {"question": "В каком году был создан язык программирования Python?",
     "options": ["1989", "1969", "1972", "1990"], "answer": "1989"}
]

user_data = {}

@dp.message_handler(commands=['start'])
async def ask_to_play(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Да"))
    keyboard.add(KeyboardButton("Нет"))
    await message.reply("Привет! Хочешь сыграть в викторину?", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text.lower() == "да")
async def start_game(message: types.Message):
    user_data[message.chat.id] = {"score": 0, "current_question": 0}
    await send_question(message.chat.id)

@dp.message_handler(lambda message: message.text.lower() == "нет")
async def decline_game(message: types.Message):
    await message.reply("Хорошо, если передумаешь, напиши /start!")

async def send_question(chat_id):
    user = user_data.get(chat_id, None)
    if user and user["current_question"] < len(questions):
        q = questions[user["current_question"]]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for option in q["options"]:
            keyboard.add(KeyboardButton(option))
        await bot.send_message(chat_id, q["question"], reply_markup=keyboard)
    else:
        await bot.send_message(chat_id, f"Игра окончена! Ваш счет: {user['score']}\nВведите /start для начала новой игры.")


@dp.message_handler()
async def handle_answer(message: types.Message):
    user = user_data.get(message.chat.id, None)
    if not user:
        await message.reply("Введите /start для начала игры.")
        return

    q = questions[user["current_question"]]
    if message.text == q["answer"]:
        user["score"] += 1
        await message.reply("Правильно!")
    else:
        await message.reply(f"Неверно! Правильный ответ: {q['answer']}")

    user["current_question"] += 1
    await send_question(message.chat.id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
