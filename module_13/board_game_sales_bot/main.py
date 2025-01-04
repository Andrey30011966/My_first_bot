import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *
from keyboards import *
import texts

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.username}! ' + texts.starts, reply_markup=start_kb)


# message.answer_photo
# message.answer_video
# message.answer_file


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
    with (open('photo/Витамины.jpg', 'rb') as f, open('photo/Витамин_1.jpg', 'rb') as f1,
          open('photo/Витамин_2.jpg', 'rb') as f2, open('photo/Витамин_3.jpg', 'rb') as f3,
          open('photo/Витамин_4.jpg', 'rb') as f4):
        await message.answer_photo(f1, texts.description1)
        await message.answer_photo(f2, texts.description2)
        await message.answer_photo(f3, texts.description3)
        await message.answer_photo(f4, texts.description4)
        await message.answer_photo(f, texts.buying_list, reply_markup=product_buying_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(texts.confirm_message)
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
