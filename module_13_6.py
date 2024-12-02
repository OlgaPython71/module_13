from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = "7877642793:AAH_MtD_MUgjVUEuLQU61TgVFKYWv2xnEB8"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)
formula = InlineKeyboardMarkup()
button_f_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_f_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
formula.add(button_f_1)
formula.add(button_f_2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=formula)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10*вес(кг)+6,25*рост(см)-5*возраст(г)-161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calculation = (10 * int(data['weight'])) + (6 * int(data['growth'])) - (5 * int(data['age'])) - 161
    await message.answer(f'Ваша норма калорий {calculation}')
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)