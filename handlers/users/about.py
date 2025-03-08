from aiogram.types import Message
from loader import dp, private
from aiogram.filters import Command

@dp.message(Command("about"))
async def about_command(message: Message):
    about_text = (
        "<b>Guruh bilan ishlash Boti haqida:</b>\n\n"
        "Ushbu bot guruh moderatsiyasi va boshqaruvi uchun yaratilgan bo'lib, quyidagi asosiy funksiyalarni bajaradi:\n"
        "• Yangi a'zolar qo'shilganda va chiqib ketganda avtomatik xabar yuborish.\n"
        "• Foydalanuvchilarni ban, unban, mute, unmute qilish imkoniyati.\n"
        "• Guruh rasmiga o'zgartirish kiritish (/setphoto).\n"
        "• Shaxsiy statistikangizni (/my_info) va umumiy guruh statistikasi (/stats) orqali ko'rish.\n\n"
        "<i>Bot yaratuvchisi: Sizning ism yoki kompaniya nomingiz</i>\n"
        "<i>Qo'shimcha ma'lumot uchun /help buyrug'ini bosing.</i>"
    )
    await message.answer(about_text, parse_mode="HTML")