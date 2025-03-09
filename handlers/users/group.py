import asyncio
from aiogram import F
from loader import db,dp, ADMINS
from aiogram.types import Message
from filters.admin import IsBotAdminFilter

# Yangi foydalanuvchi qo'shilganda

@dp.message(F.new_chat_members)
async def new_member(message: Message):
    adder = message.from_user  
    group_id = message.chat.id 

    for user in message.new_chat_members:
        adder_id = adder.id
        user_id = user.id
        user_full_name = user.full_name

        existing_user = db.get_user_by_id(user_id, group_id)

        if not existing_user:
            add_id = 0 if adder_id == user_id else adder_id
            db.add_group_user(telegram_id=user_id, full_name=user_full_name, add_id=add_id, group_id=group_id)

        
        msg = await message.answer(f"👋 {user_full_name}, guruhga xush kelibsiz 🎉")

    await message.delete()

    await asyncio.sleep(120)
    await msg.delete()

# Foydalanuvchi chiqib ketsa

@dp.message(F.left_chat_member)
async def left_member(message: Message):
    left_user = message.left_chat_member
    user_id = left_user.id
    group_id = message.chat.id

    db.delete_group_user(user_id, group_id)

    msg = await message.answer(f"{left_user.full_name}, guruhni tark etdi. Xayr 👋")

    await message.delete()
    await asyncio.sleep(120)
    await msg.delete()


@dp.message(F.text == "/my_info")
async def my_info(message: Message):
    await message.delete()
    user_id = message.from_user.id
    group_id = message.chat.id
    full_name = message.from_user.full_name
    
    added_count = db.get_added_count(user_id, group_id)
    
    text = (
        f"<blockquote><a href='tg://user?id={user_id}'>{full_name}</a> guruhdagi statistikangiz:</blockquote>\n\n"
        "📊 <b>Sizning statistikangiz:</b>\n"
        f"👥 Siz jami <b>{added_count}</b> ta odam qo'shgansiz"
    )
    msg = await message.answer(text, parse_mode="HTML")

    await asyncio.sleep(60)
    await msg.delete()

# @dp.message(F.text == "/stats", IsBotAdminFilter(ADMINS))
# async def stats(message: Message):
#     await message.delete()
#     group_id = message.chat.id
    
#     # Berilgan guruh uchun barcha foydalanuvchilarning taklif (invite) statistikasi
#     stats_list = db.all_added_count(group_id)
    
#     lines = ["<blockquote>📊 Guruhdagi statistikasi:</blockquote>", ""]
#     for telegram_id, full_name, invite_count in stats_list:
#         lines.append(f"👤 <b><a href='tg://user?id={telegram_id}'>{full_name}</a></b> - <b>{invite_count}</b> ta odam qo'shgan")
    
#     text = "\n".join(lines)
#     msg = await message.answer(text, parse_mode="HTML")
#     await asyncio.sleep(60)
#     await msg.delete()

@dp.message(F.text == "/stats", IsBotAdminFilter(ADMINS))
async def stats(message: Message):
    await message.delete()
    group_id = message.chat.id
    
    # Berilgan guruh uchun eng ko‘p odam qo‘shgan 10 ta foydalanuvchi statistikasi
    stats_list = db.all_added_count(group_id)
    
    lines = ["<blockquote>📊 Guruhdagi statistikasi:</blockquote>", ""]
    for telegram_id, full_name, invite_count in stats_list:
        lines.append(f"👤 <b><a href='tg://user?id={telegram_id}'>{full_name}</a></b> - <b>{invite_count}</b> ta odam qo‘shgan")
    
    text = "\n".join(lines)
    msg = await message.answer(text, parse_mode="HTML")
    await asyncio.sleep(60)
    await msg.delete()