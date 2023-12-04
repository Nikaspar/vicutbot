import asyncio
import configparser
import json
import logging
import os
import sys
from typing import Any
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import Message, FSInputFile, Video
from aiogram.utils.markdown import hbold
from DownloadGoogleDrive import download_file_from_google_drive as drive_download
from jdb import Jdb


DP = Dispatcher()

CP = configparser.ConfigParser()
CP.read('devconf.ini')

TOKEN = CP.get('BOT', 'TOKEN')
USERS_DIR = CP.get('USERS', 'USERS_DIR')
DB = Jdb(os.path.join(USERS_DIR, 'users.json'))

help_text = '1. Отправь мне видео\n'\
            '2. Укажи начало и конец записи которые хочешь сохранить\n'\
            'В таком формате: 01.04.09\n'\
            'А я обрежу лишнее =)'\


class IsVideo(Filter):
    async def __call__(self, message: Message) -> bool:  
        return isinstance(message, Video)


@DP.message(CommandStart())
async def command_start_handler(message: Message) -> None:
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
async def command_help_handler(message: Message) -> None:
    await message.answer(help_text)


@DP.message(IsVideo())
async def get_video_from_user(message: Message) -> None:
    print(message)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await DP.start_polling(bot)


if __name__ == '__main__':
    if not os.path.exists(USERS_DIR):
        os.mkdir(os.path.join(USERS_DIR))
        DB.init_db()

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
