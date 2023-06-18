import re
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data import config
from loader import dp

from filters import IsPrivate
from states import Registration
from utils.db_api import quick_commands as commands
from utils.misc import rate_limit

from email_sender import send_code


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), CommandStart())
async def command_start(message: types.Message):
    if message.from_user.id not in config.admins_id:
        try:
            registration_new_kb = InlineKeyboardMarkup(row_width=3,
                                                       inline_keyboard=[
                                                            [
                                                                 InlineKeyboardButton(text='Новый email', callback_data='new_registration'),
                                                            ],
                                                       ])
            user = await commands.select_user(message.from_user.id)
            if user.status == 'active':
                await message.answer(f'Приветствую, {user.first_name}\n'
                                     f'Вы уже зарегистрировались и подтвердили электронную почту!', reply_markup=registration_new_kb)
            elif user.status == 'banned':
                await message.answer('Вы заблокированы и не имеете доступа к данному боту')
            else:
                await message.answer('Вы не подтвердили email', reply_markup=registration_new_kb)
        except Exception:
            await message.answer(f'Приветствую, {message.from_user.first_name}! Вы начали регистрацию.\n'
                                 'Введите ваш email (например, example@mail.com):')
            await Registration.email.set()
    else:
        await message.answer(f'Приветствую, {message.from_user.first_name}\n'
                             f'Вы являетесь администратором. \n'
                             f'Для получения информации о ваших возможностях, используйте команду /help')


@dp.message_handler(state=Registration.email)
async def email_state(message: types.Message, state: FSMContext):
    answer = message.text
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, answer):
        await state.update_data(email=answer)
        code = random.randint(100000, 999999)
        await send_code(answer, str(code))
        await message.answer(f'Ваш email {answer}\n'
                             f'На него был отправлен 6-значный код\n'
                             f'Введите ваш код подтверждения:')
        await commands.add_user(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                email=answer,
                                status=str(code))
        await Registration.confirmation_code.set()
    else:
        await message.answer('Невалидный email')


@dp.message_handler(state=Registration.confirmation_code)
async def confirmation_code_state(message: types.Message, state: FSMContext):
    answer = message.text
    user = await commands.select_user(message.from_user.id)
    if answer == user.status:
        await message.answer("Вы успешно зарегистрированы!")
        await commands.update_user_status(message.from_user.id, 'active')
    else:
        await message.answer('Неверный код подтведждения')

    await state.finish()


@dp.callback_query_handler(text='new_registration')
async def new_registration(call: CallbackQuery):
    await commands.delete_user(call.from_user.id)
    await call.message.answer(f'Вы начали новую регистрацию.\n'
                              f'Данные о предыдущем аккаунте были удалены\n'
                              'Введите ваш новый email (например, example@mail.com):')
    await Registration.email.set()
