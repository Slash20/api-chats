from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Chat, Message
from src.schemas import ChatCreate, ChatOut, MessageOut, MessageCreate, ChatWithMessages
from src.database import get_db

router = APIRouter(prefix="/chats", tags=["Chats"])

@router.post("/", response_model=ChatOut, status_code=201)
async def create_chat(
        data: ChatCreate,
        db: AsyncSession = Depends(get_db)) -> ChatOut:
    chat = Chat(title=data.title.strip())
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


@router.post("/{chat_id}/messages/", response_model=MessageOut, status_code=201)
async def create_message(
        chat_id: int,
        data: MessageCreate,
        db: AsyncSession = Depends(get_db)) -> MessageOut:

    chat = await db.get(Chat, chat_id)

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    msg = Message(chat_id=chat_id, text=data.text)
    db.add(msg)
    await db.commit()
    await db.refresh(msg)

    return MessageOut.model_validate(msg)


@router.get("/{chat_id}", response_model=ChatWithMessages, status_code=200)
async def get_chat(
    chat_id: int,
    limit: int = Query(default=20, le=100, ge=1),
    db: AsyncSession = Depends(get_db),
) -> ChatWithMessages:
    chat = await db.get(Chat, chat_id)

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    stmt = (
        select(Message)
        .where(Message.chat_id == chat.id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )

    result = await db.execute(stmt)
    messages = result.scalars().all()

    chat_out = ChatOut.model_validate(chat)
    messages_out: list[MessageOut] = [MessageOut.model_validate(m) for m in messages]

    return ChatWithMessages(chat=chat_out, messages=messages_out)


@router.delete("/{chat_id}", status_code=204)
async def delete_chat(chat_id: int, db: AsyncSession = Depends(get_db)) -> None:

    chat = await db.get(Chat, chat_id)

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    await db.delete(chat)
    await db.commit()