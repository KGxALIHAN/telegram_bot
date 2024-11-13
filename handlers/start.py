from aiogram import Router, F, types
from aiogram.filters import Command
from handlers.review_dialog import opros_router, start_opros  
from aiogram.fsm.context import FSMContext

start_kb = Router()

@start_kb.message(Command("start"))
async def start(message: types.Message):
    msg = message.from_user
    name = msg.first_name
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="инстаграм курсов",
                    url="https://www.instagram.com/geeks_edu?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
                ),
                types.InlineKeyboardButton(
                    text="инстаграм друга",
                    url="https://www.instagram.com/kkanybek_?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Оставьте отзыв",
                    callback_data="review" 
                )
            ]
        ]
    )
    await message.answer(f"привет {name}", reply_markup=kb)

@start_kb.callback_query(F.data == "review")
async def review_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Начнем опрос...")
    await start_opros(callback.message, state) 
