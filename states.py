from aiogram.fsm.state import State, StatesGroup

class AcceptState(StatesGroup):
    full_name = State()
    birth_date = State()
    image = State()
    study_place = State()
    address = State()
    email = State()
    phone_number = State()
    file = State()
