from loader import dp, private
from aiogram.types import Message
from aiogram.filters import Command

@dp.message(Command("help"), private)
async def help_command(message: Message):
    help_text = (
        "<b>📋 Guruh Boti Buyruqlari</b>\n\n"
        "Quyidagi buyruqlar orqali guruhni boshqarishingiz mumkin:\n\n"
        "🔧 <b>Asosiy buyruqlar:</b>\n"
        "• /help - Barcha buyruqlar ro'yxatini ko'rsatadi\n\n"
        "👮‍♂️ <b>Foydalanuvchini boshqarish:</b>\n"
        "• /ban - Foydalanuvchini ban qiladi va guruhdan chiqaradi\n"
        "• /unban - Ban qilingan foydalanuvchini tiklaydi\n"
        "• /mute - Foydalanuvchini ovozsiz (mute) qiladi\n"
        "• /unmute - Mute holatini bekor qiladi\n\n"
        "📊 <b>Statistika:</b>\n"
        "• /myinfo - Shaxsiy faoliyatingiz (kimlarni qo'shgansiz)\n"
        "• /userinfo - Foydalanuvchi faoliyatinni ko'rsatadi\n"
        "• /stats - Guruh statistikasi (faqat adminlar uchun)\n\n"
        "📥 Guruhga a’zo qo‘shilganda yoki chiqib ketganda avtomatik xabar yuboriladi.\n\n"
        "⚠️ <i>Diqqat:</i> So‘kinish va nomaqbul xatti-harakatlarga ruxsat berilmaydi. Hurmat saqlang! 🤝"
    )
    await message.answer(help_text, parse_mode="HTML")