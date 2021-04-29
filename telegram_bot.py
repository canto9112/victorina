import logging
from functools import partial

from environs import Env
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (CommandHandler, ConversationHandler, Filters, MessageHandler, RegexHandler, Updater)

import questions
import redis

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

QUESTION, ANSWER = range(2)


def start(bot, update):
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счет']]

    update.message.reply_text('Привет! Это бот для викторины!',
        reply_markup=ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False))

    return QUESTION


def handle_new_question_request(bot, update, db):
    question, answer = questions.get_random_question()
    user_id = update['message']['chat']['id']

    db.set(f'tg-{user_id}', answer)
    update.message.reply_text(question)
    return ANSWER


def handle_solution_attempt(bot, update, db):
    user_id = update['message']['chat']['id']
    user_message = update['message']['text']
    answer = db.get(f'tg-{user_id}')
    if user_message == answer:
        update.message.reply_text('Правильно! Поздравляю!\n'
                                  'Чтобы продолжить нажми Новый вопрос')
        return QUESTION

    update.message.reply_text('Не правильно! Попробуйте еще раз!')
    return ANSWER


def handle_surrender(bot, update, db):
    user_id = update['message']['chat']['id']

    answer = db.get(f'tg-{user_id}')
    update.message.reply_text(f'Ответ: {answer}\n'
                              f'Чтобы продолжить нажми Новый вопрос')

    return QUESTION


def handle_cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Всего доброго!',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def handle_error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    env = Env()
    env.read_env()
    telegam_token = env('TELEGRAM_TOKEN')
    db = redis.connect_redis()

    updater = Updater(telegam_token)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            QUESTION: [RegexHandler('Новый вопрос',
                                    partial(handle_new_question_request, db=db))],
            ANSWER: [RegexHandler('Сдаться', partial(handle_surrender, db=db)),
                     MessageHandler(Filters.text, partial(handle_solution_attempt, db=db))
                     ],
        },

        fallbacks=[CommandHandler('cancel', handle_cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(handle_error)
    updater.start_polling()


if __name__ == '__main__':
    main()
