from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

calculate_button = KeyboardButton('Рассчитать')
info_button = KeyboardButton('Информация')
kb = ReplyKeyboardMarkup(resize_keyboard=True).add(calculate_button, info_button)

inline_calculate_button = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
inline_formula_button = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
inline_kb = InlineKeyboardMarkup().add(inline_calculate_button, inline_formula_button)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Привет! Нажми кнопку "Рассчитать", чтобы узнать свою норму калорий.',
                        reply_markup=kb)

@dp.message_handler(Text(equals="Рассчитать", ignore_case=True))
async def main_menu(message: types.Message):
    await message.reply('Выберите опцию: ', reply_markup=inline_kb)

@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.reply("Формула Миффлина-Сан Жеора: 10 * вес + 6.25 * рост - 5 * возраст + 5")
    await call.answer()

@dp.callback_query_handler(lambda call: call.data == 'calories')
async def get_age(call: types.CallbackQuery):
    await UserState.age.set()
    await call.message.reply('Введите свой возраст: ')
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await UserState.next()
    await message.reply('Введите свой рост: ')

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await UserState.next()
    await message.reply('Введите свой вес: ')

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    calories = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5
    await message.reply(f'Ваша норма калорий: {calories}')
    await state.finish()

@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)