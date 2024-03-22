from aiogram import Dispatcher, Router, Bot, F
from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
import asyncio
import logging

from markup import Markups

bot = Bot('TOKEN')
router = Router()
dp = Dispatcher()

users = {}
markups = Markups()


class Queries(StatesGroup):
    choosing_product = State()


@router.message(F.text == 'Back')
@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text="W3lc0m3 70 1nn0d4rk5h0p. \n1 4lr34dy h4v3 4ll"
                                                              " 1nf0rm4710n 4b0u7 y0u. 50, m4k3 y0ur53lf 47 h0m3 ☺️",
                           reply_markup=markups.main_markup())
    await state.clear()
    logging.info(f"User_id - {message.chat.id} - message amount - {users[message.chat.id]}")


@router.callback_query(F.data == 'back')
async def back(cb: types.CallbackQuery):
    await bot.delete_message(cb.message.chat.id, cb.message.message_id)


@router.message(F.text == 'C474l06 🛒')
@router.message(F.text == 'N3x7 ➡️')
@router.message(F.text == '⬅️ Pr3v')
async def catalog(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    page_number = state_data.get('page_number', 1)
    if page_number != 1 and message.text == '⬅️ Pr3v':
        page_number -= 1
    elif message.text == 'N3x7 ➡️':
        page_number += 1
    await state.update_data(page_number=page_number)
    await bot.send_message(message.from_user.id,
                           text='D0 y0u w4n7 50m37h1n6?',
                           reply_markup=markups.catalog_markup(page=page_number))


@router.message(F.text == 'B4l4nc3 💰')
async def balance(message: types.Message):
    await bot.send_message(message.chat.id, text=markups.db.get_balance(message.chat.id))


@router.callback_query(F.data.contains('buy'))
async def confirm_purchase(cb: types.CallbackQuery):
    title = cb.data.split('_')[1]
    await bot.edit_message_reply_markup(cb.message.chat.id, cb.message.message_id,
                                        reply_markup=markups.confirm_purchase(title))


@router.callback_query(F.data.contains('confirm'))
async def buy_product(cb: types.CallbackQuery):
    title = cb.data.split('_')[1]
    await bot.delete_message(cb.message.chat.id, cb.message.message_id)
    await bot.send_message(cb.message.chat.id,
                           text=markups.db.buy_product(cb.message.chat.id, title))


@router.message()
async def find_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if not data.get('page_number', None):
        return
    answer = markups.db.make_message(message.text)
    if 'T1tl3' in answer:
        await bot.send_message(message.chat.id, answer,
                           reply_markup=markups.product_info_markup(message.text))
    else:
        await bot.send_message(message.chat.id, answer)


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())