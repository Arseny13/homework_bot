
import logging
import os
import time
from logging.handlers import RotatingFileHandler
from urllib.error import HTTPError

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    handlers=[logging.FileHandler(
        filename="main.log",
        encoding='utf-8', mode='w')],
    format='%(asctime)s, %(levelname)s, %(message)s',
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(
    'Bot.log',
    maxBytes=50000000,
    backupCount=5,
    encoding='utf-8',
)
formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens() -> None:
    """Проверка на существование обязательных переменых."""
    if PRACTICUM_TOKEN is None:
        logger.critical('Нет PRACTICUM_TOKEN.')
        raise SystemExit()
    if TELEGRAM_TOKEN is None:
        logger.critical('Нет TELEGRAM_TOKEN.')
        raise SystemExit()
    if TELEGRAM_CHAT_ID is None:
        logger.critical('Нет TELEGRAM_CHAT_ID.')
        raise SystemExit()


def send_message(bot: telegram.bot.Bot, message: str) -> None:
    """Функция отправки сообщения боту ."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as error:
        logger.error(f'Ошибка при отправке: {error}.')
    else:
        logger.debug('Сообщение отправлено.')


def get_api_answer(timestamp: int) -> dict:
    """Функция запроса к API."""
    try:
        homeworks = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )
    except Exception as error:
        logger.error(f'Ошибка при запросе к основному API: {error}.')
    if homeworks.status_code != 200:
        logger.error(f'Ошибка статус ответа={homeworks.status_code}.')
        raise HTTPError(f'статус ответа={homeworks.status_code}')
    return homeworks.json()


def check_response(response: dict) -> dict:
    """Функция проверки ответа API."""
    if type(response) != dict:
        logger.error('У response не тот тип.')
        raise TypeError
    try:
        homeworks = response['homeworks']
    except KeyError:
        logger.error('У response нет ключа homeworks.')
    if type(homeworks) != list:
        logger.error('У homeworks не тот тип.')
        raise TypeError
    return response.get('homeworks')


def parse_status(homework: dict) -> str:
    """Функция получения статуса домашней работы."""
    try:
        status = homework['status']
    except KeyError:
        logger.error('У homework нет ключа status.')
    if status not in HOMEWORK_VERDICTS.keys():
        logger.error('status нет в словаре.')
        raise ValueError
    try:
        homework_name = homework['homework_name']
    except KeyError:
        logger.error('У homework нет ключа homework_name.')
    verdict = HOMEWORK_VERDICTS[status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main() -> None:
    """Основная логика работы бота."""
    check_tokens()
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
    except Exception as error:
        logger.error(f'Ошибка в запуске бота {error}')
    timestamp = int(time.time())
    send_message(bot, 'Бот включен!')
    err = ''
    while True:
        try:
            response = get_api_answer(timestamp)
            timestamp = response.get('current_date')
            homeworks = check_response(response)
            if len(homeworks) > 0:
                homework = homeworks[0]
                message = parse_status(homework)
                send_message(bot, message)
            else:
                logger.debug('Нет обновлений.')
            err = ''
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            if str(error) != str(err):
                send_message(bot, message)
                err = error
            logger.error(f'{message}')
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
