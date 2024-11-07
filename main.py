from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from services import cup_image
import asyncio
import time
import os

from pyexpat.errors import messages

token = '7923931120:AAE4ThwpUZ9HUtqNddQ7tWhKrZDXZpc15uI'

bot = Bot(token=token)

dp = Dispatcher()

class UploadPhotoState(StatesGroup):
    name = State()
    photo = State()

@dp.message(CommandStart())
async def welcome(message: Message):
    return await message.answer('Бот для додавання фото')


@dp.message(Command('photo'))
async def handle_photo(message: Message, state: FSMContext):
    await message.answer("Введіть ім'я людини чиє фото хочете завантажити")
    await state.set_state(UploadPhotoState.name)

@dp.message(UploadPhotoState.name)
async def input_name(message: Message, state: FSMContext):
    name = message.text.replace(' ', '')
    print('name', name)
    user_folder_path = os.path.join('faces', name)
    print('path', user_folder_path)
    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)

    await state.update_data(name=name)
    await message.answer('Тепер надішліть фото')
    await state.set_state(UploadPhotoState.photo)


@dp.message(UploadPhotoState.photo)
async def upload_photo(message: Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get('name')
    user_folder_path = os.path.join('faces', name)
    photo = message.photo[-1]
    photo_path = os.path.join(user_folder_path, f'{photo.file_id}.jpg')
    await message.answer('Завантажую фото ...')
    # if not os.path.exists(photo_path) or os.path.getsize(photo_path) == 0:
    #     return await message.answer('Файл було завантажено не коректно')
    # await photo.download(destination_file=photo_path)
    await bot.download(photo, destination=photo_path)
    await asyncio.sleep(1)
    cropped_photo_path = os.path.join(user_folder_path, f"cropped_{photo.file_id}.jpg")
    print('photo_path', photo_path)
    print('cropped_photo_path', cropped_photo_path)
    result = cup_image(photo_path, cropped_photo_path)
    if result == 'Збережено':
        return await message.answer('Фото збережено!')
    else:
        return await message.answer(f'Помилка {result}')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
