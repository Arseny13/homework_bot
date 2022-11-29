# homework_bot
<h1 align="center"> python telegram bot</h1>

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

____

<h2>Инструкция</h2>
1. Cкопировать проект 
'''
    git.clone
'''
2. Переименовать .env.exapmle в .env
3. Заполнить файл .env
4. Установить виртуальное окр и запустить его 
'''
python -m venv venv
source venv/Scripts/activate
python -m pip intall --upgrade pip
'''
