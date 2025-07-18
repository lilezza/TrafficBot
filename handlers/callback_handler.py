from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from api.marzneshin_api import get_admins

router = Router()


@router.callback_query(lambda c: c.data.startswith("admin:"))
async def admin_selected(callback: CallbackQuery):
    username = callback.data.split(":")[1]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 ترافیک 24 ساعت", callback_data=f"traffic:{username}:24h")],
            [InlineKeyboardButton(text="📊 ترافیک 7 روز", callback_data=f"traffic:{username}:7d")],
            [InlineKeyboardButton(text="📊 ترافیک 30 روز", callback_data=f"traffic:{username}:30d")],
            [InlineKeyboardButton(text="📊 ترافیک 3 ماه", callback_data=f"traffic:{username}:3m")],
            [InlineKeyboardButton(text="🔙 بازگشت", callback_data="back_to_admins")]
        ]
    )

    await callback.message.edit_text(
        text=f"ادمین <b>{username}</b> رو انتخاب کردی. بازه مورد نظر رو انتخاب کن 👇",
        reply_markup=keyboard
    )
    await callback.answer()



@router.callback_query(lambda c: c.data == "back_to_admins")
async def go_back(callback: CallbackQuery, session: dict):
    try:
        username = session.get("username")
        password = session.get("password")

        if not username or not password:
            await callback.message.edit_text("❌ ابتدا با دستور /start وارد شوید.")
            return

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
        print("ERROR in go_back handler:", e)

