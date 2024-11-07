import os
from dotenv import load_dotenv

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from vkpymusic import ServiceAsync, TokenReceiver

from src.keyboards.user import get_track

load_dotenv()

tokenReceiver = TokenReceiver(login=os.getenv("login"), password=os.getenv("password"))

if tokenReceiver.auth():
    tokenReceiver.get_token()
    tokenReceiver.save_to_config()

user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer("Привет! Я могу найти музыку по её названию или автору 😊 из VK")

@user.message(F.text)
async def search_music(message: Message, state: FSMContext) -> None:
    service = ServiceAsync.parse_config()
    tracks = await service.search_songs_by_text(message.text, count=10)

    if tracks:
        tracks_dict = [track.to_dict() for track in tracks]
        await state.update_data(tracks=tracks_dict)

        results = [f"По запросу <b>{message.text}</b> удалось найти:\n\n"]

        for idx, track in enumerate(tracks, start=1):
            title = track.title
            artist = track.artist
            results.append(f"{idx}. {artist} - {title}")

        results_text = "\n".join(results)

        await message.answer(results_text,
                             parse_mode=ParseMode.HTML,
                             reply_markup=await get_track(tracks))
    else:
        await message.answer("По вашему запросу ничего не найдено.")

@user.callback_query(F.data == "close")
async def delete_answer(callback: CallbackQuery) -> None:
    await callback.message.delete()

@user.callback_query(F.data.startswith("id_"))
async def send_track(callback: CallbackQuery, state: FSMContext) -> None:
    track_index = int(callback.data.split('_')[1]) - 1

    data = await state.get_data()
    tracks = data.get("tracks", [])

    if tracks and 0 <= track_index < len(tracks):
        track = tracks[track_index]

        await callback.bot.send_audio(
            chat_id=callback.from_user.id,
            audio=track['url'],
            title=track['title'],
            performer=track['artist'],
            duration=track['duration']
        )
        await callback.answer()
    else:
        await callback.answer("Трек не найден", show_alert=True)