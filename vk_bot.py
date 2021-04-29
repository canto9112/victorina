import random

import vk_api as vk
from environs import Env
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll

import questions
import reddis


def send_message(event, vk_api, user_id, keyboard):
    vk_api.messages.send(
        user_id=user_id,
        message=event,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard()
    )


def get_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.SECONDARY)

    return keyboard


def main():
    env = Env()
    env.read_env()
    vk_token = env('VK_GROUP_TOKEN')
    db = reddis.connect_redis()
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    keyboard = get_keyboard()

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_message = event.text

            user_id = event.user_id

            if user_message == "Новый вопрос":
                question, answer = questions.get_random_question()
                db.set(f'vk-{user_id}', answer)
                send_message(question, vk_api, user_id, keyboard)

            elif user_message == db.get(f'vk-{user_id}'):
                send_message('Правильно! Поздравляю!\n'
                             'Чтобы продолжить нажми Новый вопрос', vk_api, user_id, keyboard)

            elif user_message == 'Сдаться':
                db_answer = db.get(f'vk-{user_id}')
                send_message(f'Правильный ответ: {db_answer}\n'
                             f'Чтобы продолжить нажми Новый вопрос', vk_api, user_id, keyboard)

            elif user_message != db.get(f'vk-{user_id}'):
                send_message('Не правильно!\n'
                             'Попробуйте еще раз!', vk_api, user_id, keyboard)


if __name__ == '__main__':
    main()
