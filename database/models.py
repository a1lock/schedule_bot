from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import BigInteger, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class StudyForm(str, Enum):
    FULL_TIME = "Очная"
    PART_TIME = "Очно-заочная"

class EduLevel(str, Enum):
    BACHELOR = "Бакалавриат"
    SPECIALIST = "Специалитет"
    MAGISTER = "Магистратура"
    POSTGRADUATE = "Аспирантура"

class LessonParity(str, Enum):
    ALWAYS = "always" # Каждую неделю
    ODD = "odd"       # Нечетная (Верх / Числитель)
    EVEN = "even"     # Четная (Низ / Знаменатель)

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(64))
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    profile: Mapped["Profile"] = relationship(back_populates="user", cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course: Mapped[int] = mapped_column(Integer, default=1)
    group_name: Mapped[str] = mapped_column(String(255), index=True) 
    study_form: Mapped[StudyForm] = mapped_column(default=StudyForm.FULL_TIME)
    edu_level: Mapped[EduLevel] = mapped_column(default=EduLevel.BACHELOR)
    user: Mapped["User"] = relationship(back_populates="profile")

class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(String(255), index=True)
    day_of_week: Mapped[int] = mapped_column(Integer)
    lesson_number: Mapped[int] = mapped_column(Integer)
    subject: Mapped[str] = mapped_column(String(1024)) # С запасом
    lesson_type: Mapped[Optional[str]] = mapped_column(String(255))
    teacher: Mapped[Optional[str]] = mapped_column(String(1024)) # С запасом
    room: Mapped[Optional[str]] = mapped_column(String(255))
    parity: Mapped[LessonParity] = mapped_column(String(20), default=LessonParity.ALWAYS)
    week_mask: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
