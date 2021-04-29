import random
import re


def open_file(file_path):
    with open(file_path, 'r', encoding='KOI8-R') as file:
        content = file.read()
    return content


def get_questions():
    file = open_file('quiz-questions/9krug16.txt')
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
    random_question, random_answer = random.choice(list(questions.items()))

    question = ",".join(random_question.split('\n')[1:])
    answer = ",".join(random_answer.split('\n')[1:])
    clean_answer = answer.split('.')[0]
    print(question)
    print(clean_answer)
    return question, clean_answer
