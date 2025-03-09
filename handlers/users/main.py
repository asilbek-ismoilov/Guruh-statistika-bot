import re
import asyncio
from aiogram import F
from time import time
from aiogram.filters import and_f
from loader import dp, supergroup, bot, ADMINS
from filters.admin import IsBotAdminFilter
from aiogram.types import Message, ChatPermissions, input_file


# BAN BO'LISHI VA BAN DAN OCHISH

@dp.message(and_f(F.reply_to_message, F.text == "/ban"), IsBotAdminFilter(ADMINS))
async def ban_user(message: Message):
    await message.delete()
    await message.chat.ban_sender_chat(message.reply_to_message.from_user.id)
    txt = await message.answer(f"{message.reply_to_message.from_user.first_name} guruhdan chiqarildi.")
    await asyncio.sleep(60)
    await txt.delete()

@dp.message(and_f(F.reply_to_message, F.text == "/unban"), IsBotAdminFilter(ADMINS))
async def unban_user(message: Message):
    await message.delete()
    await message.chat.unban_sender_chat(message.reply_to_message.from_user.id)
    msg = await message.answer(f"{message.reply_to_message.from_user.first_name} guruhga qaytdi.")
    await asyncio.sleep(60)
    await msg.delete()

# Mute qilish (moslashuvchan vaqt bilan)

@dp.message(and_f(F.reply_to_message, F.text == "/mute"), IsBotAdminFilter(ADMINS))
async def mute_user(message: Message):
    await message.delete()
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
    await message.delete()
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
    await message.delete()
    photo =  message.reply_to_message.photo[-1].file_id
    file = await bot.get_file(photo)
    file_path = file.file_path
    file = await bot.download_file(file_path)
    file = file.read()
    await message.chat.set_photo(photo=input_file.BufferedInputFile(file=file,filename="asd.jpg"))
    await message.answer("Gruh rasmi uzgardi")

# Xaqoratli so'zlar va foydalanuvchi ogohlantirishlarini saqlash lug'ati

user_warnings = {}
xaqoratli_sozlar = {"tentak", "jinni", "to'poy", "axmoq", "ahmoq", "tupoy", "lanati", "xarom"}

@dp.message(F.text, supergroup)
async def combined_filter(message: Message):
    text = message.text.lower()
    user_id = message.from_user.id

    # Agar xabar '/' bilan boshlansa, uni o'chirib tashlaymiz
    if text.startswith("/"):
        await message.delete()
        return

    # Reklama (link) aniqlash: http:// yoki https://
    if re.search(r'https?://', message.text):
        await message.delete()  # Reklama xabarini o'chiramiz
        until_date = int(time()) + 300  # 5 daqiqa (300 soniya)
        permission = ChatPermissions(can_send_messages=False)
        await message.chat.restrict(
            user_id=user_id,
            permissions=permission,
            until_date=until_date
        )
        mute_msg = await message.answer(
            f"{message.from_user.mention_html()}, reklamadan foydalanib mumkin emas ❗\n5 minutga bloklandingiz",
            parse_mode="HTML"
        )
        await asyncio.sleep(60)
        await mute_msg.delete()
        return

    # Xabarni xaqoratli so'zlar bo'yicha tekshiramiz
    for soz in xaqoratli_sozlar:
        if soz in text:
            if user_id not in user_warnings:
                user_warnings[user_id] = 0
            user_warnings[user_id] += 1
            await message.delete()

            if user_warnings[user_id] == 1:
                first_message = await message.answer(
                    f"{message.from_user.mention_html()} ❗ Bu birinchi ogohlantirish! Guruhda so'kinmang.",
                    parse_mode="HTML"
                )
                await asyncio.sleep(60)
                await first_message.delete()
            elif user_warnings[user_id] == 2:
                until_date = int(time()) + 600  # 10 daqiqa (600 soniya)
                permission = ChatPermissions(can_send_messages=False)
                await message.chat.restrict(
                    user_id=user_id,
                    permissions=permission,
                    until_date=until_date
                )
                second_message = await message.answer(
                    f"{message.from_user.mention_html()} 🔇 10 daqiqaga yozish huquqingiz cheklandi!",
                    parse_mode="HTML"
                )
                await asyncio.sleep(60)
                await second_message.delete()
            elif user_warnings[user_id] >= 3:
                await message.chat.ban_sender_chat(user_id)  # Butun umrga bloklash
                third_message = await message.answer(
                    f"{message.from_user.mention_html()} 🚫 Siz guruhdan butunlay bloklandingiz!",
                    parse_mode="HTML"
                )
                await asyncio.sleep(60)
                await third_message.delete()
            break