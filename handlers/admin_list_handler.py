from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from api.marzneshin_api import get_admins

router = Router()

@router.callback_query(lambda c: c.data == "list_admins")
async def list_admins(callback: CallbackQuery, session: dict):
    try:
        username = session.get("username")
        password = session.get("password")

        data = await get_admins(username, password)
        admins = data.get("items", [])

        if not admins:
            await callback.message.edit_text("⚠️ هیچ ادمینی پیدا نشد.")
            return

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=admin["username"], callback_data=f"admin:{admin['username']}")]
                for admin in admins
            ] + [[InlineKeyboardButton(text="🔙 بازگشت", callback_data="back_to_home")]]
        )

        await callback.message.edit_text("👤 لیست ادمین‌ها:", reply_markup=keyboard)

    except Exception as e:
        await callback.message.edit_text("❌ خطا در دریافت لیست ادمین‌ها")
        print("Error in list_admins:", e)

@router.callback_query(lambda c: c.data == "back_to_home")
async def back_to_home(callback: CallbackQuery, session: dict):
    username = session.get("username", "کاربر")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 لیست ادمین‌ها", callback_data="list_admins")],
        [InlineKeyboardButton(text="🚪 خروج از حساب", callback_data="logout")]
    ])

    await callback.message.edit_text(
        f"سلام <b>{username}</b> دوباره! 👋\n"
        "به منوی اصلی برگشتی. از گزینه‌های زیر استفاده کن 👇",
        reply_markup=keyboard
    )

@router.callback_query(lambda c: c.data == "logout")
async def logout(callback: CallbackQuery):
    from handlers.start_handler import sessions
    sessions.pop(callback.from_user.id, None)

    await callback.message.edit_text("✅ شما با موفقیت از حساب خارج شدید.\nبرای ورود مجدد /start را بزنید.")
