from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User


async def add_user(user_id: int, first_name: str, last_name: str, username: str, email: str, status: str):
    try:
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                    email=email, status=status)
        await user.create()
    except UniqueViolationError:
        print('User cant be created')


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count


async def select_user(user_id: int):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def delete_user(user_id: int):
    user = await User.get(user_id)
    await user.delete()


async def update_user_status(user_id: int, status: str):
    user = await User.query.where(User.user_id == user_id).gino.first()
    await user.update(status=status).apply()


async def update_user_email(user_id: int, email: str):
    user = await User.query.where(User.user_id == user_id).gino.first()
    await user.update(email=email).apply()
