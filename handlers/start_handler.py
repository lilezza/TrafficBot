from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from state import LoginState
from api.marzneshin_api import get_admin_token, check_sudo_by_username

router = Router()
sessions = {}  # user_id -> {"username": ..., "password": ..., "token": ...}

@router.message(F.text == "/start")
async def start_command(message: Message, state: FSMContext):
    await message.answer("👋 سلام! لطفاً نام کاربری پنل را وارد کنید:")
    await state.set_state(LoginState.waiting_for_username)

@router.message(LoginState.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("🔐 لطفاً رمز عبور را وارد کنید:")
    await state.set_state(LoginState.waiting_for_password)

@router.message(LoginState.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    data = await state.get_data()
    username = data.get("username")
    password = message.text

    try:
        token = await get_admin_token(username, password)
        is_sudo = await check_sudo_by_username(token, username)
        if not is_sudo:
            raise Exception("⛔ فقط ادمین‌های SUDO اجازه ورود دارند.")


        sessions[message.from_user.id] = {
            "username": username,
            "password": password,
            "token": token
        }
        await state.clear()


        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👤 لیست ادمین‌ها", callback_data="list_admins")],
            [InlineKeyboardButton(text="🚪 خروج از حساب", callback_data="logout")]
        ])

        await message.answer(
            f"✅ <b>با موفقیت وارد شدید.</b>\n\n"
            f"سلام <b>{username}</b>! 🙋‍♂️\n"
            f"به ربات دریافت ترافیک خوش آمدید.\n\n"
            f"از گزینه‌های زیر استفاده کن 👇",
            reply_markup=keyboard
        )

    except Exception as e:
        await message.answer("❌ ورود ناموفق بود. لطفاً دوباره تلاش کنید با دستور /start")
        await state.clear()
