from aiogram.types import Message, CallbackQuery
from aiogram import BaseMiddleware
from handlers.start_handler import sessions
from aiogram.fsm.context import FSMContext
from state import LoginState

class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        state: FSMContext = data.get("state")
        current_state = await state.get_state() if state else None

        if isinstance(event, Message):
            if (
                event.text == "/start"
                or current_state in [LoginState.waiting_for_username.state, LoginState.waiting_for_password.state]
            ):
                return await handler(event, data)
            user_id = event.from_user.id

        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            return

        if user_id not in sessions:
            if isinstance(event, Message):
                await event.answer("❗️لطفاً ابتدا با دستور /start وارد شوید.")
            elif isinstance(event, CallbackQuery):
                await event.message.answer("❗️لطفاً ابتدا با دستور /start وارد شوید.")
                await event.answer()
            return

        data["session"] = sessions[user_id]
        return await handler(event, data)
