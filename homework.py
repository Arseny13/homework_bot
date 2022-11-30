
import json
import logging
import os
import time
from http import HTTPStatus
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
    exit = False
    if PRACTICUM_TOKEN is None:
        logger.critical('Нет PRACTICUM_TOKEN.')
        exit = True
    if TELEGRAM_TOKEN is None:
        logger.critical('Нет TELEGRAM_TOKEN.')
        exit = True
    if TELEGRAM_CHAT_ID is None:
        logger.critical('Нет TELEGRAM_CHAT_ID.')
        exit = True
    if exit:
        raise SystemExit()


def send_message(bot: telegram.bot.Bot, message: str) -> None:
    """Функция отправки сообщения боту ."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug('Сообщение отправлено.')
    except Exception as error:
        logger.error(f'Ошибка при отправке: {error}.')


def get_api_answer(timestamp: int) -> dict:
    """Функция запроса к API."""
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )
    except requests.exceptions.HTTPError as errh:
        logger.error(f' Ошибка HTTP : {errh}.')
    except requests.exceptions.ConnectionError as errc:
        logger.error(f' Ошибка соединения : {errc}.')
    except requests.exceptions.Timeout as errt:
        logger.error(f' Превышено время : {errt}.')
    except requests.exceptions.RequestException as error:
        logger.error(f'Неизвестная Ошибка: {error}.')
    if response.status_code != HTTPStatus.OK:
        logger.error(f'Ошибка статус ответа={response.status_code}.')
        raise HTTPError(f'статус ответа={response.status_code}')
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        logger.error('Ответ не преобразовался в json.')


def check_response(response: dict) -> dict:
    """Функция проверки ответа API."""
    if not isinstance(response, dict):
        logger.error('У response не тот тип.')
        raise TypeError
    homeworks = response.get('homeworks')
    if homeworks is None:
        logger.error('У response нет ключа homeworks.')
        raise KeyError
    if not isinstance(homeworks, list):
        logger.error('У homeworks не тот тип.')
        raise TypeError
    return homeworks


def parse_status(homework: dict) -> str:
    """Функция получения статуса домашней работы."""
    status = homework.get('status')
    if status is None:
        logger.error('У homework нет ключа status.')
        raise KeyError
    if status not in HOMEWORK_VERDICTS.keys():
        logger.error('status нет в словаре.')
        raise ValueError
    homework_name = homework.get('homework_name')
    if homework_name is None:
        logger.error('У homework нет ключа homework_name.')
        raise KeyError
    verdict = HOMEWORK_VERDICTS[status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main() -> None:
    """Основная логика работы бота."""
    check_tokens()
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
    except telegram.error.TelegramError as error:
        logger.error(f'Ошибка в запуске бота {error}')
        raise SystemExit()
    timestamp = int(time.time() - RETRY_PERIOD)
    send_message(bot, 'Бот включен!')
    last_error = ''
    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            if len(homeworks) > 0:
                homework = homeworks[0]
                message = parse_status(homework)
                send_message(bot, message)
            else:
                logger.debug('Нет обновлений.')
            last_error = ''
            timestamp = response.get('current_date', timestamp)
        except Exception as error:
            error = str(error)
            message = f'Сбой в работе программы: {error}'
            if error != last_error:
                send_message(bot, message)
                last_error = error
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
