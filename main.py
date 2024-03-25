import asyncio
import logging
import sys

from config import TOKEN
import dbmanager as dm

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart

from aiogram.types import (
    Message
)

import terminal as tm

form_router = Router()


@form_router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer("Type /mailadd {login}@apethrone.ru {mailaddress}")


@form_router.message(Command("mailadd"))
async def mailadd(message: Message):
    try:

        text_tuple = (message.text.split())
        mail = text_tuple[2]
        if (mail.find('@') == -1) or (not 5 < len(mail) < 255):
            raise IndexError

        elif mail[mail.find('@'):].find('.') == -1:
            raise IndexError

        else:
            user_id = message.from_user.id
            name = text_tuple[1]
            mail_from = text_tuple[1] + '@apethrone.ru'
            dm.register_user(user_id=user_id, source=mail_from, destination=mail)
            tm.add_to_ubuntu(name=name)

    except IndexError:
        await message.answer("Ошибка")


@form_router.message(Command("getuser"))
async def getuser(message: Message):
    try:
        user_id = message.from_user.id
        string = ''
        answers = dm.get_user(user_id=user_id)
        if len(answers) != 0:
            for answer in answers:
                string += f'Почта отправитель: {answer[1]} -> Почта получатель: {answer[2]}\n\n'
            await message.answer(string)
        else:
            raise IndexError
    except IndexError:
        await message.answer("Нет")


@form_router.message(Command("maildelete"))
async def maildelete(message: Message):
    try:
        mails = (message.text.split())
        mailaddressfrom = mails[1] + '@apethrone.ru'
        name = mails[1]

        dm.delete_user(source=mailaddressfrom)
        tm.delete_user(name=name)
    except IndexError:
        await message.answer("Нет")


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)
    dm.create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
