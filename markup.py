from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from shopDB import DB


class Markups:
    def __init__(self):
        self.db = DB()
        self.products_on_page = 3

    @staticmethod
    def main_markup() -> ReplyKeyboardMarkup:
        buttons = [[KeyboardButton(text='C474l06 🛒')],
                   [KeyboardButton(text='B4l4nc3 💰')]]
        markup = ReplyKeyboardMarkup(keyboard=buttons)
        return markup

    def catalog_markup(self, page=1) -> ReplyKeyboardMarkup:
        buttons = []
        res = self.db.get_all_products()
        for id_, title, price in res[(page - 1) * self.products_on_page:min(len(res), page * self.products_on_page)]:
            buttons.append([KeyboardButton(text=title)])

        arrows = []
        if page != 1:
            arrows.append(KeyboardButton(text='⬅️ Pr3v'))
        if min(len(res), page * self.products_on_page) != len(res):
            arrows.append(KeyboardButton(text='N3x7 ➡️'))
        buttons.append(arrows)
        buttons.append([KeyboardButton(text='Back')])
        markup = ReplyKeyboardMarkup(keyboard=buttons)
        return markup

    @staticmethod
    def basket_markup() -> ReplyKeyboardMarkup:
        buttons = [[KeyboardButton(text='P4ym3n7')],
                   [KeyboardButton(text='Cl34r b45k37')]]
        markup = ReplyKeyboardMarkup(keyboard=buttons)
        return markup

    @staticmethod
    def product_info_markup(title) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Buy pr0duc7 ✅', callback_data=f'buy_{title}'[:25])]])

    @staticmethod
    def confirm_purchase(title):
        buttons = [[InlineKeyboardButton(text='C0nf1rm purch453 ✅', callback_data=f'confirm_{title}'),
                    InlineKeyboardButton(text='B4ck ❌', callback_data='back')]]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
