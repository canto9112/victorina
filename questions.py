from environs import Env
from pprint import pprint
import random
import re


def open_file(file_path):
    with open(file_path, 'r', encoding='KOI8-R') as file:
        content = file.read()
    return content


def get_questions():
    file = open_file('quiz-questions/13voin.txt')
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
    return question, answer


def get_explanation(answer):
    explanation_regex = re.compile("\[(.*)\]")
    answer_explanation = explanation_regex.findall(answer)

    if answer_explanation:
        return answer_explanation[0]


def get_clean_answer(answer):
    clean_answer = answer.split('.')[0]
    answer_explanation = get_explanation(clean_answer)
    if answer_explanation:
        clean_answer = clean_answer.split(']')[1].strip()
        return clean_answer, answer_explanation
    else:
        return clean_answer, None
