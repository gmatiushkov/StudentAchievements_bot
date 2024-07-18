from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Добавить достижение", callback_data='add_achievement'),
        InlineKeyboardButton("Удалить достижение", callback_data='delete_achievement'),
        InlineKeyboardButton("Просмотр всех достижений", callback_data='view_achievements'),
        InlineKeyboardButton("Подтверждение достижений", callback_data='approve_achievements')
    )

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
