import asyncio
import json
import logging
import os.path
import sys
from os import getenv
from typing import Any, Dict
import pickle

import config
import dbmanager as dm

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

TOKEN = "6781267153:AAGmWDZrL2n-qUfkR-hyyGhVzpfFfvzxxWU"

n = 0
form_router = Router()
file = open('mail.p', 'rb')
mailarray = pickle.load(file)
file.close()


class Form(StatesGroup):
    login = State()
    password = State()
    creation = State()
    mailgenend = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.login)
    await message.answer(
        "Hi there! What's your login?",
        reply_markup=ReplyKeyboardRemove(),
    )

@form_router.message(Command("test"))
async def test(message: Message):

    try:
        text_tuple = (message.text.split())
        mail = text_tuple[1]
        mail_from = text_tuple[2]

        if (mail.find('@') == -1 or mail_from.find('@') == -1) or (not 5 < len(mail) < 255) or (not 5 < len(mail_from) < 255):
            raise IndexError

        elif mail[mail.find('@'):].find('.') == -1 or mail_from[mail_from.find('@'):].find('.') == -1:
            raise IndexError

        else:

            user_id = message.from_user.id

            path_to_json = f'UsersMails/{user_id}.json'

            if not os.path.isfile(path_to_json):
                user_dict: dict = {'mail': [mail],
                             'mail_from': [mail_from]}

                with open(path_to_json, 'w') as json_file:
                    json.dump(user_dict, json_file, indent=4)

            else:

                with open(path_to_json, "r") as json_file:
                    user_dict: dict = json.load(json_file)

                    user_dict['mail'].append(mail)
                    user_dict['mail_from'].append(mail_from)

                with open(path_to_json, 'w') as json_file:
                    json.dump(user_dict, json_file, indent=4)


    except IndexError:
        await message.answer("Нет")




@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Command('delete'))
async def delete(message: Message, state: FSMContext):
    text: str = message.text.split()[-1]
    mailarray.remove(text)
    with open('mail.p', 'wb') as file:
        pickle.dump(mailarray, file)


@form_router.message(Form.login)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.password)
    login = message.text
    if login == "master":
        await message.answer("correct, now let's proceed to your password",
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("incorrect, try again",
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.login)


@form_router.message(Form.password)
async def process_password(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    password = message.text
    if password == "pass":
        await message.answer("correct, now you wanna procced with the creation of new mail?",
                             reply_markup=ReplyKeyboardMarkup(
                                 keyboard=[
                                     [
                                         KeyboardButton(text="Yes"),
                                         KeyboardButton(text="No"),
                                     ]
                                 ],
                                 resize_keyboard=True,
                             )
                             )
        await state.set_state(Form.creation)
        Valid = True
    else:
        await message.answer("incorrect")
        await state.set_state(Form.password)


@form_router.message(Form.creation, F.text.casefold() == "yes")
async def process_creation_yes(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.mailgenend)
    await message.answer("Cool, so let's begin, then. \nWhat will be your e-mail login?",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("Just type like this {You write this part}@apethrone.ru")


@form_router.message(Form.creation, F.text.casefold() == "no")
async def process_creation_no(message: Message, state: FSMContext) -> None:
    await message.answer("Then why would you even log in bro? Just leave...",
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()


@form_router.message(Form.creation)
async def process_creation_unexpected(message: Message, state: FSMContext):
    await message.answer("Bro just doesn't see the context menu, does he?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="Yes"),
                                     KeyboardButton(text="No"),
                                 ]
                             ],
                             resize_keyboard=True,
                         )
                         )
    await state.set_state(Form.creation)


@form_router.message(Form.mailgenend)
async def mail_end(message: Message, state: FSMContext):
    name = message.text
    if name in mailarray:
        await message.answer("already exists")
    else:
        mailarray.append(name)

        user_id: int = message.from_user.id
        mail = "google@gmail.com"
        mailadreesfrom: str = f"{name.lower()}@apethrone.ru"

        dm.register_user(user_id=user_id, mail=mail, mailaddressfrom=mailadreesfrom)

        await message.answer("You're newly generated email address is " + name.lower() + "@apethrone.ru", sep="")
        with open('mail.p', 'wb') as file:
            pickle.dump(mailarray, file)


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    name = data["name"]
    language = data.get("language", "<something unexpected>")
    text = f"I'll keep in mind that, {html.quote(name)}, "
    text += (
        f"you like to write bots with {html.quote(language)}."
        if positive
        else "you don't like to write bots, so sad..."
    )
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)
    dm.create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
