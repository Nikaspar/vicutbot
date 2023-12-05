import asyncio
import configparser
import logging
import os
import sys
from typing import Any
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile, Video
from aiogram.utils.markdown import hbold
from DownloadGoogleDrive import download_file_from_google_drive as drive_download
from jdb import Jdb

from time import sleep # del


CP = configparser.ConfigParser()
CP.read('devconf.ini')

TOKEN = CP.get('BOT', 'TOKEN')
USERS_DIR = CP.get('USERS', 'USERS_DIR')
DB = Jdb(os.path.join(USERS_DIR, 'users.json'))

# Initialize Bot instance with a default parse mode which will be passed to all API calls
BOT = Bot(TOKEN, parse_mode=ParseMode.HTML)
DP = Dispatcher()

help_text = f'1. Отправь мне видео ({hbold('до 50МБ')})\n'\
            '2. Укажи начало и конец записи которые хочешь сохранить\n'\
            'А я обрежу лишнее =)'\


class Form(StatesGroup):
    waiting_video = State()
    waiting_time = State()
    in_progress = State()


class IsVideo(Filter):
    async def __call__(self, message: Message) -> bool:  
        return message.video is not None


class IsText(Filter):
    async def __call__(self, message: Message) -> bool:  
        return message.text is not None


@DP.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> Any:
    await state.set_state(Form.waiting_video)
    chat = message.chat
    user = message.from_user
    chat_id = chat.id
    user_id = user.id
    fullname = user.full_name
    username = user.username if user.username !='' else fullname

    if not DB.is_exists_user(user_id):
        DB.add_user(user_id, chat_id, username)
        await message.answer(f'Привет, {hbold(fullname)}!\n{help_text}')
    else:
        await message.answer(f'Бот уже запущен, но если тебе нужна помощь - вот она:\n{help_text}')


@DP.message(Command('help'))
async def command_help_handler(message: Message) -> Any:
    await message.answer(help_text)


@DP.message(IsVideo(), Form.waiting_video)
async def get_video_from_user(message: Message, state: FSMContext) -> Any:
    await state.set_state(Form.waiting_time)
    video: Video = message.video
    video_dur = video.duration
    video_name = video.file_name
    user = message.from_user
    fullname = user.full_name
    username = user.username if user.username !='' else fullname
    user_uploads = os.path.join(USERS_DIR, 'uploads', f'{username}')
    
    if not os.path.exists(user_uploads):
        os.makedirs(user_uploads)
    await message.answer('Пробую загрузить видео с серверов телеграма.')
    
    try:
        await BOT.download(video, os.path.join(user_uploads, video_name))
    except TelegramBadRequest as bad_req:
        await message.answer(f'Ой, не могу скачать, слишком большое\n Я как бот могу получить только 50МБ\nПопробуй другой способ\nОтвет от телеги:{bad_req}')
    else:
        time_str = convert_seconds(video_dur)
        await message.answer(f'Отлично! Видео у меня.\nПродолжительность твоего видео {time_str}\n'\
                             f'Введи какую чать сохранить в таком виде:\n\t00:00:00 {time_str}')


@DP.message(IsText(), Form.waiting_time)
async def get_times_from_user(message: Message, state: FSMContext) -> Any:
    await message.answer('Принято! Постараюсь как можно быстрей сделать и сразу пришлю тебе =)')
    await state.set_state(Form.in_progress)
    sleep(30) # del
    await message.answer('30 сек прошло') # del
    await state.set_state(Form.waiting_video)


def convert_seconds(seconds) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)


async def main() -> None:
    await DP.start_polling(BOT)


if __name__ == '__main__':
    if not os.path.exists(USERS_DIR):
        os.mkdir(os.path.join(USERS_DIR))
        DB.init_db()

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
