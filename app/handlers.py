import requests
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from bs4 import BeautifulSoup

import app.keyboards as kb

router = Router()


class Registration(StatesGroup):
    username = State()
    codeword = State()


def check_instagram_subscription(username):
    url = f'https://www.instagram.com/{username}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    followers_count = soup.find('meta', attrs={'name': 'description'})['content'].split(',')[1].split(' ')[1]
    return int(followers_count.replace('.', ''))


def check_instagram_post_comments(post_url):
    response = requests.get(post_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    comments_count = soup.find('meta', attrs={'property': 'og:description'})['content'].split(',')[1].split(' ')[1]
    return int(comments_count.replace('.', ''))


def check_telegram_channel_subscription(channel_username):
    url = f'https://t.me/{channel_username}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    subscribers_count = soup.find('div', {'class': 'tgme_page_extra'}).text.split(' ')[0]
    return int(subscribers_count.replace('.', ''))


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Для получения приза нужно пройти проверку', reply_markup=kb.main)


@router.callback_query(F.data == 'verify')
async def reg_one(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.username)
    await callback.answer('')
    await callback.message.answer('Введите свой инстаграм ник')


@router.message(Registration.username)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Registration.codeword)
    await message.answer('Введите кодовое слово')


@router.message(Registration.codeword)
async def two_three(message: Message, state: FSMContext):
    await state.update_data(codeword=message.text)
    data = await state.get_data()
    await message.answer(f'Username: {data["username"]}\nCodeword: {data["codeword"]}')
    await state.clear()
