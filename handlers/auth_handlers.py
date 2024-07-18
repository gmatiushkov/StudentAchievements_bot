from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import add_user, get_user
from keyboards import get_auth_menu, get_back_menu, get_back_to_auth_menu, get_main_menu_admin, get_main_menu_student
from functools import partial
from config import ADMINS_FULLNAMES

class AuthState(StatesGroup):
    not_authorized = State()
    authorized = State()

class Register(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_group_number = State()
    waiting_for_password = State()

class Login(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_password = State()

def register_auth_handlers(dp: Dispatcher, bot: Bot):
    dp.register_message_handler(send_welcome, commands=['start'], state='*')
    dp.register_callback_query_handler(lambda c: process_register(c, bot), lambda c: c.data == 'register', state='*')
    dp.register_callback_query_handler(lambda c: process_login(c, bot), lambda c: c.data == 'login', state='*')
    dp.register_callback_query_handler(partial(process_back_to_auth_menu, bot=bot), lambda c: c.data == 'back_to_auth_menu', state='*')
    dp.register_message_handler(lambda msg, state: process_register_full_name(msg, state, bot), state=Register.waiting_for_full_name)
    dp.register_message_handler(lambda msg, state: process_register_group_number(msg, state, bot), state=Register.waiting_for_group_number)
    dp.register_message_handler(lambda msg, state: process_register_password(msg, state, bot), state=Register.waiting_for_password)
    dp.register_message_handler(lambda msg, state: process_login_full_name(msg, state, bot), state=Login.waiting_for_full_name)
    dp.register_message_handler(lambda msg, state: process_login_password(msg, state, bot), state=Login.waiting_for_password)

async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply("Добро пожаловать! Пожалуйста, войдите или зарегистрируйтесь.", reply_markup=get_auth_menu())
    await state.set_state(AuthState.not_authorized)

async def process_register(callback_query: types.CallbackQuery, bot: Bot):
    await bot.send_message(callback_query.from_user.id, "Введите ваше ФИО:", reply_markup=get_back_to_auth_menu())
    await bot.answer_callback_query(callback_query.id)
    await Register.waiting_for_full_name.set()

async def process_register_full_name(message: types.Message, state: FSMContext, bot: Bot):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await message.reply("Введите номер группы:", reply_markup=get_back_to_auth_menu())
    await Register.waiting_for_group_number.set()

async def process_register_group_number(message: types.Message, state: FSMContext, bot: Bot):
    group_number = message.text
    await state.update_data(group_number=group_number)
    await message.reply("Введите пароль:", reply_markup=get_back_to_auth_menu())
    await Register.waiting_for_password.set()

async def process_register_password(message: types.Message, state: FSMContext, bot: Bot):
    password = message.text
    user_data = await state.get_data()
    add_user(user_data['full_name'], user_data['group_number'], password)
    user = get_user(user_data['full_name'], password)
    await state.update_data(full_name=user.full_name, group_number=user.group_number)
    await message.reply("Регистрация прошла успешно!", reply_markup=get_auth_menu())
    await state.set_state(AuthState.not_authorized)

async def process_login(callback_query: types.CallbackQuery, bot: Bot):
    await bot.send_message(callback_query.from_user.id, "Введите ваше ФИО:", reply_markup=get_back_to_auth_menu())
    await bot.answer_callback_query(callback_query.id)
    await Login.waiting_for_full_name.set()

async def process_login_full_name(message: types.Message, state: FSMContext, bot: Bot):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await message.reply("Введите пароль:", reply_markup=get_back_to_auth_menu())
    await Login.waiting_for_password.set()

async def process_login_password(message: types.Message, state: FSMContext, bot: Bot):
    password = message.text
    user_data = await state.get_data()
    user = get_user(user_data['full_name'], password)
    if user:
        is_admin = user.full_name in ADMINS_FULLNAMES
        await state.update_data(full_name=user.full_name, group_number=user.group_number, is_admin=is_admin)
        if is_admin:
            await message.reply("Вход администратора выполнен успешно!", reply_markup=get_main_menu_admin())
        else:
            await message.reply("Вход выполнен успешно!", reply_markup=get_main_menu_student())
        await state.set_state(AuthState.authorized)
    else:
        await message.reply("Неверное ФИО или пароль. Попробуйте еще раз.", reply_markup=get_auth_menu())
        await state.set_state(AuthState.not_authorized)

async def process_back_to_auth_menu(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state in [Register.waiting_for_full_name.state, Register.waiting_for_group_number.state, Register.waiting_for_password.state, Login.waiting_for_full_name.state, Login.waiting_for_password.state]:
        await state.set_state(AuthState.not_authorized)
        await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=get_auth_menu())
    else:
        await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=get_main_menu())
    await callback_query.answer()
