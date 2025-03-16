import re
import asyncio
from aiogram import F
from time import time
from aiogram.filters import and_f
from loader import dp, group, supergroup, bot, ADMINS
from filters.admin import IsBotAdminFilter
from aiogram.types import Message, ChatPermissions, input_file


# BAN BO'LISHI VA BAN DAN OCHISH

@dp.message(and_f(F.reply_to_message, F.text == "/ban"), IsBotAdminFilter(ADMINS),  group, supergroup)
async def ban_user(message: Message):
    await message.delete()
    await message.chat.ban_sender_chat(message.reply_to_message.from_user.id)
    txt = await message.answer(f"{message.reply_to_message.from_user.first_name} guruhdan chiqarildi.")
    await asyncio.sleep(60)
    await txt.delete()

@dp.message(and_f(F.reply_to_message, F.text == "/unban"), IsBotAdminFilter(ADMINS), group, supergroup)
async def unban_user(message: Message):
    await message.delete()
    await message.chat.unban_sender_chat(message.reply_to_message.from_user.id)
    msg = await message.answer(f"{message.reply_to_message.from_user.first_name} guruhga qaytdi.")
    await asyncio.sleep(60)
    await msg.delete()

# Mute qilish (moslashuvchan vaqt bilan)

@dp.message(and_f(F.reply_to_message, F.text == "/mute"), IsBotAdminFilter(ADMINS), group, supergroup)
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


@dp.message(and_f(F.reply_to_message, F.text == "/unmute"), IsBotAdminFilter(ADMINS),  group, supergroup)
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

@dp.message(and_f(F.reply_to_message.photo,F.text=="/setphoto"),  group, supergroup, IsBotAdminFilter(ADMINS))
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

# Global o'zgaruvchilar
user_warnings = {}
xaqoratli_sozlar = {"tentak", "jinni", "to'poy", "axmoq", "ahmoq", "tupoy", "lanati", "xarom"}

# Linklarni aniqlash uchun to'liq regex
link_pattern = re.compile(r"(https?://\S+|www\.\S+|\S+\.(com|uz|net|org|ru|ly|io|me|t.me|telegram.me)\S*)")

# Barcha xabarlarni superguruhda tekshirish uchun handler
@dp.message(F.text,  group, supergroup)
async def combined_filter(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Admin yoki ownerligini tekshiramiz
    chat_member = await message.chat.get_member(user_id)
    if chat_member.status in ["administrator", "creator"]:
        return  

    # **1. Forward qilingan xabarni tekshirish**
    if (message.forward_sender_name or message.forward_signature or message.forward_date or
        message.forward_from_message_id or message.forward_from_chat or message.forward_from):
        await message.delete()
        until_date = int(time()) + 300  # 5 daqiqa
        permission = ChatPermissions(can_send_messages=False)
        await message.chat.restrict(user_id=user_id, permissions=permission, until_date=until_date)
        
        mute_msg = await message.answer(
            f"{message.from_user.mention_html()}, forward qilingan xabar yuborish mumkin emas! ❗\n"
            f"5 minutga yozish huquqingiz olib tashlandi.",
            parse_mode="HTML"
        )
        await asyncio.sleep(60)
        await mute_msg.delete()
        return

    # **2. Matnli xabarlar uchun qo'shimcha tekshiruvlar**
    if message.text:  # Agar xabarda matn bo'lsa
        text = message.text.lower()
        
        # **2.1. Agar xabar '/' bilan boshlansa, uni o'chirib tashlaymiz**
        if text.startswith("/"):
            await message.delete()
            return
        
        # **2.2. Link borligini tekshirish**
        if link_pattern.search(text):
            await message.delete()
            until_date = int(time()) + 300  # 5 daqiqa
            permission = ChatPermissions(can_send_messages=False)
            await message.chat.restrict(user_id=user_id, permissions=permission, until_date=until_date)

            mute_msg = await message.answer(
                f"{message.from_user.mention_html()}, guruhda reklamadan foydalanish mumkin emas! ❗\n"
                f"5 minutga yozish huquqingiz olib tashlandi.",
                parse_mode="HTML"
            )
            await asyncio.sleep(60)
            await mute_msg.delete()
            return

        # **2.3. Xabarni xaqoratli so'zlar bo'yicha tekshirish**
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
                    await message.chat.restrict(user_id=user_id, permissions=permission, until_date=until_date)

                    mute_message = await message.answer(
                        f"{message.from_user.mention_html()} ❗ 10 daqiqaga guruhda yozish huquqingiz olib tashlandi.",
                        parse_mode="HTML"
                    )
                    await asyncio.sleep(60)
                    await mute_message.delete()
                return