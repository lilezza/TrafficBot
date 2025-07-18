from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from api.marzneshin_api import get_total_used_traffic

router = Router()

@router.callback_query(lambda c: c.data.startswith("traffic:"))
async def show_traffic(callback: CallbackQuery, session: dict):
    _, admin_username, period = callback.data.split(":")

    try:
        username = session.get("username")
        password = session.get("password")

        if not username or not password:
            await callback.message.answer("❌ ابتدا با دستور /start وارد شوید.")
            return

        print("📦 Session inside traffic_handler:", session)

        traffic = await get_total_used_traffic(admin_username, username, password)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 بازگشت", callback_data=f"admin:{admin_username}")]
            ]
        )

        await callback.message.edit_text(
            text=f"📊 ترافیک کل کاربران ادمین <b>{admin_username}</b> در بازه <b>{period}</b>:\n<code>{traffic}</code>",
            reply_markup=keyboard
        )
        await callback.answer()

    except Exception as e:
        await callback.message.answer("❌ خطا در دریافت اطلاعات ترافیک")
        print("🔥 Exception in show_traffic:")
        print("Type:", type(e))
        print("Details:", str(e))

