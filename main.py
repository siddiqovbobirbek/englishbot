import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters
from oxfordLookup import getDefinitions
from googletrans import Translator
translator = Translator()


API_TOKEN = '5877282476:AAGnMyFvYGACfBdB-EB10BocirZJDFUna5s'

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, proxy=None, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user = message.from_user
    full_name = user.first_name
    await message.reply(f"Assalomu alaykum, {full_name}!!!  \nBotimizga Xush Kelibsiz!")



@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Inglizcha Biror So'z Kiriting! \nMen Sizga Tushuntirib Beraman!")


@dp.message_handler(~filters.Text(startswith='/'))
async def tarjimon(message: types.Message):
    lang = translator.detect(message.text).lang
    if len(message.text.split()) > 1:
        dest = 'uz' if lang == 'en' else 'en'
        await message.reply(translator.translate(message.text, dest).text)

    else:
        if lang=='en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text

        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply("Bunday so'z topilmadi!")


@dp.message_handler(commands='admin')
async def get_members(message: types.Message):
    chat_id = message.chat.id
    print("Message chat id", chat_id)
    members = await bot.get_chat_members_count(chat_id=chat_id)
    print("Members", members)
    await message.reply(f"Your bot has {members}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

