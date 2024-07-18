from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_student():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Добавить достижение", callback_data="add_achievement"),
        InlineKeyboardButton(text="Удалить достижение", callback_data="delete_achievement"),
        InlineKeyboardButton(text="Просмотр достижений", callback_data="view_achievements")
    )
    return keyboard

def get_main_menu_admin():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Просмотр достижений", callback_data="view_achievements"),
        InlineKeyboardButton(text="Удалить достижение", callback_data="delete_achievement"),
        InlineKeyboardButton(text="Подтверждение достижений", callback_data="approve_achievements")
    )
    return keyboard
def get_main_menu(user_data):
    is_admin = user_data.get('is_admin', False)
    if is_admin:
        return get_main_menu_admin()
    else:
        return get_main_menu_student()

def get_back_menu():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Назад", callback_data='back_to_main_menu')
    )

def get_back_to_auth_menu():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Назад", callback_data='back_to_auth_menu')
    )

def get_view_achievements_menu():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Просмотр достижения", callback_data='view_achievement_details'),
        InlineKeyboardButton("Назад", callback_data='back_to_main_menu')
    )

def get_back_to_achievements_menu():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Назад", callback_data='back_to_achievements')
    )

def get_approval_menu():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Подтвердить", callback_data='approve'),
        InlineKeyboardButton("Отклонить", callback_data='reject'),
        InlineKeyboardButton("Назад", callback_data='back_to_approvals')
    )

def get_auth_menu():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Войти", callback_data='login'),
        InlineKeyboardButton("Зарегистрироваться", callback_data='register')
    )
