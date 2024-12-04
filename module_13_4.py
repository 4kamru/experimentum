from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

api =""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

s_age = 0
s_growth = 0
s_weight = 0

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью")


@dp.message_handler(text='calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    global s_age
    await state.update_data(first=message.text)
    data = await state.get_data()
    s_age = data["first"]
    # print(f'set_growth {data["first"]}')
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    global s_growth
    await state.update_data(first=message.text)
    data = await state.get_data()
    s_growth = data["first"]
    # print(f'set_weight {data["first"]}')
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    global s_weight
    await state.update_data(first=message.text)
    data = await state.get_data()
    s_weight = data["first"]
    # print(f'send_calories {data["first"]}')
    # вычисление нормы калорий
    norma = 10*float(s_weight) + 6.25*float(s_growth) - 5*float(s_age)
    # print('s_age =', s_age, ' s_growth = ', s_growth,' s_weight = ', s_weight)
    await message.answer(f'Ваша норма калорий: {norma}')
    await state.finish()



@dp.message_handler()
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)


