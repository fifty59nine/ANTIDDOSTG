from ANTIDDOSTG.models import antiddostg
from aiogram.bot import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from threading import Thread
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType

ddos = antiddostg.ANTIDDOSTG(autoban=True, timeout=5, limit=10, autobantime=60)
bot = Bot("TOKEN")
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def main(message: Message):
    k = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    k.add(KeyboardButton("GET"), KeyboardButton("SET"))
    await message.answer("HELLO!", reply_markup=k)


@dp.message_handler(content_types=ContentType.TEXT)
async def txt(message: Message):
    if not ddos.ddos_message(message):
        print(ddos.ddosers)
        print(ddos.messages_ddos)
        return
    if message.text == "GET":
        await message.answer("Take it!")
    elif message.text == "SET":
        await message.answer("Ok!")
    else:
        await message.answer("Idk what is it!")

if __name__ == '__main__':
    t = Thread(target=ddos.start_service)
    t.start()
    executor.start_polling(dp)

