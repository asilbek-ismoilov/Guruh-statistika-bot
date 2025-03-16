from loader import dp, private
from aiogram.types import Message
from aiogram.filters import Command

@dp.message(Command("help"), private)
async def help_command(message: Message):
    help_text = (
        "<b>Guruh Botining Buyruqlari:</b>\n\n"
        "/help - Bot buyruqlari ro'yxatini ko'rsatadi\n"
        "/ban - Foydalanuvchini guruhdan ban qiladi\n"
        "/unban - Ban qilingan foydalanuvchini qayta tiklaydi\n"
        "/mute - Foydalanuvchini guruhda ovozsiz qiladi (mute)\n"
        "/unmute - Mute o'chiriladi\n"
        "/setphoto - Guruh rasmiga o'zgartirish kiritadi\n"
        "/my_info - Sizning shaxsiy statistikangiz (qaysi odamlarni qo'shganingiz)\n"
        "/stats - Guruhdagi umumiy statistikani ko'rsatadi (faqat adminga)\n"
        "Foydalanuvchi guruhga qo'shilsa va chiqib ketsa xabar kelib turadi\n\n"
        "<i>Diqqat:</i> So'kinishga qat'iy cheklov qo'llaniladi. Iltimos, hurmatli bo'ling!"
    )
    await message.answer(help_text, parse_mode="HTML")