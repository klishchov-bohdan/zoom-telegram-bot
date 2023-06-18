async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)

    import filters
    filters.setup(dp)

    from loader import db
    from utils.db_api.db_gino import on_startup
    print('PostgreSQL connection...')
    await on_startup(dp)

    # print('deleting db')
    # await db.gino.drop_all()

    print('creating tables')
    await db.gino.create_all()
    print('Complete!')

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)
    print('bot started')


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup)
