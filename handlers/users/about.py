from aiogram.types import Message
from loader import dp, private
from aiogram.filters import Command

#about commands
@dp.message(Command("about"), private)
async def about_commands(message:Message):
    await message.answer("Guruh bilan ishlaydigan bot. \nAdmin:@Asilbek_Ismoilov_AI")

