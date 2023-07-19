# homework_bot
<h1 align="center"> python telegram bot</h1>

___
<h2>Задача бота</h2>

- раз в 10 минут опрашивать API сервиса Практикум.Домашка и проверять статус отправленной на ревью домашней работы;
- при обновлении статуса анализировать ответ API и отправлять вам соответствующее уведомление в Telegram;
- логировать свою работу и сообщать вам о важных проблемах сообщением в Telegram.

___
<h2>Инструкция</h2>

1. Cкопировать проект 
```
    git.clone git@github.com:Arseny13/homework_bot.git
```
2. Переименовать .env.exapmle в .env
3. Заполнить файл .env
4. Установить виртуальное окр и запустить его 
```
python -m venv venv
source venv/Scripts/activate
python -m pip intall --upgrade pip
```
5. Написать в консоль(установка библеотек)
```
pip install -r requirements.txt
```
6. Запустить программу
```
python homework.py
```
___
<h2>Задание</h2>

- Функция main(): в ней описана основная логика работы программы. Все остальные функции должны запускаться из неё. Последовательность действий в общем виде должна быть примерно такой:
    1. Сделать запрос к API.
    2. Проверить ответ.
    3. Если есть обновления — получить статус работы из обновления и отправить сообщение в Telegram.
    4. Подождать некоторое время и вернуться в пункт 1.
- Функция check_tokens() проверяет доступность переменных окружения, которые необходимы для работы программы. Если отсутствует хотя бы одна переменная окружения — продолжать работу бота нет смысла.
- Функция get_api_answer() делает запрос к единственному эндпоинту API-сервиса. В качестве параметра в функцию передается временная метка. В случае успешного запроса должна вернуть ответ API, приведя его из формата JSON к типам данных Python.
- Функция check_response() проверяет ответ API на соответствие документации. В качестве параметра функция получает ответ API, приведенный к типам данных Python.
- Функция parse_status() извлекает из информации о конкретной домашней работе статус этой работы. В качестве параметра функция получает только один элемент из списка домашних работ. В случае успеха, функция возвращает подготовленную для отправки в Telegram строку, содержащую один из вердиктов словаря HOMEWORK_VERDICTS.
- Функция send_message() отправляет сообщение в Telegram чат, определяемый переменной окружения TELEGRAM_CHAT_ID. Принимает на вход два параметра: экземпляр класса Bot и строку с текстом сообщения.

___
<h2>Логирование</h2>
Каждое сообщение в журнале логов должно состоять как минимум из

- даты и времени события,
- уровня важности события,
- описания события.
Например:
```
2021-10-09 15:34:45,150 [ERROR] Сбой в работе программы: Эндпоинт https://practicum.yandex.ru/api/user_api/homework_statuses/111 недоступен. Код ответа API: 404
2021-10-09 15:34:45,355 [DEBUG] Бот отправил сообщение "Сбой в работе программы: Эндпоинт [https://practicum.yandex.ru/api/user_api/homework_statuses/](https://practicum.yandex.ru/api/user_api/homework_statuses/) недоступен. Код ответа API: 404"
```
Обязательно должны логироваться такие события:
- отсутствие обязательных переменных окружения во время запуска бота (уровень CRITICAL).
- удачная отправка любого сообщения в Telegram (уровень DEBUG);
- сбой при отправке сообщения в Telegram (уровень ERROR);
- недоступность эндпоинта https://practicum.yandex.ru/api/user_api/homework_statuses/ (уровень ERROR);
- любые другие сбои при запросе к эндпоинту (уровень ERROR);
- отсутствие ожидаемых ключей в ответе API (уровень ERROR);
- неожиданный статус домашней работы, обнаруженный в ответе API (уровень ERROR);
- отсутствие в ответе новых статусов (уровень DEBUG).

<h2>Используемые технологии</h2>

- python-dotenv==0.19.0
- python-telegram-bot==13.7
- requests==2.26.0
