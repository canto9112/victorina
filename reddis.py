import redis
from environs import Env


def connect_redis():
    env = Env()
    env.read_env()

    host = env('REDIS_HOST')
    port = env('REDIS_PORT')
    password = env('REDIS_PASSWORD')

    db = redis.StrictRedis(
        host=host,
        port=port,
        password=password,
        decode_responses=True
    )
    return db


def record_user_question(db, user_id, question):
    db.set(user_id, question)


def get_user_question(db, user_id):
    question = db.get(user_id)
    return question


db = connect_redis()
user_id = '1224342333'
quesiton = 'qeustion-2'

record_user_question(db, user_id, quesiton)
user_question = get_user_question(db, user_id)
print(user_question)



