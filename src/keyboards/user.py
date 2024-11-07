from aiogram.utils.keyboard import InlineKeyboardBuilder

async def get_track(tracks):
    builder = InlineKeyboardBuilder()

    for index, track in enumerate(tracks, start=1):
        builder.button(text=f"{index}", callback_data=f"id_{index}")

    builder.button(text="⬅️", callback_data="prev")
    builder.button(text="❌", callback_data="close")
    builder.button(text="➡️", callback_data="next")

    builder.adjust(5, 5, 3)

    return builder.as_markup()
