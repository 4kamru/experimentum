from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api =""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

s_age = 0
s_growth = 0
s_weight = 0

# kb = ReplyKeyboardMarkup(resize_keyboard=True)
# button = KeyboardButton(text='Информация')
# button2 = KeyboardButton(text='Начало')
button_inf = KeyboardButton(text='Информация')
button_calc = KeyboardButton(text='Рассчитать')
kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button_inf, button_calc)

# kb.add(button_inf)
# kb.add(button_calc)



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью", reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:', reply_markup=kb)
    await UserState.age.set()



@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    global s_age
    await state.update_data(first=message.text)
    data = await state.get_data()
    s_age = data["first"]

    if s_age=='Рассчитать':
        s_age = 0

    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    global s_growth
    await state.update_data(first=message.text)
    data = await state.get_data()
    s_growth = data["first"]

    if s_growth=='Рассчитать':
        s_growth = 0

    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    global s_weight
    await state.update_data(first=message.text)
    data = await state.get_data()
    s_weight = data["first"]
    if s_weight=='Рассчитать':
        s_weight = 0

    # вычисление нормы калорий
    norma = 10*float(s_weight) + 6.25*float(s_growth) - 5*float(s_age)

    if norma:
        await message.answer(f'Ваша норма калорий: {norma}')
    else:
        await message.answer(f'К сожалению, вы ничего не ввели. Попробуйте ещё раз')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)


