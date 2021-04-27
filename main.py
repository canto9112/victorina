import telegram_bot
from environs import Env
import reddis








def main():
    env = Env()
    env.read_env()

    telegam_token = env('TELEGRAM_TOKEN')
    db = reddis.connect_redis()

    telegram_bot.start_bot(telegam_token, db)


if __name__ == '__main__':

    main()