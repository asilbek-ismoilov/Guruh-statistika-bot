import asyncio
from aiogram import F
from aiogram.filters import and_f
from aiogram.types import Message
from loader import db,dp, group, supergroup, bot, ADMINS

# Yangi foydalanuvchi qo'shilganda

@dp.message(F.new_chat_members, group | supergroup)
async def new_member(message: Message):
    adder = message.from_user  
    group_id = message.chat.id 

    for user in message.new_chat_members:
        adder_id = adder.id
        user_id = user.id
        user_full_name = user.full_name
        adder_full_name = adder.full_name

        existing_user = db.get_user_by_id(user_id, group_id)
        adder_user = db.get_user_by_id(adder_id, group_id)

        if not adder_user:
            db.add_group_user(telegram_id=adder_id, full_name=adder_full_name, add_id=0, group_id=group_id)

        if not existing_user:
            add_id = 0 if adder_id == user_id else adder_id
            db.add_group_user(telegram_id=user_id, full_name=user_full_name, add_id=add_id, group_id=group_id)

        
        msg = await message.answer(f"👋 {user_full_name}, guruhga xush kelibsiz 🎉")

    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        text = f"Qo'shilish xabar o'chirishda xatolik: {e}"
        for admin in ADMINS:
            await bot.send_message(chat_id=int(admin),text=text)
        print(text)

    await asyncio.sleep(120)
    await msg.delete()

# Foydalanuvchi chiqib ketsa

@dp.message(F.left_chat_member, group | supergroup)
async def left_member(message: Message):
    left_user = message.left_chat_member
    user_id = left_user.id
    group_id = message.chat.id

    db.delete_group_user(user_id, group_id)

    try:
        msg = await message.answer(f"{left_user.full_name}, guruhni tark etdi. Xayr 👋")
    except:
        print("Bot guruhdan chiqarilgan, xabar yuborilmadi.")

    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        text = f"Tark etgan xabar o'chirishda xatolik: {e}"
        for admin in ADMINS:
            await bot.send_message(chat_id=int(admin),text=text)
        print(text)

    await asyncio.sleep(120)
    await msg.delete()


@dp.message(F.text.in_({"/myinfo", "/myinfo@Gopihelper_bot"}), group | supergroup)
async def my_info(message: Message):
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        text = f"my_info xabar o'chirishda xatolik: {e}"
        for admin in ADMINS:
            await bot.send_message(chat_id=int(admin),text=text)
        print(text)
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


@dp.message(and_f(F.reply_to_message, F.text.in_({"/userinfo", "/userinfo@Gopihelper_bot"})), group | supergroup)
async def userinfo(message: Message):
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        text = f"userinfo xabar o'chirishda xatolik: {e}"
        for admin in ADMINS:
            await bot.send_message(chat_id=int(admin),text=text)
        print(text)

    user_id = message.reply_to_message.from_user.id
    group_id = message.chat.id
    full_name = message.from_user.full_name
    
    added_count = db.get_added_count(user_id, group_id)
    
    text = (
        f"<blockquote><a href='tg://user?id={user_id}'>{full_name}</a> guruhdagi statistikangiz:</blockquote>\n\n"
        f"👥 <a href='tg://user?id={user_id}'>{full_name}</a> jami <b>{added_count}</b> ta odam qo'shgansiz"
    )
    msg = await message.answer(text, parse_mode="HTML")

    await asyncio.sleep(60)
    await msg.delete()


@dp.message(F.text.in_({"/stats", "/stats@Gopihelper_bot"}), group | supergroup)
async def stats(message: Message):
    # Chatdagi adminlarni olish
    chat_admins = await bot.get_chat_administrators(message.chat.id)
    admin_ids = {admin.user.id for admin in chat_admins}  # Adminlar ID ro‘yxati
    count = await message.chat.get_member_count()
    
    # Foydalanuvchi admin yoki guruh egasi ekanligini tekshirish
    if message.from_user.id not in admin_ids:
        try:
            await message.delete()
        except Exception as e:
            text = f"stats admin xabar o'chirishda xatolik: {e}"
            for admin in ADMINS:
                await bot.send_message(chat_id=int(admin),text=text)
            print(text)
        msg = await message.answer("❌ Siz admin emassiz!")
        await asyncio.sleep(5)
        await msg.delete()
        return

    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        text = f"stats xabar o'chirishda xatolik: {e}"
        for admin in ADMINS:
            await bot.send_message(chat_id=int(admin),text=text)
        print(text)
    group_id = message.chat.id
    
    # Berilgan guruh uchun eng ko‘p odam qo‘shgan 10 ta foydalanuvchi statistikasi
    stats_list = db.all_added_count(group_id)
    
    lines = [f"<blockquote>📊 Guruhdagi statistikasi:</blockquote> <b>Guruhda {count}</b> ta a'zo bor", ""]
    for telegram_id, full_name, invite_count in stats_list:
        if telegram_id not in [admin.user.id for admin in chat_admins]: 
            lines.append(f"👤 <b><a href='tg://user?id={telegram_id}'>{full_name}</a></b> - <b>{invite_count}</b> ta odam qo‘shgan")
    
    text = "\n".join(lines)
    msg = await message.answer(text, parse_mode="HTML")
    await asyncio.sleep(60)
    await msg.delete()