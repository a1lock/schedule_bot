from sqlalchemy import select
from database.core import async_session
from database.models import User, Profile, Lesson

async def get_user_profile(tg_id: int):
    """Получает профиль пользователя по его Telegram ID"""
    async with async_session() as session:
        query = select(Profile).join(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

async def create_or_update_user(tg_id: int, username: str, group_name: str):
    """Создает пользователя и профиль или обновляет существующий"""
    async with async_session() as session:
        # Ищем юзера
        user_query = select(User).where(User.tg_id == tg_id)
        user = (await session.execute(user_query)).scalar_one_or_none()
        
        if not user:
            user = User(tg_id=tg_id, username=username)
            session.add(user)
            await session.flush() # Получаем ID юзера
            
        # Ищем или создаем профиль
        profile_query = select(Profile).where(Profile.user_id == user.id)
        profile = (await session.execute(profile_query)).scalar_one_or_none()
        
        if not profile:
            profile = Profile(user_id=user.id, group_name=group_name)
            session.add(profile)
        else:
            profile.group_name = group_name
            
        await session.commit()

async def get_all_groups():
    """Возвращает список всех уникальных групп из базы"""
    async with async_session() as session:
        query = select(Lesson.group_name).distinct()
        result = await session.execute(query)
        return sorted([r for r in result.scalars().all()])