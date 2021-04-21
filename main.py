from environs import Env
from pprint import pprint


def open_file(file_path):
    with open(file_path, 'r', encoding='KOI8-R') as file:
        content = file.read()
    return content


def get_questions(file):
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




if __name__ == '__main__':
    env = Env()
    env.read_env()

    file = open_file('quiz-questions/12koll12.txt')
    get_questions(file)




