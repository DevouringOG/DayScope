from aiogram.fsm.state import StatesGroup, State


class StartSG(StatesGroup):
    start = State()


class MenuSG(StatesGroup):
    view = State()
    help = State()


class CreateTaskSG(StatesGroup):
    enter_title = State()
    enter_value = State()


class TasksSG(StatesGroup):
    view = State()


class CurrentTaskSG(StatesGroup):
    view = State()
    change_title = State()
    confirm_remove = State()


class TodaySG(StatesGroup):
    view = State()


class CreateNote(StatesGroup):
    enter_text = State()
    confirm_text = State()
    edit_text = State()


class CurrentNoteSG(StatesGroup):
    view = State()
    change_text = State()
    confirm_remove = State()
