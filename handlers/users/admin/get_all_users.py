from aiogram import types

from data import config
from loader import dp

from filters import IsPrivate
from utils.db_api import quick_commands as commands
from utils.misc import rate_limit


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/users')
async def get_all_users(message: types.Message):
    if message.from_user.id in config.admins_id:
        try:
            users = await commands.select_all_users()
            for user in users:
                status = ''
                if user.status != 'banned' and user.status != 'active':
                    status = 'not confirmed'
                else:
                    status = user.status
                await message.answer(f'Имя: {user.first_name}\n'
                                     f'Email: {user.email}\n'
                                     f'Статус: {status}\n'
                                     f'username: {user.username}\n')

        except Exception:
            await message.answer('Невозможно получить список пользователей')
    else:
        await message.answer('Только администратор имеет доступ к этой функции')
