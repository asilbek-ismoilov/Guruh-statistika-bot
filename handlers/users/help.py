from loader import dp, private
from aiogram.types import Message
from aiogram.filters import Command

#help commands
@dp.message(Command("help"), private)
async def help_commands(message:Message):
    await message.answer("🔥 Buyruqlar \nBotdan foydalanish uchun ... \n /about - Bot haqida \n\nAdmin bilan bog'lanmoqchi bo'lsangiz \"/xabar\" tugmasini bosing va ✉️ Xabaringizni yozib qoldiring ! ")
