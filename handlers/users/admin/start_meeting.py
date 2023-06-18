from asyncio import sleep

from aiogram import types

from data import config
from loader import dp

from filters import IsPrivate
from utils.db_api import quick_commands as commands
from utils.misc import rate_limit
from zoom import get_access_token, start_zoom_meeting


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/meeting')
async def start_meeting(message: types.Message):
    if message.from_user.id in config.admins_id:
        token = get_access_token()
        if token is not None:
            meeting_info = start_zoom_meeting(token)
            if meeting_info is not None:
                await message.answer(f'Конференция запланирована на {meeting_info["start_time"]}\n'
                                     f'Для старта перейдите по ссылке {meeting_info["start_url"]}\n'
                                     f'Другим пользователям была отправлена ссылка для подключения')
                users = await commands.select_all_users()
                for user in users:
                    await dp.bot.send_message(user.user_id, f'Конференция запланирована на {meeting_info["start_time"]}\n'
                                                            f'Ссылка для подключения: {meeting_info["join_url"]}\n'
                                                            f'Пароль для подключения {meeting_info["password"]}')
                    await sleep(0.33)
            else:
                await message.answer('Произошла ошибка при создании встречи')
        else:
            await message.answer('Произошла ошибка при получении токена')
    else:
        await message.answer('Только администратор имеет доступ к этой функции')
