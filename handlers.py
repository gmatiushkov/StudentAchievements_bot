from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import add_achievement, delete_achievement, get_achievements, get_pending_achievements, update_achievement_status
from keyboards import get_main_menu, get_back_menu, get_view_achievements_menu, get_back_to_achievements_menu, get_approval_menu
from models import Achievement

class AddAchievement(StatesGroup):
    waiting_for_description = State()
    waiting_for_files = State()

class DeleteAchievement(StatesGroup):
    waiting_for_number = State()

class ViewAchievement(StatesGroup):
    waiting_for_number = State()
    viewing_achievement = State()

class ApproveAchievement(StatesGroup):
    waiting_for_number = State()
    viewing_achievement = State()

def register_handlers(dp: Dispatcher, bot: Bot):
    dp.register_message_handler(send_welcome, commands=['start'], state='*')
    dp.register_callback_query_handler(lambda c: process_add_achievement(c, bot), lambda c: c.data == 'add_achievement', state='*')
    dp.register_callback_query_handler(lambda c: process_delete_achievement(c, bot), lambda c: c.data == 'delete_achievement', state='*')
    dp.register_callback_query_handler(lambda c: process_view_achievements(c, bot), lambda c: c.data == 'view_achievements', state='*')
    dp.register_callback_query_handler(lambda c: process_view_achievement_details(c, bot), lambda c: c.data == 'view_achievement_details', state='*')
    dp.register_callback_query_handler(lambda c: process_back_to_achievements(c, bot), lambda c: c.data == 'back_to_achievements', state='*')
    dp.register_callback_query_handler(lambda c: process_back(c, bot), lambda c: c.data == 'back', state='*')
    dp.register_callback_query_handler(lambda c: process_approve_achievements(c, bot), lambda c: c.data == 'approve_achievements', state='*')
    dp.register_callback_query_handler(lambda c, state: process_view_approval_details(c, state, bot), lambda c: c.data == 'approve', state='*')
    dp.register_callback_query_handler(lambda c, state: process_reject_approval(c, state, bot), lambda c: c.data == 'reject', state='*')
    dp.register_callback_query_handler(lambda c: process_back_to_approvals(c, bot), lambda c: c.data == 'back_to_approvals', state='*')
    dp.register_message_handler(lambda msg, state: process_achievement_description(msg, state, bot), state=AddAchievement.waiting_for_description)
    dp.register_message_handler(lambda msg, state: process_achievement_files(msg, state, bot), content_types=['document', 'photo'], state=AddAchievement.waiting_for_files)
    dp.register_message_handler(done_adding_files, commands=['done'], state=AddAchievement.waiting_for_files)
    dp.register_message_handler(lambda msg, state: process_achievement_number(msg, state, bot), state=DeleteAchievement.waiting_for_number)
    dp.register_message_handler(lambda msg, state: process_view_achievement_number(msg, state, bot), state=ViewAchievement.waiting_for_number)
    dp.register_message_handler(lambda msg, state: process_approval_number(msg, state, bot), state=ApproveAchievement.waiting_for_number)

def trim_description(description):
    if len(description) > 27:
        return description[:27] + "..."
    return description

async def send_welcome(message: types.Message):
    await message.reply("Добро пожаловать! Выберите действие:", reply_markup=get_main_menu())

async def process_add_achievement(callback_query: types.CallbackQuery, bot: Bot):
    await bot.send_message(callback_query.from_user.id, "Введите описание достижения (до 1000 символов):", reply_markup=get_back_menu())
    await bot.answer_callback_query(callback_query.id)
    await AddAchievement.waiting_for_description.set()

async def process_achievement_description(message: types.Message, state: FSMContext, bot: Bot):
    description = message.text
    if len(description) > 1000:
        await message.reply("Описание слишком длинное! Попробуйте еще раз.", reply_markup=get_back_menu())
    else:
        await state.update_data(description=description, files=[])
        await message.reply("Теперь отправьте файлы (до 10 файлов). Когда закончите, нажмите /done.", reply_markup=get_back_menu())
        await AddAchievement.waiting_for_files.set()

async def process_achievement_files(message: types.Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    files = user_data.get('files', [])
    if message.content_type == 'document':
        files.append(('document', message.document.file_id))
    elif message.content_type == 'photo':
        files.append(('photo', message.photo[-1].file_id))

    if len(files) > 10:
        await message.reply("Вы прислали слишком много файлов! Попробуйте еще раз.", reply_markup=get_back_menu())
    else:
        await state.update_data(files=files)

async def done_adding_files(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    description = user_data['description']
    files = user_data['files']
    add_achievement(description, files)
    await message.reply("Достижение добавлено!", reply_markup=get_main_menu())
    await state.finish()

async def process_delete_achievement(callback_query: types.CallbackQuery, bot: Bot):
    achievements = get_achievements()
    if not achievements:
        await bot.send_message(callback_query.from_user.id, "Нет достижений для удаления.", reply_markup=get_main_menu())
    else:
        response = "Список достижений:\n"
        for i, ach in enumerate(achievements, 1):
            response += f"{i}. {trim_description(ach.description)}\n"
        response += "\nВведите номер достижения, которое хотите удалить:"
        await bot.send_message(callback_query.from_user.id, response, reply_markup=get_back_menu())
        await bot.answer_callback_query(callback_query.id)
        await DeleteAchievement.waiting_for_number.set()

async def process_achievement_number(message: types.Message, state: FSMContext, bot: Bot):
    try:
        number = int(message.text)
        achievements = get_achievements()
        if number < 1 or number > len(achievements):
            response = "Список достижений:\n"
            for i, ach in enumerate(achievements, 1):
                response += f"{i}. {trim_description(ach.description)}\n"
            response += "\nНекорректный номер. Попробуйте еще раз."
            await message.reply(response, reply_markup=get_back_menu())
        else:
            achievement_id = achievements[number - 1].id
            delete_achievement(achievement_id)
            await message.reply("Достижение удалено!", reply_markup=get_main_menu())
            await state.finish()
    except ValueError:
        achievements = get_achievements()
        response = "Список достижений:\n"
        for i, ach in enumerate(achievements, 1):
            response += f"{i}. {trim_description(ach.description)}\n"
        response += "\nНекорректный ввод. Введите номер достижения."
        await message.reply(response, reply_markup=get_back_menu())

async def process_view_achievements(callback_query: types.CallbackQuery, bot: Bot):
    achievements = get_achievements()
    if not achievements:
        await bot.send_message(callback_query.from_user.id, "Достижений нет.", reply_markup=get_back_menu())
    else:
        response = "Список достижений:\n"
        for i, ach in enumerate(achievements, 1):
            response += f"{i}. {trim_description(ach.description)}\n"
        await bot.send_message(callback_query.from_user.id, response, reply_markup=get_view_achievements_menu())
    await bot.answer_callback_query(callback_query.id)

async def process_view_achievement_details(callback_query: types.CallbackQuery, bot: Bot):
    achievements = get_achievements()
    if not achievements:
        await bot.send_message(callback_query.from_user.id, "Достижений нет.", reply_markup=get_back_to_achievements_menu())
    else:
        response = "Список достижений:\n"
        for i, ach in enumerate(achievements, 1):
            response += f"{i}. {trim_description(ach.description)}\n"
        response += "\nВведите номер достижения, которое хотите просмотреть:"
        await bot.send_message(callback_query.from_user.id, response, reply_markup=get_back_to_achievements_menu())
    await ViewAchievement.waiting_for_number.set()
    await bot.answer_callback_query(callback_query.id)

async def process_view_achievement_number(message: types.Message, state: FSMContext, bot: Bot):
    try:
        number = int(message.text)
        achievements = get_achievements()
        if number < 1 or number > len(achievements):
            response = "Список достижений:\n"
            for i, ach in enumerate(achievements, 1):
                response += f"{i}. {trim_description(ach.description)}\n"
            response += "\nНекорректный номер. Попробуйте еще раз."
            await message.reply(response, reply_markup=get_back_to_achievements_menu())
        else:
            achievement = achievements[number - 1]
            if achievement.files:
                for file_type, file_id in achievement.files:
                    if file_type == 'photo':
                        await bot.send_photo(message.from_user.id, file_id)
                    else:
                        await bot.send_document(message.from_user.id, file_id)
            await message.reply(f"Достижение {number}:\n{achievement.description}")
            response = "Список достижений:\n"
            for i, ach in enumerate(achievements, 1):
                response += f"{i}. {trim_description(ach.description)}\n"
            await bot.send_message(message.from_user.id, response, reply_markup=get_view_achievements_menu())
            await ViewAchievement.viewing_achievement.set()
    except ValueError:
        achievements = get_achievements()
        response = "Список достижений:\n"
        for i, ach in enumerate(achievements, 1):
            response += f"{i}. {trim_description(ach.description)}\n"
        response += "\nНекорректный ввод. Введите номер достижения."
        await message.reply(response, reply_markup=get_back_to_achievements_menu())

async def process_approve_achievements(callback_query: types.CallbackQuery, bot: Bot):
    achievements = get_pending_achievements()
    if not achievements:
        await bot.send_message(callback_query.from_user.id, "Нет достижений для подтверждения.", reply_markup=get_main_menu())
    else:
        response = "Список достижений на рассмотрении:\n"
        for i, ach in enumerate(achievements, 1):
            response += f"{i}. {trim_description(ach.description)}\n"
        response += "\nВведите номер достижения, которое хотите просмотреть:"
        await bot.send_message(callback_query.from_user.id, response, reply_markup=get_back_menu())
        await ApproveAchievement.waiting_for_number.set()
    await bot.answer_callback_query(callback_query.id)

async def process_approval_number(message: types.Message, state: FSMContext, bot: Bot):
    try:
        number = int(message.text)
        achievements = get_pending_achievements()
        if number < 1 or number > len(achievements):
            response = "Список достижений на рассмотрении:\n"
            for i, ach in enumerate(achievements, 1):
                response += f"{i}. {trim_description(ach.description)}\n"
            response += "\nНекорректный номер. Попробуйте еще раз."
            await message.reply(response, reply_markup=get_back_menu())
        else:
            achievement = achievements[number - 1]
            await state.update_data(achievement_id=achievement.id)
            if achievement.files:
                for file_type, file_id in achievement.files:
                    if file_type == 'photo':
                        await bot.send_photo(message.from_user.id, file_id)
                    else:
                        await bot.send_document(message.from_user.id, file_id)
            await message.reply(f"Достижение {number}:\n{achievement.description}", reply_markup=get_approval_menu())
            await ApproveAchievement.viewing_achievement.set()
    except ValueError:
        achievements = get_pending_achievements()
        response = "Список достижений на рассмотрении:\n"
        for i, ach in enumerate(achievements, 1):
            response += f"{i}. {trim_description(ach.description)}\n"
        response += "\nНекорректный ввод. Введите номер достижения."
        await message.reply(response, reply_markup=get_back_menu())

async def process_view_approval_details(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    achievement_id = user_data['achievement_id']
    update_achievement_status(achievement_id, 'Подтверждено')
    await bot.send_message(callback_query.from_user.id, "Достижение подтверждено!")
    await process_approve_achievements(callback_query, bot)
    await state.finish()
    await callback_query.answer()

async def process_reject_approval(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    achievement_id = user_data['achievement_id']
    update_achievement_status(achievement_id, 'Отклонено')
    await bot.send_message(callback_query.from_user.id, "Достижение отклонено.")
    await process_approve_achievements(callback_query, bot)
    await state.finish()
    await callback_query.answer()

async def process_back_to_approvals(callback_query: types.CallbackQuery, bot: Bot):
    await process_approve_achievements(callback_query, bot)

async def process_back_to_achievements(callback_query: types.CallbackQuery, bot: Bot):
    achievements = get_achievements()
    if not achievements:
        await bot.send_message(callback_query.from_user.id, "Достижений нет.", reply_markup=get_main_menu())
    else:
        response = "Список достижений:\n"
        for i, ach in enumerate(achievements, 1):
            response += f"{i}. {trim_description(ach.description)}\n"
        await bot.send_message(callback_query.from_user.id, response, reply_markup=get_view_achievements_menu())
    await ViewAchievement.waiting_for_number.set()
    await callback_query.answer()

async def process_back(callback_query: types.CallbackQuery, bot: Bot):
    await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=get_main_menu())
    await callback_query.answer()
