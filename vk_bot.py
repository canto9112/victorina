import random
from environs import Env

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
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


if __name__ == "__main__":
    env = Env()
    env.read_env()

    vk_token = env('VK_GROUP_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    keyboard = get_keyboard()

    db = reddis.connect_redis()
    question, answer = questions.get_random_question()
    clean_answer, answer_explanation = questions.get_clean_answer(answer)

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            user_id = event.user_id

            db.set(user_id, clean_answer)

            if event.text == "Новый вопрос":
                user_message = event.text
                send_message(question, vk_api, user_id, keyboard)
            db_answer = db.get(user_id)
            print(db_answer)
            if event.text == db_answer:
                print(event.text)
                send_message('Правильно!', vk_api, user_id, keyboard)
            if event.text == 'Сдаться':
                send_message(f'Правильный ответ: {clean_answer}\n'
                             f'Чтобы продолжить нажми Новый вопрос', vk_api, user_id, keyboard)

                # if event.text == clean_answer:
                #     send_message('Правильно!', vk_api, user_id, keyboard)

