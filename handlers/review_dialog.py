from aiogram import Router, types
from aiogram.filters import Command 
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

opros_router = Router()

class RestourantReview(StatesGroup):
    name = State()
    number = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@opros_router.message(Command('opros'))
async def start_opros(message: types.Message, state: FSMContext):
    await state.set_state(RestourantReview.name)
    await message.answer("Как вас зовут?")

@opros_router.message(RestourantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestourantReview.number)
    await message.answer("Напишите ваш номер телефона или инстаграм")

@opros_router.message(RestourantReview.number)
async def process_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await state.set_state(RestourantReview.visit_date)
    await message.answer("Дата вашего посещения")

@opros_router.message(RestourantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    await state.set_state(RestourantReview.food_rating)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Плохо"), KeyboardButton(text="Удовлетворительно")],
            [KeyboardButton(text="Хорошо"), KeyboardButton(text="Отлично")],
            [KeyboardButton(text="Супер")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Как вы оцениваете качество еды?", reply_markup=keyboard)

@opros_router.message(RestourantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    await state.update_data(food_rating=message.text)
    await state.set_state(RestourantReview.cleanliness_rating)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Плохо"), KeyboardButton(text="Удовлетворительно")],
            [KeyboardButton(text="Хорошо"), KeyboardButton(text="Отлично")],
            [KeyboardButton(text="Супер")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Как вы оцениваете чистоту заведения?", reply_markup=keyboard)

@opros_router.message(RestourantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    await state.update_data(cleanliness_rating=message.text)
    await state.set_state(RestourantReview.extra_comments)
    await message.answer("Оставьте ваш отзыв о нашем ресторане")

@opros_router.message(RestourantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    data = await state.get_data()
    review_summary = (
        f"Отзыв:\n"
        f"Имя: {data['name']}\n"
        f"Контакт: {data['number']}\n"
        f"Дата визита: {data['visit_date']}\n"
        f"Оценка еды: {data['food_rating']}\n"
        f"Чистота: {data['cleanliness_rating']}\n"
        f"Комментарий: {data['extra_comments']}"
    )
    await message.answer(review_summary)
    await state.clear()
