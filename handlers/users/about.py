from aiogram.types import Message
from loader import dp, private
from aiogram.filters import Command

@dp.message(Command("about"), private)
async def about_command(message: Message):
    about_text = (
        "<b>🤖 Guruh Moderatsiya Boti haqida</b>\n\n"
        "Ushbu bot guruhingizni tartibda saqlash va boshqarishni osonlashtiradi. Quyidagi imkoniyatlar mavjud:\n\n"
        "🔹 <b>Avtomatik Xabarlar:</b>\n"
        "• Yangi a'zolar qo‘shilganda yoki chiqib ketganda xabar yuboriladi.\n\n"
        "🔹 <b>Foydalanuvchilarni Boshqarish:</b>\n"
        "• <code>/ban</code> - Foydalanuvchini bloklab, guruhdan chiqarish.\n"
        "• <code>/unban</code> - Ban qilingan foydalanuvchini guruhga qaytarish.\n"
        "• <code>/mute</code> - Foydalanuvchini jim qilish (ovozsiz).\n"
        "• <code>/unmute</code> - Mute holatini bekor qilish.\n\n"
        "🔹 <b>Statistika:</b>\n"
        "• <code>/myinfo</code> - Sizning shaxsiy statistikangiz.\n"
        "• <code>/userinfo</code> - Boshqa foydalanuvchi haqida ma'lumot.\n"
        "• <code>/stats</code> - Guruh statistikasi.\n\n"
        "📌 Guruhdagi harakatlar nazorat ostida bo‘ladi va tartib saqlanadi.\n\n"
        "<i>👤 Bot yaratuvchisi:</i> @Asilbek_Ismoilov_AI\n"
        "<i>📚 Qo‘shimcha ma'lumot uchun:</i> /help buyrug‘ini yuboring."
    )
    await message.answer(about_text, parse_mode="HTML")