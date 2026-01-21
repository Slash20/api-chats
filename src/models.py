from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from src.database import Base

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    messages = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(String(5000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    chat = relationship("Chat", back_populates="messages")