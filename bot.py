import asyncio
import configparser
import json
import logging
import os
import sys
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from jdb import Jdb


DP = Dispatcher()

CP = configparser.ConfigParser()
CP.read('devconf.ini')

TOKEN = CP.get('BOT', 'TOKEN')
USERS_DIR = CP.get('USERS', 'USERS_DIR')
DB = Jdb(os.path.join(USERS_DIR, 'jdb.json'))

help_text = 'Отправь мне видео, укажи начало и конец записи которые хочешь сохранить, а я обрежу лишнее =)'


@DP.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    chat = message.chat
    chat_id = message.chat.id
    fullname = message.from_user.full_name
    print(chat)
    await message.answer(f"Привет, {hbold(fullname)}!")
    await command_help_handler(message)


@DP.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    await message.answer(help_text)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await DP.start_polling(bot)


if __name__ == '__main__':
    if not os.path.exists(USERS_DIR):
        os.mkdir(os.path.join(USERS_DIR))
    if not os.path.exists(DB.get_path()):
        DB.init_db()
        # with open(os.path.join(USERS_DIR, DB), 'w+') as db:
        #     db.close()
    
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())