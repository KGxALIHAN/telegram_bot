from aiogram import Router, types
from aiogram.filters import Command
import random

start_router = Router()

@start_router.message(Command('myinfo'))
async def myinfo(message: types.Message):
    user = message.from_user
    last_name = user.last_name
    name = user.first_name
    user_id = user.id
    await message.answer(f'Имя: {name} Фамилия: {last_name} id: {user_id}')

random_name_list = ['Alihan', 'Kazy']

@start_router.message(Command('random'))
async def random_name(message: types.Message):
    name = random.choice(random_name_list)
    await message.answer(name)