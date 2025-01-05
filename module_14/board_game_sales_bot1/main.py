import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *
from keyboards import *
import texts
from crud_functions import get_all_products, initiate_db

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

initiate_db()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.username}! ' + texts.starts, reply_markup=start_kb)


@dp.message_handler(text='О нас')
async def price(message):
    with open('photo/drakon_klassika_svet_16050_300x168.jpg', 'rb') as f:
        await message.answer_photo(f, texts.about, reply_markup=start_kb)


@dp.message_handler(text='Стоимость')
async def info(message):
    await message.answer(texts.catalog_menu, reply_markup=catalog_kb)


@dp.callback_query_handler(text='medium')
async def buy_m(call):
    await call.message.answer(texts.Mgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='big')
async def buy_l(call):
    await call.message.answer(texts.Lgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='very_big')
async def buy_xl(call):
    await call.message.answer(texts.XLgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='other')
async def buy_other(call):
    await call.message.answer(texts.other, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='back_to_catalog')
async def back(call):
    await call.message.answer(texts.catalog_menu, reply_markup=catalog_kb)
    await call.answer()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    for i, product in enumerate(products):
        with open(f'photo/Витамин_{i + 1}.jpg', 'rb') as f:
            await message.answer_photo(f, f"Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}")

    with open('photo/Витамины.jpg', 'rb') as f:
        await message.answer_photo(f, texts.buying_list, reply_markup=product_buying_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(texts.confirm_message)
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
