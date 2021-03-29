from environs import Env


def open_file(file_path):
    with open(file_path, 'r', encoding='KOI8-R') as file:
        content = file.read()
    return content


def main():
    pass


if __name__ == '__main__':
    env = Env()
    env.read_env()

    main()
    print(open_file('quiz-questions/1vs1200.txt'))