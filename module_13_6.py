from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api =""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())



button_inf = KeyboardButton(text='Информация')
button_calc = KeyboardButton(text='Рассчитать')
kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button_inf, button_calc)

# Создайте клавиатуру InlineKeyboardMarkup с 2 кнопками InlineKeyboardButton:
kb2 = InlineKeyboardMarkup()

# !!!!!!!!!!!! button.add - уже не нужно, у нас есть то, что ниже (inline_keyboard) - напоминание для себя
# либо у нас button.add  , либо вот эта матрица из кнопок...
# блин, на уроке там были обычные ReplyKeyboardMarkup, хотя тема была про инлайн - РРРРРРРР!
calc_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas') # эти 2 кнопки во 2-й строке
        ]
    ], resize_keyboard=True
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Создайте новую функцию main_menu(message), которая:
# Будет обёрнута в декоратор message_handler, срабатывающий при передаче текста 'Рассчитать'.
# Сама функция будет присылать ранее созданное Inline меню и текст 'Выберите опцию:'
@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=calc_menu)

# Создайте новую функцию get_formulas(call), которая:
# Будет обёрнута в декоратор callback_query_handler, который будет реагировать на текст 'formulas'.
# Будет присылать сообщение с формулой Миффлина-Сан Жеора.
@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    msg = ('Упрощенный вариант формулы Миффлина-Сан Жеора:\n'
           + 'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\n'
           +'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.message.answer(msg,reply_markup=kb2)
    await call.answer()


@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью", reply_markup=kb)

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Я умею рассчитывать норму ккал (для мужчин) по упрощенной формуле Миффлина-Сан Жеора.')

# Измените функцию set_age и декоратор для неё:
# Декоратор смените на callback_query_handler, который будет реагировать на текст 'calories'.
# Теперь функция принимает не message, а call. Доступ к сообщению будет следующим - call.message.
@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()



@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(txt_age=message.text)
    data = await state.get_data()

    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(txt_growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(txt_weight=message.text)
    data = await state.get_data()
    try:
        s_age = float(data["txt_age"])
        s_growth = float(data["txt_growth"])
        s_weight = float(data["txt_weight"])
    except:
        await message.answer(f'Невозможно преобразовать ваши данные в числа. Скорее всего некорректный ввод')
        await state.finish()
        return


    # вычисление нормы калорий
    norma = 10*float(s_weight) + 6.25*float(s_growth) - 5*float(s_age)

    await message.answer(f'Ваша норма калорий: {norma}')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)


