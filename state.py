from aiogram.fsm.state import State, StatesGroup

class LoginState(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()
