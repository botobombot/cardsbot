from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from database import *
from fight import fight

# Состояния
SELECTING_CHARACTER, FREE_MODE = range(2)

# Функция для начала боя
async def start_fight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    character1_id = context.user_data.get('character1_id')
    character2_id = context.user_data.get('character2_id')

    if character1_id is None or character2_id is None:
        await update.message.reply_text("Пожалуйста, выберите обоих персонажей для боя.")
        return SELECTING_CHARACTER

    character1 = get_character(character1_id)
    character2 = get_character(character2_id)

    if character1 is None or character2 is None:
        await update.message.reply_text("Один или оба персонажа не найдены в базе данных.")
        return SELECTING_CHARACTER

    result = fight(character1, character2)
    await update.message.reply_text(result)
    return FREE_MODE

# Функция для обработки неизвестных сообщений
async def handle_unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Z ваще тупой и ниче не понимаю. Короч вот что я умею, общайся по шаблонам.\n/list_characters - показать айдишники персонажей. \
    Пока только ими могу распоряжаться. \n/select_character - выбор персонажей.\n/user - зарегаться\n/bio - добавить био\n/me - проверить акк")

# Функция для добавления пользователя в базу данных
async def add_user_to_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    add_user(user_id)
    await update.message.reply_text("Done")


#bio
async def add_bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    bio = update.message.text
    add_bio(user_id, bio)

# Функция для вывода списка userov
async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    usr = get_user(user_id)
    message = "Профиль:\n"
    message += f"ID: {usr.user_id}, Карты: {usr.own}, Клан: {usr.clan}, Био: {usr.bio}\n"
    await update.message.reply_text(message)

# Функция для рассылки сообщений всем пользователям
async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    secret_command = "РазошлиСообщениеВсемПароль123йцукен"
    if update.message.text == secret_command:
        users = get_all_users()
        message = "Нововведение: Теперь вы можете выбирать персонажей для боя!"
        for user_id in users:
            await context.bot.send_message(chat_id=user_id, text=message)
        await update.message.reply_text("Сообщение успешно разослано всем пользователям.")
    else:
        await update.message.reply_text("Неверная команда.")

# Функция для выбора персонажа
async def select_character(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    characters = get_all_characters()
    keyboard = [[f"{char[0]}: {char[1]}" for char in characters]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text("Выберите персонажа:", reply_markup=reply_markup)

# Функция для обработки выбора персонажа
async def handle_character_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        character_id = int(update.message.text.split(':')[0])
        character = get_character(character_id)

        if character:
            if 'character1_id' not in context.user_data:
                context.user_data['character1_id'] = character_id
                await update.message.reply_text(f"Вы выбрали первого персонажа: {character.name}. Теперь выберите второго персонажа.")
            elif 'character2_id' not in context.user_data:
                context.user_data['character2_id'] = character_id
                await update.message.reply_text(f"Вы выбрали второго персонажа: {character.name}. Начните бой с помощью команды /start_fight.")
            else:
                await update.message.reply_text(f"Братан, ты уже выбрал двух чаров, это {get_character(context.user_data.get('character1_id')).name} и {get_character(context.user_data.get('character2_id')).name}. Начни сражение командой /start_fight.")
        else:
            await update.message.reply_text("Персонаж с таким ID не найден. Пожалуйста, введите корректный ID персонажа.")
    except ValueError:
        await update.message.reply_text("Неверный формат ID. Пожалуйста, введите корректный ID персонажа.")

    return SELECTING_CHARACTER

# Функция для перехода в режим выбора персонажа
async def enter_select_character_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()  # Сброс выбора персонажей
    await update.message.reply_text("Вы перешли в режим выбора персонажа. Введите ID персонажа.")
    return SELECTING_CHARACTER
    
# Функция для возврата в свободный режим
async def return_to_free_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()  # Сброс выбора персонажей
    await update.message.reply_text("Вы вернулись в свободный режим.")
    return FREE_MODE

# Функция для вывода списка персонажей с их ID и именами
async def list_characters(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    characters = get_characters_with_ids()
    message = "Список персонажей:\n"
    for char in characters:
        message += f"ID: {char[0]}, Имя: {char[1]}\n"
    await update.message.reply_text(message)

def main():
    application = ApplicationBuilder().token("7898629957:AAFdOaUjnmmCJNvlz6BQ5Bdez9qo2A4qsYw").build()


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("list_characters", list_characters),
                        CommandHandler("select_character", enter_select_character_mode),
                        CommandHandler("user", add_user_to_db),
                        CommandHandler("bio", add_bio),
                        CommandHandler("me", whoami),
                        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown_message)],
        states={
            SELECTING_CHARACTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_character_selection),
                                  CommandHandler("start_fight", start_fight)],
            FREE_MODE: [CommandHandler("list_characters", list_characters),
                        CommandHandler("select_character", enter_select_character_mode),
                        MessageHandler(filters.TEXT & ~filters.COMMAND, add_user_to_db),
                        MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_message),
                        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown_message)]
        },
        fallbacks=[CommandHandler("cancel", return_to_free_mode)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", return_to_free_mode))

    print("Бот запущен")

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
