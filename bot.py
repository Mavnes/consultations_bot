import datetime

import telebot
import json
import re

TOKEN = "5636903277:AAFu9Ig3yH9IPDWjMvk3GLe8pB0mwSjeqWs"
bot = telebot.TeleBot(TOKEN)
consultations = []

class Consultation:
    class_cons = "class"
    room_cons = "room"
    date_cons = "date"
    time_cons = "time"
    people_cons = []

    def __init__(self, class_cons, room_cons, date_cons, time_cons, people_cons):
        self.class_cons = class_cons
        self.room_cons = room_cons
        self.date_cons = date_cons
        self.time_cons = time_cons
        self.people_cons = people_cons


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Привет, я чертила')


# /addme Иванов Иван Иванович -r ВТВ-268 -c Мат. анализ -d 01.01.2020 -t 15:00
@bot.message_handler(commands=['addme'])
def start_handler(message):
    message_text = str(message.text)
    result = re.match(r'^\/addme ([А-ЯЁ][а-яё]+[\-\s]?){3,} -r [А-ЯЁ]{1,3}-\d{1,4}[а-яё]? -c [ А-Яа-яЁё.]+-d \d{1,2}.\d{2}.\d{4} -t \d{1,2}:\d{2}$', message_text)
    ok = False

    if result is not None:
        params = re.split(r' -[rcdt]{1} ', result.group())
        for i, consultation in enumerate(consultations):
            if consultation.class_cons == params[2]:
                if consultation.room_cons == params[1]:
                    if consultation.date_cons == params[3]:
                        if consultation.time_cons == params[4]:
                            consultation.people_cons.append(params[0][7:])
                            save_data("data.json")
                            result = f"Создана запись:\n   Имя: {params[0][7:]}\n   Предмет:  {consultation.class_cons}\n   Аудитория: {consultation.room_cons}\n   Дата: {consultation.date_cons}\n   Время: {consultation.time_cons}"
                            ok = True
    if not ok:
        result = "Ошибка. Введены неверные данные."

    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['list'])
def start_handler(message):
    result = "Список консультаций: "
    for i, consultation in enumerate(consultations):
        result += f"\n{i + 1}. {consultation.class_cons}:\n    Дата: {consultation.date_cons}\n    Время: {consultation.time_cons}\n    Аудитория: {consultation.room_cons}"

    bot.send_message(message.chat.id, result)


def get_data(path):
    with open(path, "r", encoding='utf-8') as read_file:
        data = json.load(read_file)

    for i, consultation in enumerate(data):
        people = []
        for person in data[i]['people_cons']:
            people.append(person)
        consultations.append(Consultation(data[i]['class_cons'], data[i]['room_cons'], data[i]['date_cons'], data[i]['time_cons'], people))


def save_data(path):
    json_string = "["

    for i, consultation in enumerate(consultations):
        json_string += json.dumps(consultation.__dict__, ensure_ascii=False)
        if i == consultations.__len__() - 1:
            json_string += "\n"
        else:
            json_string += ",\n"

    json_string += "]"

    with open(path, "w", encoding='utf-8') as write_file:
        write_file.write(json_string)


get_data("data.json")
bot.polling()
