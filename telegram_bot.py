from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import questions
import reddis


def start(bot, update):
    user_name = update['message']['chat']['username']
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(text=f'Привет {user_name}! Это бот для викторины!',
                              reply_markup=reply_markup)


def send_message(bot, update):
    user_message = update['message']['text']
    user_id = update['message']['chat']['id']

    question = questions.get_random_question()

    db = reddis.connect_redis()

    if user_message == 'Новый вопрос':
        reddis.record_user_question(db, user_id, question)
        update.message.reply_text(question)
        print(reddis.get_user_question(db, user_id))


def start_bot(token):
    updater = Updater(token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, send_message))
    updater.start_polling()
    updater.idle()


def main():
    env = Env()
    env.read_env()

    telegam_token = env('TELEGRAM_TOKEN')
    start_bot(telegam_token)


if __name__ == '__main__':
    main()