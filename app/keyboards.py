from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Начать проверку', callback_data='verify')]]
                            , resize_keyboard=True, input_field_placeholder='Введите /verify')
