import random
import os


def open_file(file_path):
    with open(file_path, 'r', encoding='KOI8-R') as file:
        content = file.read()
    return content


def get_questions(filename):
    file = open_file(f'quiz-questions/{filename}')

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
    directory = os.listdir('quiz-questions')
    for file in directory:
        questions = get_questions(file)
        random_question, random_answer = random.choice(list(questions.items()))
        question = ",".join(random_question.split('\n')[1:])
        answer = ",".join(random_answer.split('\n')[1:])
        clean_answer = answer.split('.')[0]

        return question, clean_answer

