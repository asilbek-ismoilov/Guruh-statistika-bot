from aiogram import F
from time import time
from aiogram.filters import and_f
from loader import dp, db, supergroup, bot, ADMINS
from filters.admin import IsBotAdminFilter
from aiogram.types import Message, ChatPermissions, input_file, ChatMemberAdministrator


# @dp.message(F.text=="/members")
# async def get_group_members(message: Message):
#     print("salom")
#     chat_id = message.chat.id
#     count = await bot.get_chat_member_count(chat_id)
#     await message.answer(f"Guruhda {count} ta a'zo bor.")


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

@dp.message(and_f(F.reply_to_message, F.text=="/mute"), supergroup, IsBotAdminFilter(ADMINS))
async def mute_user(message:Message):
    user_id =  message.reply_to_message.from_user.id
    permission = ChatPermissions(can_send_messages=False)

    until_date = int(time()) + 60 
    
    await message.chat.restrict(user_id=user_id, permissions=permission, until_date=until_date)
    await message.answer(f"{message.reply_to_message.from_user.first_name} 1 minutga blocklandingiz")

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


