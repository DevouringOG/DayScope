from aiogram.fsm.state import State, StatesGroup


class CreateTaskSG(StatesGroup):
    enter_title = State()
    enter_value = State()


class TasksSG(StatesGroup):
    view = State()


class CurrentTaskSG(StatesGroup):
    view = State()
    change_title = State()
    confirm_delete = State()
