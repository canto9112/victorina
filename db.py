import db
from environs import Env


def connect_redis():
    env = Env()
    env.read_env()

    host = env('REDIS_HOST')
    port = env('REDIS_PORT')
    password = env('REDIS_PASSWORD')

    db = db.StrictRedis(
        host=host,
        port=port,
        password=password,
        decode_responses=True
    )
    return db
