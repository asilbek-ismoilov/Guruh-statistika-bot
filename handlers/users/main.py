import asyncio
from aiogram import F
from time import time
from aiogram.filters import and_f
from loader import dp, db, supergroup, bot, ADMINS
from filters.admin import IsBotAdminFilter
from aiogram.types import Message, ChatPermissions, input_file


# BAN BO'LISHI VA BAN DAN OCHISH

@dp.message(and_f(F.reply_to_message, F.text=="/ban"), supergroup, IsBotAdminFilter(ADMINS))
async def ban_user(message:Message):
    user_id =  message.reply_to_message.from_user.id
    await message.chat.ban_sender_chat(user_id)
    await message.answer(f"{message.reply_to_message.from_user.first_name} guruhdan chiqarib yuborilasiz.")

@dp.message(and_f(F.reply_to_message, F.text=="/unban"), supergroup, IsBotAdminFilter(ADMINS))
async def unban_user(message:Message):
    user_id =  message.reply_to_message.from_user.id
    await message.chat.unban_sender_chat(user_id)
    await message.answer(f"{message.reply_to_message.from_user.first_name} guruhga qaytishingiz mumkin.")


# Mute qilish (moslashuvchan vaqt bilan)

@dp.message(and_f(F.reply_to_message, F.text == "/mute"), IsBotAdminFilter(ADMINS))
async def mute_user(message: Message):
    await message.chat.restrict(
        user_id=message.reply_to_message.from_user.id,
        permissions=ChatPermissions(can_send_messages=False),
        until_date=int(time()) + 300
    )
    msg = await message.answer(f"{message.reply_to_message.from_user.first_name} 5 minutga bloklandi.")
    await asyncio.sleep(60)
    await msg.delete()

    
@dp.message(and_f(F.reply_to_message, F.text == "/unmute"), IsBotAdminFilter(ADMINS))
async def unmute_user(message: Message):
    await message.chat.restrict(
        user_id=message.reply_to_message.from_user.id,
        permissions=ChatPermissions(can_send_messages=True)
    )
    msg = await message.answer(f"{message.reply_to_message.from_user.first_name} yana yozishi mumkin.")
    await asyncio.sleep(60)
    await msg.delete()
# Guruh rasmini o'rnatish

@dp.message(and_f(F.reply_to_message.photo,F.text=="/setphoto"), supergroup, IsBotAdminFilter(ADMINS))
async def setphoto_group(message:Message):
    photo =  message.reply_to_message.photo[-1].file_id
    file = await bot.get_file(photo)
    file_path = file.file_path
    file = await bot.download_file(file_path)
    file = file.read()
    await message.chat.set_photo(photo=input_file.BufferedInputFile(file=file,filename="asd.jpg"))
    await message.answer("Gruh rasmi uzgardi")

    
@dp.message(F.text.startswith("/poll"), supergroup, IsBotAdminFilter(ADMINS))
async def create_poll(message: Message):
    args = message.text.split("\n")[1:]  # Savol va variantlar
    if len(args) < 3:
        return await message.answer("⛔ Iltimos, kamida 1 savol va 2 ta variant yozing.")

    question = args[0]
    options = args[1:]
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=options,
        is_anonymous=False
    )

# /poll
# Guruhda qanday o'zgarishlar kerak?
# Variant 1
# Variant 2
# Variant 3

user_warnings = {}

from time import time
xaqoratli_sozlar = {"tentak", "jinni", "to'poy", "axmoq", "ahmoq", "tupoy", "lanati", "xarom"}

@dp.message(F.chat.func(lambda chat: chat.type == "supergroup"), F.text)
async def tozalash(message: Message):
    user_id = message.from_user.id
    text = message.text.lower()

    # Agar foydalanuvchi oldin so‘kingan bo‘lsa, uning ogohlantirish sonini oshiramiz
    if user_id not in user_warnings:
        user_warnings[user_id] = 0

    # Xabarni xaqoratli so‘zlarga tekshiramiz
    for soz in xaqoratli_sozlar:
        if soz in text:
            user_warnings[user_id] += 1  # Ogohlantirishni oshiramiz
            await message.delete()  # So‘kinish xabarini o‘chirib tashlaymiz

            if user_warnings[user_id] == 1:
                first_message = await message.answer(f"{message.from_user.mention_html()} ❗ Bu birinchi ogohlantirish! Guruhda so‘kinmang.", parse_mode="HTML")
                await asyncio.sleep(60)
                await first_message.delete()
            elif user_warnings[user_id] == 2:
                until_date = int(time()) + 600  # 10 daqiqaga mute
                permission = ChatPermissions(can_send_messages=False)
                await message.chat.restrict(user_id=user_id, permissions=permission, until_date=until_date)
                second_message = await message.answer(f"{message.from_user.mention_html()} 🔇 10 daqiqaga yozish huquqingiz cheklandi!", parse_mode="HTML")
                await asyncio.sleep(60)
                await second_message.delete()
            elif user_warnings[user_id] >= 3:
                await message.chat.ban_sender_chat(user_id)  # Butun umrga ban
                third_message = await message.answer(f"{message.from_user.mention_html()} 🚫 Siz guruhdan butunlay bloklandingiz!", parse_mode="HTML")
                await asyncio.sleep(60)
                third_message.delete()
            break