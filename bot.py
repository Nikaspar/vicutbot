import os
from configparser import ConfigParser
from pyrogram import Client, filters
from pyrogram.types import Message


config = ConfigParser()
config.read('devconf.ini')
api_id = config['ALL']['API_ID']
api_hash = config['ALL']['API_HASH']
bot_token = config['ALL']['TOKEN']

bot = Client(os.path.join('session', 'vicutbit'), api_id, api_hash, bot_token=bot_token)


@bot.on_message(filters.command(['start', 'help']))
def command_start(client: Client, message: Message):
    print(message)


if __name__ == '__main__':
    bot.run()
