import structlog
from aiogram_dialog import DialogManager

logger = structlog.get_logger(__name__)


async def note_view_getter(dialog_manager: DialogManager, *args, **kwargs):
    if not dialog_manager.dialog_data.get("note_text", False):
        dialog_manager.dialog_data["note_text"] = dialog_manager.start_data[
            "note_text"
        ]
    return {}
