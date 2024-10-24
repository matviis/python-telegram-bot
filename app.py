import os
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PORT = int(os.environ.get('PORT', '8443'))  # Порт для вебхука

# Функция для стартового экрана с кнопками
def start(update, context):
    keyboard = [["Каталог"], ["Вопрос-ответ"], ["Консультация"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Привет! Чем могу помочь?", reply_markup=reply_markup)

# Обработка кнопки Каталог
def catalog(update, context):
    update.message.reply_text("Вы открыли каталог товаров.")

# Обработка кнопки Вопрос-ответ
def faq(update, context):
    update.message.reply_text("Часто задаваемые вопросы:\n1. Как сделать заказ?\n2. Какова стоимость доставки?\n...")

# Обработка кнопки Консультация
def consultation(update, context):
    update.message.reply_text("Для консультации напишите нашему менеджеру @manager_username.")

# Функция обработки сообщений
def handle_message(update, context):
    text = update.message.text
    if text == "Каталог":
        catalog(update, context)
    elif text == "Вопрос-ответ":
        faq(update, context)
    elif text == "Консультация":
        consultation(update, context)
    else:
        update.message.reply_text("Пожалуйста, выберите один из вариантов.")

# Основная функция
def main():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")  # Получаем токен из переменных окружения
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Настройка вебхуков
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook(f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}")

    updater.idle()

if __name__ == '__main__':
    main()
