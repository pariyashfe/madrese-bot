import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ================= تنظیمات =================
import os
TOKEN =os.getenv("7799078454:AAGCYY07ApfY3jpoauKT-Vl7-_waYo3_L74")
#TOKEN = "7799078454:AAGCYY07ApfY3jpoauKT-Vl7-_waYo3_L74"
CHANNEL_USERNAME = "@madreseyaaab"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ================= دیتابیس =================
conn = sqlite3.connect("madrese.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS resumes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    grade TEXT,
    subject TEXT,
    city TEXT,
    experience TEXT,
    degree TEXT,
    skills TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ads(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_name TEXT,
    ad_city TEXT,
    ad_grade_subject TEXT,
    num_staff TEXT,
    description TEXT,
    ad_phone TEXT
)
""")

conn.commit()

# ================= حالت‌ها =================
class Form(StatesGroup):
    choose = State()

    name = State()
    grade = State()
    subject = State()
    city = State()
    experience = State()
    degree = State()
    skills = State()
    phone = State()

    school_name = State()
    ad_city = State()
    ad_grade_subject = State()
    num_staff = State()
    description = State()
    ad_phone = State()

# ================= کیبورد عضویت =================
join_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="عضویت در کانال",
                url="https://t.me/madreseyaaab"
            )
        ],
        [
            InlineKeyboardButton(
                text="عضو شدم ✅",
                callback_data="check_join"
            )
        ]
    ]
)

# ================= کیبورد تماس =================
contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="ارسال شماره تماس", request_contact=True)]],
    resize_keyboard=True
)

# ================= بررسی عضویت =================
async def is_member(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

# ================= منو اصلی =================
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="رزومه معلم")],
            [KeyboardButton(text="آگهی استخدامی")]
        ],
        resize_keyboard=True
    )

# ================= /start =================
@dp.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()

    if not await is_member(message.from_user.id):
        await message.answer(
            "برای استفاده از ربات ابتدا عضو کانال شوید 👇",
            reply_markup=join_keyboard
        )
        return

    await message.answer(
        "سلام 👋 خوش آمدید\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=main_menu()
    )
    await state.set_state(Form.choose)

# ================= بررسی دکمه «عضو شدم» =================
@dp.callback_query(F.data == "check_join")
async def check_join_handler(callback: CallbackQuery, state: FSMContext):

    if not await is_member(callback.from_user.id):
        await callback.answer("هنوز عضو نشدی ❌", show_alert=True)
        return

    await callback.message.edit_reply_markup()  # حذف دکمه عضویت

    await callback.message.answer(
        "عضویت تایید شد ✅\nحالا یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=main_menu()
    )

    await state.set_state(Form.choose)
    await callback.answer()

# ================= انتخاب حالت =================
@dp.message(Form.choose)
async def choose_handler(message: Message, state: FSMContext):

    if message.text == "رزومه معلم":
        await message.answer("نام کامل:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.name)

    elif message.text == "آگهی استخدامی":
        await message.answer("نام آموزشگاه:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.school_name)

    else:
        await message.answer("یکی از گزینه‌ها را انتخاب کنید.")

# ================= مراحل رزومه =================
@dp.message(Form.name)
async def name_handler(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("مقطع تحصیلی:")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade_handler(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await message.answer("رشته:")
    await state.set_state(Form.subject)

@dp.message(Form.subject)
async def subject_handler(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("شهر:")
    await state.set_state(Form.city)

@dp.message(Form.city)
async def city_handler(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("سابقه کاری:")
    await state.set_state(Form.experience)

@dp.message(Form.experience)
async def exp_handler(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("مدرک تحصیلی:")
    await state.set_state(Form.degree)

@dp.message(Form.degree)
async def degree_handler(message: Message, state: FSMContext):
    await state.update_data(degree=message.text)
    await message.answer("مهارت‌ها:")
    await state.set_state(Form.skills)

@dp.message(Form.skills)
async def skills_handler(message: Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await message.answer("شماره تماس را ارسال کنید:", reply_markup=contact_keyboard)
    await state.set_state(Form.phone)

@dp.message(Form.phone)
async def phone_handler(message: Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    data = await state.get_data()

    cursor.execute("""
        INSERT INTO resumes(full_name, grade, subject, city, experience, degree, skills, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["full_name"], data["grade"], data["subject"],
        data["city"], data["experience"], data["degree"],
        data["skills"], phone
    ))
    conn.commit()

    await message.answer("✅ رزومه ثبت شد.", reply_markup=ReplyKeyboardRemove())
    await state.clear()

# ================= اجرای ربات =================
async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
