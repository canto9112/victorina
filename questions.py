from environs import Env
from pprint import pprint
import random


def open_file(file_path):
    with open(file_path, 'r', encoding='KOI8-R') as file:
        content = file.read()
    return content


def get_questions():
    file = open_file('quiz-questions/12koll12.txt')
    content = file.split('\n\n')
    block_questions = []
    block_answers = []
    for block in content:
        if block.startswith('Вопрос'):
            block_questions.append(block)

        elif block.startswith('Ответ'):

            block_answers.append(block)
    questions = dict(zip(block_questions, block_answers))

    return questions


def get_random_question():
    questions = get_questions()
    random_question = random.choice(list(questions.keys()))
    return random_question



# if __name__ == '__main__':
#     env = Env()
#     env.read_env()
#
#     get_random_question()




