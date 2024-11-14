from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3
import re

class RestaurantReview(StatesGroup):
    name = State()
    phone_or_instagram = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

review_router = Router()

def is_valid_date(date_text):
    return bool(re.match(r"\d{2}\.\d{2}\.\d{4}$", date_text))

@review_router.callback_query(lambda c: c.data == 'review')
async def start_review(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RestaurantReview.name)
    await callback.message.answer("Как вас зовут?")

@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestaurantReview.phone_or_instagram)
    await message.answer("Ваш номер телефона или инстаграм?")

@review_router.message(RestaurantReview.phone_or_instagram)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(phone_or_instagram=message.text)
    await state.set_state(RestaurantReview.visit_date)
    await message.answer("Дата вашего посещения нашего заведения? (формат ДД.ММ.ГГГГ)")

@review_router.message(RestaurantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    if not is_valid_date(message.text):
        await message.answer("Пожалуйста, введите дату в формате ДД.ММ.ГГГГ.")
        return
    await state.update_data(visit_date=message.text)
    
    rating_kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=str(i), callback_data=f"food_rating:{i}") for i in range(1, 6)]
        ]
    )
    await state.set_state(RestaurantReview.food_rating)
    await message.answer("Как оцениваете качество еды? (1-5)", reply_markup=rating_kb)

@review_router.callback_query(RestaurantReview.food_rating)
async def process_food_rating(callback: types.CallbackQuery, state: FSMContext):
    rating = int(callback.data.split(":")[1])
    await state.update_data(food_rating=rating)
    
    rating_kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=str(i), callback_data=f"cleanliness_rating:{i}") for i in range(1, 6)]
        ]
    )
    await state.set_state(RestaurantReview.cleanliness_rating)
    await callback.message.answer("Как оцениваете чистоту заведения? (1-5)", reply_markup=rating_kb)

@review_router.callback_query(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(callback: types.CallbackQuery, state: FSMContext):
    rating = int(callback.data.split(":")[1])
    await state.update_data(cleanliness_rating=rating)
    
    await state.set_state(RestaurantReview.extra_comments)
    await callback.message.answer("Дополнительные комментарии/жалоба:")

@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)

    data = await state.get_data()

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO reviews (name, phone_or_instagram, visit_date, food_rating, cleanliness_rating, extra_comments)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['phone_or_instagram'], data['visit_date'],
          data['food_rating'], data['cleanliness_rating'], data['extra_comments']))
    conn.commit()
    conn.close()

    await message.answer("Спасибо за ваш отзыв!")
    await state.clear()
