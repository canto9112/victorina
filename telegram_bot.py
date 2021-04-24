import logging

from environs import Env
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (CommandHandler, ConversationHandler, Filters, MessageHandler, RegexHandler, Updater)

import questions
import reddis

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

QUESTION, ANSWER, SURRENDER = range(3)


def start(bot, update):
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счет']]

    update.message.reply_text('Привет! Это бот для викторины!',
        reply_markup=ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False))

    return QUESTION


def handle_new_question_request(bot, update):
    user_id = update['message']['chat']['id']
    db = reddis.connect_redis()
    question, answer = questions.get_random_question()
    db.set(user_id, answer)
    update.message.reply_text(question)
    print('clean_answer', answer)

    return ANSWER


def answer(bot, update):
    user_message = update['message']['text']
    user_id = update['message']['chat']['id']
    db = reddis.connect_redis()
    answer = db.get(user_id)

    clean_answer, answer_explanation = questions.get_clean_answer(answer)

    if user_message == clean_answer:
        update.message.reply_text('Правильно! Поздравляю!')
        return QUESTION

    elif user_message == 'Сдаться':
        return SURRENDER

    else:
        update.message.reply_text(f'Неправильно…\n'
                                  f'Попробуешь ещё раз?')
        return ANSWER


def surrender(bot, update):
    user_id = update['message']['chat']['id']

    db = reddis.connect_redis()
    answer = db.get(user_id)
    clean_answer, answer_explanation = questions.get_clean_answer(answer)
    update.message.reply_text(f'Ответ: {clean_answer}')

    return QUESTION


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    env = Env()
    env.read_env()

    telegam_token = env('TELEGRAM_TOKEN')
    updater = Updater(telegam_token)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            QUESTION: [RegexHandler('Новый вопрос', handle_new_question_request)],
            ANSWER: [MessageHandler(Filters.text, answer)],
            SURRENDER: [MessageHandler(Filters.text, surrender)],


        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()