import random
import requests
import json
# import sqlite3
import psycopg2
import urllib.parse
import telebot
from telebot import types
import os
from flask import Flask, request


TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
print("BOT_TOKEN:", TOKEN)

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL:", DATABASE_URL)


WEBHOOK_PATH = f"/{TOKEN}"
print("WEBHOOK_PATH:", WEBHOOK_PATH)
WEBHOOK_URL = f"https://risbot-production.up.railway.app{WEBHOOK_PATH}"
print("WEBHOOK_PATH:", WEBHOOK_PATH)

app = Flask(__name__)
print('app = Flask(__name__)')


@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    print('in @app.route')
    return '', 200


class ConvertionException(Exception):
    pass


class MyCustomException(Exception):
    pass


def get_admins():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT administrators.name FROM administrators')
    result = cursor.fetchall()
    conn.close()
    admins = [admin[0] for admin in result]
    return admins


def get_example_meme():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT photo FROM example_meme')
    result = cursor.fetchall()
    conn.close()
    actual_meme = result[0][0]
    return actual_meme


def get_announcements(argument):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT game_announcement.name, game_announcement.announcement FROM game_announcement WHERE status IS NULL')
    announcements = cursor.fetchall()
    conn.close()

    if argument is None:
        if len(announcements) == 0:
            return 'Новых анонсов от игроков нет 😌'
        else:
            result = []
            for text in announcements:
                master = text[0]
                text_announcement = text[1]
                new_text = f'Мастер: @{master}\n{text_announcement}'
                result.append(new_text)

            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE game_announcement SET status=%s WHERE status IS NULL',
                (True, ))
            conn.commit()
            conn.close()
            return result

    elif argument is True:
        if len(announcements) == 0:
            return 'Анонсов от игроков пока нет 😌'
        else:
            result = []
            for text in announcements:
                master = text[0]
                text_announcement = text[1]
                new_text = f'Мастер: @{master}\n{text_announcement}'
                result.append(new_text)
            return result


def get_stories(argument):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT history.author, history.text FROM history WHERE status IS NULL')
    stories = cursor.fetchall()
    conn.close()

    if argument is None:
        if len(stories) == 0:
            return 'Новых историй от игроков нет 😌'
        else:
            result = []
            for text in stories:
                author = text[0]
                text_story = text[1]
                if author != 'автор пожелал остаться анонимным 😌':
                    new_text = f'Автор: @{author}\n{text_story}'
                    result.append(new_text)
                else:
                    new_text = f'Автор: {author}\n{text_story}'
                    result.append(new_text)
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE history SET status=%s WHERE status IS NULL',
                (True, ))
            conn.commit()
            conn.close()
            return result

    elif argument is True:
        if len(stories) == 0:
            return 'Историй от игроков пока нет 😌'
        else:
            result = []
            for text in stories:
                author = text[0]
                text_story = text[1]
                if author != 'автор пожелал остаться анонимным 😌':
                    new_text = f'Автор: @{author}\n{text_story}'
                    result.append(new_text)
                else:
                    new_text = f'Автор: {author}\n{text_story}'
                    result.append(new_text)
            return result


def get_ideas(argument):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT ideas.author, ideas.idea FROM ideas WHERE status IS NULL')
    ideas = cursor.fetchall()
    conn.close()

    if argument is None:
        if len(ideas) == 0:
            return 'Новых идей от игроков нет 😌'
        else:
            result = []
            for elem in ideas:
                author = elem[0]
                text_idea = elem[1]
                if author != 'автор пожелал остаться анонимным 😌':
                    new_text = f'Автор: @{author}\n{text_idea}'
                    result.append(new_text)
                else:
                    new_text = f'Автор: {author}\n{text_idea}'
                    result.append(new_text)
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE ideas SET status=%s WHERE status IS NULL',
                (True, ))
            conn.commit()
            conn.close()
            return result

    elif argument is True:
        if len(ideas) == 0:
            return 'Идей от игроков пока нет 😌'
        else:
            result = []
            for elem in ideas:
                author = elem[0]
                text_idea = elem[1]
                if author != 'автор пожелал остаться анонимным 😌':
                    new_text = f'Автор: @{author}\n{text_idea}'
                    result.append(new_text)
                else:
                    new_text = f'Автор: {author}\n{text_idea}'
                    result.append(new_text)
            return result


def get_memes(argument):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT memes.author, memes.meme FROM memes WHERE status IS NULL')
    memes = cursor.fetchall()
    print(f'memes = {memes}')
    conn.close()

    if argument is None:
        if len(memes) == 0:
            return 'Новых мемов от игроков нет 😌'
        else:
            result = []
            for elem in memes:
                new_list = []
                author = elem[0]
                photo = elem[1]
                if author != 'автор пожелал остаться анонимным 😌':
                    new_text = f'Автор: @{author}'
                    new_list.append(new_text)
                    new_list.append(photo)
                    result.append(new_list)
                else:
                    new_text = f'Автор: {author}'
                    new_list.append(new_text)
                    new_list.append(photo)
                    result.append(new_list)
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE memes SET status=%s WHERE status IS NULL',
                (True, ))
            conn.commit()
            conn.close()
            return result

    elif argument is True:
        if len(memes) == 0:
            return 'Мемов от игроков пока нет 😌'
        else:
            result = []
            for elem in memes:
                new_list = []
                author = elem[0]
                photo = elem[1]
                if author != 'автор пожелал остаться анонимным 😌':
                    new_text = f'Автор: @{author}'
                    new_list.append(new_text)
                    new_list.append(photo)
                    result.append(new_list)
                else:
                    new_text = f'Автор: {author}'
                    new_list.append(new_text)
                    new_list.append(photo)
                    result.append(new_list)
            return result


def add_announcement(data, name):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        f'INSERT INTO game_announcement (announcement, name) VALUES (%s, %s)', (data, name, ))
    conn.commit()
    conn.close()


def delete_announcement():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM game_announcement')
    list_id = cursor.fetchall()
    conn.close()

    if len(list_id) != 0:
        list_id = [elem[0] for elem in list_id]
        list_id.sort()
        actual_id = list_id[-1]

        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM game_announcement WHERE id=%s', (actual_id, ))
        conn.commit()
        conn.close()


def add_history(data, name, status):
    if status == 'anonymous':
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO history (text, author) VALUES (%s, %s)',
                       (data, "автор пожелал остаться анонимным 😌"))
        conn.commit()
        conn.close()
    else:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO history (text, author) VALUES (%s, %s)', (data, name, ))
        conn.commit()
        conn.close()


def delete_history():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM history')
    list_id = cursor.fetchall()
    conn.close()

    if len(list_id) != 0:
        list_id = [elem[0] for elem in list_id]
        list_id.sort()
        actual_id = list_id[-1]

        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM history WHERE id=%s ', (actual_id, ))
        conn.commit()
        conn.close()


def add_idea(data, name, status):
    if status == 'anonymous':
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ideas (idea, author) VALUES (%s, %s)',
                       (data, "автор пожелал остаться анонимным 😌"))
        conn.commit()
        conn.close()
    else:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ideas (idea, author) VALUES (%s, %s)', (data, name))
        conn.commit()
        conn.close()


def delete_idea():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM ideas')
    list_id = cursor.fetchall()
    conn.close()

    if len(list_id) != 0:
        list_id = [elem[0] for elem in list_id]
        list_id.sort()
        actual_id = list_id[-1]

        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM ideas WHERE id=%s', (actual_id, ))
        conn.commit()
        conn.close()


def add_meme(data, author):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO memes (meme, author) VALUES (%s, %s)', (data, author))
    conn.commit()
    conn.close()


def delete_all_messages():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM game_announcement WHERE status=1')
    conn.commit()
    conn.close()

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM history WHERE status=1')
    conn.commit()
    conn.close()

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ideas WHERE status=1')
    conn.commit()
    conn.close()

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM memes WHERE status=1')
    conn.commit()
    conn.close()


def delete_some_messages(argument):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM %s', (argument, ))
    list_id = cursor.fetchall()
    conn.close()

    if len(list_id) != 0:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM %s WHERE status=1', (argument, ))
        conn.commit()
        conn.close()


@bot.message_handler(commands=['start', ])
def start(message: telebot.types.Message):
    print('ПРИШЛИ В СТАРТ')
    if message.chat.type == 'private':
        username = message.from_user.username
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if message.text == '/help_me':
            help_me(message)
        else:
            admins = get_admins()
            if username in admins:
                markup.add(types.KeyboardButton('Новые сообщения'),
                           types.KeyboardButton('Просмотренные сообщения'))
                bot.send_message(message.chat.id, text="Привет, администратор {0.first_name}!\nРеши, что хочешь"
                                                       " сделать :)".format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, admin_actions)
            else:
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="Привет, {0.first_name}!\nРеши, что хочешь сделать :)"
                                 .format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)


@bot.message_handler(commands=['help_me', ])
def help_me(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton('Вернуться в самое начало'))
        bot.send_message(message.chat.id, text='Привет, {0.first_name}!\nЯ помогу тебе разобраться :)\nЭтот бот '
                                               'служит помощником для админов телеграм канала "РИС (Ролевые '
                                               'Игры в Сербии)".\nТы можешь прислать боту свой ролевой мем, анонс '
                                               'своей игры или рассказать свою историю с ролевых игр. Админы '
                                               'канала всё посмотрят и решат, что с этим делать :)\n'
                                               'Просто иди по кнопкам, которые тебе предлагает бот и ни о чём не '
                                               'переживай 😌'.format(message.from_user),
                         reply_markup=markup)
        bot.register_next_step_handler(message, start)


@bot.message_handler(content_types=['text', 'photo'])
def handle_error(message):
    bot.send_message(message.chat.id,
                     text='*СЛИШКОМ МНОГО БУКВ 😳😳😳\nВОЗМОЖНО, ТЫ ВВЕЛ БОЛЬШОЙ ТЕКСТ И ТЕЛЕГРАММ АВТОМАТИЧЕСКИ'
                          ' РАЗДЕЛИЛ ЕГО НА НЕСКОЛЬКО ЧАСТЕЙ, ТАК КАК У ТЕЛЕГРАММА ЕСТЬ СВОИ ОГРАНИЧЕНИЯ ПО'
                          ' КОЛИЧЕСТВУ СИМВОЛОВ В ПОСТЕ.\nВЕРНИСЬ В САМОЕ НАЧАЛО ПРИ ПОМОЩИ КОМАНДЫ "start" В СИНЕЙ'
                          ' ПЛАШКЕ МЕНЮ, ЗАПОЛНИ ВСЁ ЗАНОВО С УЧЁТОМ СОКРАЩЁННОГО ТЕКСТА :)\nВ ПРОТИВНОМ СЛУЧАЕ АДМИН'
                          ' ПОЛУЧИТ ЛИШЬ ЧАСТЬ ТВОЕГО ТЕКСТА 😕*'
                     .format(message.from_user), parse_mode='Markdown')
    # bot.register_next_step_handler(message, start)


def admin_actions(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Новые сообщения'),
                           types.KeyboardButton('Просмотренные сообщения'))
                bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                bot.register_next_step_handler(message, admin_actions)
            elif message.text == 'Новые сообщения':
                markup.add(types.KeyboardButton('Анонсы игр'), types.KeyboardButton('Ролевые истории'),
                           types.KeyboardButton('Идеи для развития сообщества'),
                           types.KeyboardButton('Ролевые мемы'),
                           types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id, text='Реши, что хочешь посмотреть и нажми на эту кнопку :)',
                                 reply_markup=markup)
                bot.register_next_step_handler(message, view_messages, None)
            elif message.text == 'Просмотренные сообщения':
                markup.add(types.KeyboardButton('Анонсы игр'), types.KeyboardButton('Ролевые истории'),
                           types.KeyboardButton('Идеи для развития сообщества'),
                           types.KeyboardButton('Ролевые мемы'),
                           types.KeyboardButton('Вернуться в главное меню'),
                           types.KeyboardButton('Удалить все просмотренные сообщения'))
                bot.send_message(message.chat.id, text='Реши, что хочешь посмотреть и нажми на эту кнопку :)',
                                 reply_markup=markup)
                bot.register_next_step_handler(message, view_messages, True)
            else:
                markup.add(types.KeyboardButton('Новые сообщения'), types.KeyboardButton('Просмотренные сообщения'))
                bot.send_message(message.chat.id,
                                 text='{0.first_name}, ты что-то не то нажимаешь😌\nВыбери один из '
                                      'вариантов, представленных ниже :)'.format(message.from_user),
                                 reply_markup=markup)
                bot.register_next_step_handler(message, admin_actions)
        else:
            markup.add(types.KeyboardButton('Новые сообщения'), types.KeyboardButton('Просмотренные сообщения'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь или шлешь нам картинки 😌\nВыбери один '
                                  'из вариантов, представленных ниже :)'.format(message.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(message, admin_actions)


def view_messages(message, argument):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Новые сообщения'),
                           types.KeyboardButton('Просмотренные сообщения'))
                bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                bot.register_next_step_handler(message, admin_actions)
            elif message.text == 'Удалить все просмотренные сообщения':
                markup.add(types.KeyboardButton('Да!'),
                           types.KeyboardButton('Неть ☺️'))
                bot.send_message(message.chat.id, text='Ты правда хочешь удалить все просмотренные сообщения?',
                                 reply_markup=markup)
                bot.register_next_step_handler(message, delete_messages)
            elif argument is True:
                if message.text == 'Анонсы игр':
                    announcements = get_announcements(argument)
                    if type(announcements) is str:
                        markup.add(types.KeyboardButton('Новые сообщения'),
                                   types.KeyboardButton('Просмотренные сообщения'))
                        bot.send_message(message.chat.id, text=announcements)
                        bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                        bot.register_next_step_handler(message, admin_actions)
                    else:
                        markup.add(types.KeyboardButton('Удалить просмотренные анонсы'),
                                   types.KeyboardButton('Вернуться в главное меню'))
                        for i in range(len(announcements)):
                            if i == len(announcements) - 1:
                                bot.send_message(message.chat.id, text=announcements[i], reply_markup=markup)
                                bot.register_next_step_handler(message, delete_or_not)
                            else:
                                bot.send_message(message.chat.id, text=announcements[i])
                elif message.text == 'Ролевые истории':
                    stories = get_stories(argument)
                    if type(stories) is str:
                        markup.add(types.KeyboardButton('Новые сообщения'),
                                   types.KeyboardButton('Просмотренные сообщения'))
                        bot.send_message(message.chat.id, text=stories)
                        bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                        bot.register_next_step_handler(message, admin_actions)
                    else:
                        markup.add(types.KeyboardButton('Удалить просмотренные ролевые истории'),
                                   types.KeyboardButton('Вернуться в главное меню'))
                        for i in range(len(stories)):
                            if i == len(stories) - 1:
                                bot.send_message(message.chat.id, text=stories[i], reply_markup=markup)
                                bot.register_next_step_handler(message, delete_or_not)
                            else:
                                bot.send_message(message.chat.id, text=stories[i])
                elif message.text == 'Идеи для развития сообщества':
                    ideas = get_ideas(argument)
                    if type(ideas) is str:
                        markup.add(types.KeyboardButton('Новые сообщения'),
                                   types.KeyboardButton('Просмотренные сообщения'))
                        bot.send_message(message.chat.id, text=ideas)
                        bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                        bot.register_next_step_handler(message, admin_actions)
                    else:
                        markup.add(types.KeyboardButton('Удалить просмотренные идеи'),
                                   types.KeyboardButton('Вернуться в главное меню'))
                        for i in range(len(ideas)):
                            if i == len(ideas) - 1:
                                bot.send_message(message.chat.id, text=ideas[i], reply_markup=markup)
                                bot.register_next_step_handler(message, delete_or_not)
                            else:
                                bot.send_message(message.chat.id, text=ideas[i])
                elif message.text == 'Ролевые мемы':
                    memes = get_memes(argument)
                    if type(memes) is str:
                        markup.add(types.KeyboardButton('Новые сообщения'),
                                   types.KeyboardButton('Просмотренные сообщения'))
                        bot.send_message(message.chat.id, text=memes)
                        bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                        bot.register_next_step_handler(message, admin_actions)
                    else:
                        markup.add(types.KeyboardButton('Удалить просмотренные мемы'),
                                   types.KeyboardButton('Вернуться в главное меню'))
                        for i in range(len(memes)):
                            text = memes[i][0]
                            photo = memes[i][1]
                            if i == len(memes) - 1:
                                bot.send_photo(message.chat.id, photo, text, reply_markup=markup)
                                bot.register_next_step_handler(message, delete_or_not)
                            else:
                                bot.send_photo(message.chat.id, photo, text)
                else:
                    markup.add(types.KeyboardButton('Анонсы игр'), types.KeyboardButton('Ролевые истории'),
                               types.KeyboardButton('Идеи для развития сообщества'),
                               types.KeyboardButton('Ролевые мемы'),
                               types.KeyboardButton('Вернуться в главное меню'))
                    bot.send_message(message.chat.id,
                                     text='{0.first_name}, ты что-то не то нажимаешь😌\nВыбери один из '
                                          'вариантов, представленных ниже :)'.format(message.from_user),
                                     reply_markup=markup)
                    bot.register_next_step_handler(message, view_messages, True)
            elif argument is None:
                if message.text == 'Анонсы игр':
                    announcements = get_announcements(argument)
                    if type(announcements) is str:
                        markup.add(types.KeyboardButton('Новые сообщения'),
                                   types.KeyboardButton('Просмотренные сообщения'))
                        bot.send_message(message.chat.id, text=announcements)
                        bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                        bot.register_next_step_handler(message, admin_actions)
                    else:
                        markup.add(types.KeyboardButton('Вернуться в главное меню'))
                        for i in range(len(announcements)):
                            if i == len(announcements) - 1:
                                bot.send_message(message.chat.id, text=announcements[i], reply_markup=markup)
                                bot.register_next_step_handler(message, admin_actions)
                            else:
                                bot.send_message(message.chat.id, text=announcements[i])
                elif message.text == 'Ролевые истории':
                    stories = get_stories(argument)
                    if type(stories) is str:
                        markup.add(types.KeyboardButton('Новые сообщения'),
                                   types.KeyboardButton('Просмотренные сообщения'))
                        bot.send_message(message.chat.id, text=stories)
                        bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                        bot.register_next_step_handler(message, admin_actions)
                    else:
                        markup.add(types.KeyboardButton('Вернуться в главное меню'))
                        for i in range(len(stories)):
                            if i == len(stories) - 1:
                                bot.send_message(message.chat.id, text=stories[i], reply_markup=markup)
                                bot.register_next_step_handler(message, admin_actions)
                            else:
                                bot.send_message(message.chat.id, text=stories[i])
                elif message.text == 'Идеи для развития сообщества':
                    ideas = get_ideas(argument)
                    if type(ideas) is str:
                        markup.add(types.KeyboardButton('Новые сообщения'),
                                   types.KeyboardButton('Просмотренные сообщения'))
                        bot.send_message(message.chat.id, text=ideas)
                        bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                        bot.register_next_step_handler(message, admin_actions)
                    else:
                        markup.add(types.KeyboardButton('Вернуться в главное меню'))
                        for i in range(len(ideas)):
                            if i == len(ideas) - 1:
                                bot.send_message(message.chat.id, text=ideas[i], reply_markup=markup)
                                bot.register_next_step_handler(message, admin_actions)
                            else:
                                bot.send_message(message.chat.id, text=ideas[i])
                elif message.text == 'Ролевые мемы':
                    memes = get_memes(argument)
                    if type(memes) is str:
                        markup.add(types.KeyboardButton('Новые сообщения'),
                                   types.KeyboardButton('Просмотренные сообщения'))
                        bot.send_message(message.chat.id, text=memes)
                        bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                        bot.register_next_step_handler(message, admin_actions)
                    else:
                        markup.add(types.KeyboardButton('Вернуться в главное меню'))
                        for i in range(len(memes)):
                            text = memes[i][0]
                            photo = memes[i][1]
                            if i == len(memes) - 1:
                                bot.send_photo(message.chat.id, photo, text, reply_markup=markup)
                                bot.register_next_step_handler(message, admin_actions)
                            else:
                                bot.send_photo(message.chat.id, photo, text)
                else:
                    markup.add(types.KeyboardButton('Анонсы игр'), types.KeyboardButton('Ролевые истории'),
                               types.KeyboardButton('Идеи для развития сообщества'),
                               types.KeyboardButton('Ролевые мемы'),
                               types.KeyboardButton('Вернуться в главное меню'))
                    bot.send_message(message.chat.id,
                                     text='{0.first_name}, ты что-то не то нажимаешь😌\nВыбери один из '
                                          'вариантов, представленных ниже :)'.format(message.from_user),
                                     reply_markup=markup)
                    bot.register_next_step_handler(message, view_messages, None)
            else:
                markup.add(types.KeyboardButton('Анонсы игр'), types.KeyboardButton('Ролевые истории'),
                           types.KeyboardButton('Идеи для развития сообщества'),
                           types.KeyboardButton('Ролевые мемы'),
                           types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id,
                                 text='{0.first_name}, ты что-то не то нажимаешь 😌\nВыбери один '
                                      'из вариантов, представленных ниже :)'.format(message.from_user),
                                 reply_markup=markup)
                bot.register_next_step_handler(message, view_messages, '-')

        else:
            markup.add(types.KeyboardButton('Анонсы игр'), types.KeyboardButton('Ролевые истории'),
                       types.KeyboardButton('Идеи для развития сообщества'),
                       types.KeyboardButton('Ролевые мемы'),
                       types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь или шлешь нам картинки 😌\nВыбери один '
                                  'из вариантов, представленных ниже :)'.format(message.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(message, view_messages, '-')


def delete_messages(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Новые сообщения'),
                           types.KeyboardButton('Просмотренные сообщения'))
                bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                bot.register_next_step_handler(message, admin_actions)
            else:
                if message.text == 'Да!':
                    delete_all_messages()
                    markup.add(types.KeyboardButton('Новые сообщения'),
                               types.KeyboardButton('Просмотренные сообщения'))
                    bot.send_message(message.chat.id, text='Все просмотренные сообщения удалены ✅')
                    bot.send_message(message.chat.id, text='Реши, что хочешь посмотреть :)', reply_markup=markup)
                    bot.register_next_step_handler(message, admin_actions)
                elif message.text == 'Неть ☺️':
                    markup.add(types.KeyboardButton('Новые сообщения'),
                               types.KeyboardButton('Просмотренные сообщения'))
                    bot.send_message(message.chat.id, text='Реши, что хочешь посмотреть :)', reply_markup=markup)
                    bot.register_next_step_handler(message, admin_actions)
                else:
                    pass
        else:
            markup.add(types.KeyboardButton('Да!'),
                       types.KeyboardButton('Неть ☺️'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь или шлешь нам картинки 😌\nЛучше реши, '
                                  'ты правда хочешь удалить все просмотренные сообщения?'.format(message.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(message, delete_messages)


def delete_or_not(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Новые сообщения'),
                           types.KeyboardButton('Просмотренные сообщения'))
                bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                bot.register_next_step_handler(message, admin_actions)
            elif message.text == 'Удалить просмотренные анонсы':
                markup.add(types.KeyboardButton('Да!'),
                           types.KeyboardButton('Неть ☺️'))
                bot.send_message(message.chat.id, text='Ты правда хочешь удалить все просмотренные анонсы?',
                                 reply_markup=markup)
                bot.register_next_step_handler(message, delete_many_messages, 'game_announcement')
            elif message.text == 'Удалить просмотренные ролевые истории':
                markup.add(types.KeyboardButton('Да!'),
                           types.KeyboardButton('Неть ☺️'))
                bot.send_message(message.chat.id, text='Ты правда хочешь удалить все просмотренные истории?',
                                 reply_markup=markup)
                bot.register_next_step_handler(message, delete_many_messages, 'history')
            elif message.text == 'Удалить просмотренные идеи':
                markup.add(types.KeyboardButton('Да!'),
                           types.KeyboardButton('Неть ☺️'))
                bot.send_message(message.chat.id, text='Ты правда хочешь удалить все просмотренные идеи?',
                                 reply_markup=markup)
                bot.register_next_step_handler(message, delete_many_messages, 'ideas')
            elif message.text == 'Удалить просмотренные мемы':
                markup.add(types.KeyboardButton('Да!'),
                           types.KeyboardButton('Неть ☺️'))
                bot.send_message(message.chat.id, text='Ты правда хочешь удалить все просмотренные мемы?',
                                 reply_markup=markup)
                bot.register_next_step_handler(message, delete_many_messages, 'memes')
            else:
                markup.add(types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id,
                                 text='{0.first_name}, ты что-то не то нажимаешь 😌\nВернись в начало '
                                      ':)'.format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, admin_actions)
        else:
            markup.add(types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь или шлешь нам картинки 😌\nВернись '
                                  'в начало :)'.format(message.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(message, admin_actions)


def delete_many_messages(message, argument):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Новые сообщения'),
                           types.KeyboardButton('Просмотренные сообщения'))
                bot.send_message(message.chat.id, text='Реши, что будешь делать :)', reply_markup=markup)
                bot.register_next_step_handler(message, admin_actions)
            else:
                if message.text == 'Да!':
                    delete_some_messages(argument)
                    bot.send_message(message.chat.id, text='Готово ✅', reply_markup=markup)
                    markup.add(types.KeyboardButton('Новые сообщения'),
                               types.KeyboardButton('Просмотренные сообщения'))
                    bot.send_message(message.chat.id, text='Реши, что хочешь посмотреть :)', reply_markup=markup)
                    bot.register_next_step_handler(message, admin_actions)
                elif message.text == 'Неть ☺️':
                    markup.add(types.KeyboardButton('Новые сообщения'),
                               types.KeyboardButton('Просмотренные сообщения'))
                    bot.send_message(message.chat.id, text='Реши, что хочешь посмотреть :)', reply_markup=markup)
                    bot.register_next_step_handler(message, admin_actions)
                else:
                    markup.add(types.KeyboardButton('Вернуться в главное меню'))
                    bot.send_message(message.chat.id,
                                     text='{0.first_name}, ты что-то не то нажимаешь 😌\nВернись '
                                          'в начало :)'.format(message.from_user), reply_markup=markup)
                    bot.register_next_step_handler(message, admin_actions)
        else:
            markup.add(types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь или шлешь нам картинки 😌\nВернись '
                                  'в начало :)'.format(message.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(message, admin_actions)


def user_actions(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            else:
                if message.text == 'Прислать новость 📝':
                    markup.add(types.KeyboardButton('Прислать анонс своей игры 🎭'),
                               types.KeyboardButton('Прислать офигительную историю из своей ролевой жизни 🌚'),
                               types.KeyboardButton('Прислать идею для развития ролевого движения в Сербии 🍷'),
                               types.KeyboardButton('Вернуться в главное меню'))
                    bot.send_message(message.chat.id,
                                     text='{0.first_name}, выбери, что хочешь сделать :)'.
                                     format(message.from_user), reply_markup=markup, )
                    bot.register_next_step_handler(message, send_news)
                elif message.text == 'Прислать мем 🦄':
                    markup.add(types.KeyboardButton('Вернуться в главное меню'))
                    bot.send_message(message.chat.id,
                                     text='{0.first_name}, здесь мы будем собирать наши собственные ролевые мемы!'.
                                     format(message.from_user))
                    picture = get_example_meme()
                    text = 'Например, вот такой ролевой мем с "Последнего Оплота"'
                    bot.send_photo(message.chat.id, picture, text)
                    bot.send_message(message.chat.id,
                                     text='Загрузи свой мем :) Просто прикрепи изображение '
                                          ':)\nЕсли передумал, то вернись в главное меню :)'.format(message.from_user),
                                     reply_markup=markup)
                    bot.register_next_step_handler(message, send_meme)
                else:
                    markup.add(types.KeyboardButton('Прислать новость 📝'),
                               types.KeyboardButton('Прислать мем 🦄'))
                    bot.send_message(message.chat.id,
                                     text='{0.first_name}, ты что-то не то нажимаешь😌\nВыбери один из '
                                          'вариантов, представленных ниже :)'.format(message.from_user),
                                     reply_markup=markup)
                    bot.register_next_step_handler(message, user_actions)

        else:
            markup.add(types.KeyboardButton('Прислать новость 📝'),
                       types.KeyboardButton('Прислать мем 🦄'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь😌\nВыбери один из '
                                  'вариантов, представленных ниже :)'.format(message.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(message, user_actions)


def send_news(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="Реши, что хочешь сделать :)".format(message.from_user),
                                 reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            else:
                if message.text == 'Прислать анонс своей игры 🎭':
                    markup.add(types.KeyboardButton('Отправить свой анонс'),
                               types.KeyboardButton('Создать анонс по шаблону'),
                               types.KeyboardButton('Вернуться в главное меню'))
                    bot.send_message(message.chat.id,
                                     text='Выбери, что хочешь сделать :)'.
                                     format(message.from_user), reply_markup=markup, )
                    bot.register_next_step_handler(message, announcement)

                elif message.text == 'Прислать офигительную историю из своей ролевой жизни 🌚':
                    markup.add(types.KeyboardButton('Пусть все знают моё имя! 💃'),
                               types.KeyboardButton('Нет, я стесняшка, хочу быть анонимным 👀'),
                               types.KeyboardButton('Вернуться в главное меню'))
                    bot.send_message(message.chat.id, text='Для начала уточним, хочешь ли ты остаться анонимным или '
                                                           'пусть все знают автора истории? 😏', reply_markup=markup)
                    bot.register_next_step_handler(message, history)

                elif message.text == 'Прислать идею для развития ролевого движения в Сербии 🍷':
                    markup.add(types.KeyboardButton('Пусть все знают моё имя! 💃'),
                               types.KeyboardButton('Нет, я стесняшка, хочу быть анонимным 👀'),
                               types.KeyboardButton('Вернуться в главное меню'))
                    bot.send_message(message.chat.id, text='Для начала уточним, хочешь ли ты остаться анонимным или '
                                                           'пусть все знают автора идеи? 😏', reply_markup=markup)
                    bot.register_next_step_handler(message, idea)
                else:
                    markup.add(types.KeyboardButton('Прислать анонс своей игры 🎭'),
                               types.KeyboardButton('Прислать офигительную историю из своей ролевой жизни 🌚'),
                               types.KeyboardButton('Прислать идею для развития ролевого движения в Сербии 🍷'),
                               types.KeyboardButton('Вернуться в главное меню'))
                    bot.send_message(message.chat.id,
                                     text='{0.first_name}, ты что-то не то нажимаешь😌\nВыбери один из '
                                          'вариантов, представленных ниже :)'.format(message.from_user),
                                     reply_markup=markup)
                    bot.register_next_step_handler(message, send_news)
        else:
            markup.add(types.KeyboardButton('Прислать анонс своей игры 🎭'),
                       types.KeyboardButton('Прислать офигительную историю из своей ролевой жизни 🌚'),
                       types.KeyboardButton('Прислать идею для развития ролевого движения в Сербии 🍷'),
                       types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь😌\nВыбери один из '
                                  'вариантов, представленных ниже :)'.format(message.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(message, send_news)


def send_meme(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        username = message.from_user.username
        if message.text == '/start':
            start(message)
        elif message.text == '/help_me':
            help_me(message)
        elif message.text == 'Вернуться в главное меню':
            markup.add(types.KeyboardButton('Прислать новость 📝'),
                       types.KeyboardButton('Прислать мем 🦄'))
            bot.send_message(message.chat.id, text="Привет, {0.first_name}! Реши, что хочешь сделать :)"
                             .format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, user_actions)
        else:
            content_type = message.content_type
            if content_type != 'photo':
                markup.add(types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id,
                                 text='{0.first_name}, ты что-то не то нажимаешь😌 или не отправляешь нам свои '
                                      'мемы😐\nЗагрузи свой мем (просто картинкой! не файлом!) или вернись в главное '
                                      'меню :)'.format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, send_meme)
            elif content_type == 'photo':
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                # photo = message.photo[-1]  # Берем изображение с наибольшим разрешением
                # add_inf_masters(photo.file_id, 'photo', username)
                # back_to_master_short_schedule(message)
                photo = message.photo[-1]
                add_meme(photo.file_id, username)
                bot.send_message(message.chat.id,
                                 text='Урааа! В нашей коллекции на один мем больше 😍😍😍\nСкоро админ посмотрит его '
                                      'и, возможно, поделится мемом в общей группе 😌\n'
                                      'Реши, что хочешь сделать дальше :)',
                                 reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)


def announcement(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="Реши, что хочешь сделать :)".format(message.from_user),
                                 reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            else:
                if message.text == 'Отправить свой анонс':
                    markup.add(types.KeyboardButton('Вернуться в главное меню'))
                    bot.send_message(message.chat.id, text='Напиши в свободной форме анонс своей игры :)'.
                                     format(message.from_user), reply_markup=markup)
                    bot.register_next_step_handler(message, send_announcement)
                elif message.text == 'Создать анонс по шаблону':
                    markup.add(types.KeyboardButton('Вернуться в главное меню'))
                    bot.send_message(message.chat.id, text='Скопируй текст и создай анонс своей игры по этому '
                                                           'шаблону и пришли в следующем сообщении :)')
                    bot.send_message(message.chat.id, text='Название:\nКогда:\nГде:\nСколько стоит:\nТекст анонса:',
                                     reply_markup=markup)
                    bot.register_next_step_handler(message, send_announcement)
                else:
                    markup.add(types.KeyboardButton('Отправить свой анонс'),
                               types.KeyboardButton('Создать анонс по шаблону'),
                               types.KeyboardButton('Вернуться в главное меню'))
                    bot.send_message(message.chat.id,
                                     text='{0.first_name}, ты что-то не то нажимаешь😌\nВыбери один из '
                                          'вариантов, представленных ниже :)'.format(message.from_user),
                                     reply_markup=markup)
                    bot.register_next_step_handler(message, announcement)
        else:
            markup.add(types.KeyboardButton('Отправить свой анонс'),
                       types.KeyboardButton('Создать анонс по шаблону'),
                       types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь😌\nВыбери один из '
                                  'вариантов, представленных ниже :)'.format(message.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(message, announcement)


def send_announcement(message):
    if message.chat.type == 'private':
        username = message.from_user.username
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="Реши, что хочешь сделать :)", reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            else:
                add_announcement(message.text, username)
                markup.add(types.KeyboardButton('Всё круто, отправить анонс админу 💃'),
                           types.KeyboardButton('Нет, поправлю немного 👀'),
                           types.KeyboardButton('Передумал отправлять анонс 🌚'))
                bot.send_message(message.chat.id, text='{0.first_name}, ещё раз прочитай и проверь свой '
                                                       'анонс 😌'.format(message.from_user))
                bot.send_message(message.chat.id, text=message.text, reply_markup=markup)
                bot.register_next_step_handler(message, finally_send_announcement)
        else:
            markup.add(types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь😌 или шлешь нам картинки вместо текста '
                                  'анонса 🙃\nНапиши анонс своей игры или вернись в главное '
                                  'меню :)'.format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, send_announcement)


def finally_send_announcement(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                delete_announcement()
                start(message)
            elif message.text == '/help_me':
                delete_announcement()
                help_me(message)
            elif message.text == 'Всё круто, отправить анонс админу 💃':
                bot.send_message(message.chat.id, text='Анонс твоей игры отправлен админу :)\nЕсли у админа '
                                                       'возникнут вопросы по твоей игре - он тебе напишет :)')
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="{0.first_name}, реши, что хочешь сделать :)"
                                 .format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            elif message.text == 'Нет, поправлю немного 👀':
                delete_announcement()
                markup.add(types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id, text='Отправь новый анонс своей игры :)'.
                                 format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, send_announcement)
            elif message.text == 'Передумал отправлять анонс 🌚':
                delete_announcement()
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="{0.first_name}, реши, что хочешь сделать :)"
                                 .format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            else:
                markup.add(types.KeyboardButton('Всё круто, отправить анонс админу 💃'),
                           types.KeyboardButton('Нет, поправлю немного 👀'),
                           types.KeyboardButton('Передумал отправлять анонс 🌚'))
                bot.send_message(message.chat.id,
                                 text='{0.first_name}, ты что-то не то нажимаешь😌 \nВыбери один из этих вариантов, '
                                      'что делать с твоим анонсом :)'.format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, finally_send_announcement)
        else:
            markup.add(types.KeyboardButton('Всё круто, отправить анонс админу 💃'),
                       types.KeyboardButton('Нет, поправлю немного 👀'),
                       types.KeyboardButton('Передумал отправлять анонс 🌚'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь😌 или шлешь нам картинки вместо текста '
                                  'анонса 🙃\nВыбери один из этих вариантов, что делать с твоим анонсом '
                                  ':)'.format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, finally_send_announcement)


def history(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="Реши, что хочешь сделать :)", reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            elif message.text == 'Пусть все знают моё имя! 💃':
                markup.add(types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id,
                                 text='{0.first_name}, хорошо!\nНапиши сюда то, чем хочешь поделиться с сообществом '
                                      'ролевиков ☺️\nМожет твоя история появится в группе или ляжет в основу новой '
                                      'игры ☺️'.format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, send_history)
            elif message.text == 'Нет, я стесняшка, хочу быть анонимным 👀':
                markup.add(types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id,
                                 text='{0.first_name}, хорошо!\nНапиши сюда то, чем хочешь поделиться с сообществом '
                                      'ролевиков ☺️\nМожет твоя история появится в группе или ляжет в основу новой '
                                      'игры ☺️'.format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, send_history_anonymous)
            else:
                markup.add(types.KeyboardButton('Пусть все знают моё имя! 💃'),
                           types.KeyboardButton('Нет, я стесняшка, хочу быть анонимным 👀'),
                           types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id, text='И всё-таки давай сначала решим, хочешь ли ты остаться '
                                                       'анонимным или пусть все знают автора истории? 😏',
                                 reply_markup=markup)
                bot.register_next_step_handler(message, history)
        else:
            markup.add(types.KeyboardButton('Пусть все знают моё имя! 💃'),
                       types.KeyboardButton('Нет, я стесняшка, хочу быть анонимным 👀'),
                       types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь😌 или шлешь нам картинки вместо ответа на '
                                  'вопросы 🙃\nРеши, хочешь ли ты прислать историю анонимно или нет :)\n'
                                  'Или вернись в главное меню'.format(message.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(message, history)


def send_history(message):
    if message.chat.type == 'private':
        username = message.from_user.username
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="Реши, что хочешь сделать :)", reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            else:
                add_history(message.text, username, 'identified')
                markup.add(types.KeyboardButton('Всё круто, отправить историю админу 💃'),
                           types.KeyboardButton('Нет, поправлю немного 👀'),
                           types.KeyboardButton('Передумал отправлять историю 🌚'))
                bot.send_message(message.chat.id, text='{0.first_name}, ещё раз прочитай и проверь свою историю '
                                                       '😌'.format(message.from_user))
                bot.send_message(message.chat.id, text=message.text, reply_markup=markup)
                bot.register_next_step_handler(message, finally_send_history)
        else:
            markup.add(types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь😌 или шлешь нам картинки вместо текста '
                                  'истории 🙃\nНапиши свою историю или вернись в главное меню '
                                  ':)'.format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, send_history)


def send_history_anonymous(message):
    if message.chat.type == 'private':
        username = message.from_user.username
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="Реши, что хочешь сделать :)", reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            else:
                add_history(message.text, username, 'anonymous')
                markup.add(types.KeyboardButton('Всё круто, отправить историю админу 💃'),
                           types.KeyboardButton('Нет, поправлю немного 👀'),
                           types.KeyboardButton('Передумал отправлять историю 🌚'))
                bot.send_message(message.chat.id, text='{0.first_name}, ещё раз прочитай и проверь свою историю '
                                                       '😌'.format(message.from_user))
                bot.send_message(message.chat.id, text=message.text, reply_markup=markup)
                bot.register_next_step_handler(message, finally_send_history)
        else:
            markup.add(types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь😌 или шлешь нам картинки вместо текста '
                                  'истории 🙃\nНапиши свою историю или вернись в главное меню '
                                  ':)'.format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, send_history_anonymous)


def finally_send_history(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                delete_history()
                start(message)
            elif message.text == '/help_me':
                delete_history()
                help_me(message)
            elif message.text == 'Всё круто, отправить историю админу 💃':
                bot.send_message(message.chat.id, text='Твоя история отправлена админу :)\nЕсли у админа '
                                                       'возникнут вопросы - он тебе напишет :)')
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="{0.first_name}, реши, что хочешь сделать :)"
                                 .format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            elif message.text == 'Нет, поправлю немного 👀':
                delete_history()
                markup.add(types.KeyboardButton('Пусть все знают моё имя! 💃'),
                           types.KeyboardButton('Нет, я стесняшка, хочу быть анонимным 👀'),
                           types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id, text='Напомни, пожалуйста, хочешь ли ты остаться анонимным или '
                                                       'пусть все знают автора истории? 😏', reply_markup=markup)
                bot.register_next_step_handler(message, history)
            elif message.text == 'Передумал отправлять историю 🌚':
                delete_history()
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="{0.first_name}, реши, что хочешь сделать :)"
                                 .format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            else:
                markup.add(types.KeyboardButton('Всё круто, отправить историю админу 💃'),
                           types.KeyboardButton('Нет, поправлю немного 👀'),
                           types.KeyboardButton('Передумал отправлять историю 🌚'))
                bot.send_message(message.chat.id,
                                 text='{0.first_name}, ты что-то не то нажимаешь😌 \nВыбери один из этих вариантов, '
                                      'что делать с твоей историей :)'.format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, finally_send_history)
        else:
            markup.add(types.KeyboardButton('Всё круто, отправить историю админу 💃'),
                       types.KeyboardButton('Нет, поправлю немного 👀'),
                       types.KeyboardButton('Передумал отправлять историю 🌚'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь или шлешь нам картинки вместо текста 😌'
                                  '\nВыбери один из этих вариантов, что делать с твоей историей '
                                  ':)'.format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, finally_send_history)


def idea(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="Реши, что хочешь сделать :)", reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            elif message.text == 'Пусть все знают моё имя! 💃':
                markup.add(types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id,
                                 text='{0.first_name}, хорошо!\nНапиши сюда свои мысли и идеи, что бы ты хотел '
                                      'улучшить/предложить нового для развития ролевого движения или для '
                                      'развития этого канала ☺️\nАдмин прочитает и, если его заинтересует твоя идея, '
                                      'свяжется с тобой для уточнения подробностей, если ты указал свой '
                                      'контакт :)\nИ давай сразу договоримся, что админ по своему желанию может '
                                      'использовать или не использовать твои идеи и что ты делишься ими безвозмездно '
                                      '☺️'.format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, send_idea)
            elif message.text == 'Нет, я стесняшка, хочу быть анонимным 👀':
                markup.add(types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id,
                                 text='{0.first_name}, хорошо!\nНапиши сюда свои мысли и идеи, что бы ты хотел '
                                      'улучшить/предложить нового для развития ролевого движения или для '
                                      'развития этого канала ☺️\nАдмин прочитает и, если его заинтересует твоя идея, '
                                      'свяжется с тобой для уточнения подробностей, если ты указал свой '
                                      'контакт :)\nИ давай сразу договоримся, что админ по своему желанию может '
                                      'использовать или не использовать твои идеи и что ты делишься ими безвозмездно '
                                      '☺️'.format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, send_idea_anonymous)
            else:
                markup.add(types.KeyboardButton('Пусть все знают моё имя! 💃'),
                           types.KeyboardButton('Нет, я стесняшка, хочу быть анонимным 👀'),
                           types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id, text='И всё-таки давай сначала решим, хочешь ли ты остаться '
                                                       'анонимным или нет? 😏',
                                 reply_markup=markup)
                bot.register_next_step_handler(message, idea)
        else:
            markup.add(types.KeyboardButton('Пусть все знают моё имя! 💃'),
                       types.KeyboardButton('Нет, я стесняшка, хочу быть анонимным 👀'),
                       types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь😌 или шлешь нам картинки вместо ответа на '
                                  'вопросы 🙃\nРеши, хочешь ли ты прислать свои идеи анонимно или нет :)\n'
                                  'Или вернись в главное меню'.format(message.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(message, idea)


def send_idea(message):
    if message.chat.type == 'private':
        username = message.from_user.username
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="Реши, что хочешь сделать :)", reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            else:
                add_idea(message.text, username, 'identified')
                markup.add(types.KeyboardButton('Всё круто, отправить идеи админу 💃'),
                           types.KeyboardButton('Нет, поправлю немного 👀'),
                           types.KeyboardButton('Передумал отправлять идеи 🌚'))
                bot.send_message(message.chat.id, text='{0.first_name}, ещё раз прочитай и проверь свою идеи '
                                                       '😌'.format(message.from_user))
                bot.send_message(message.chat.id, text=message.text, reply_markup=markup)
                bot.register_next_step_handler(message, finally_send_idea)
        else:
            markup.add(types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь😌 или шлешь нам картинки вместо своих '
                                  'идей 🙃\nНапиши свою идеи или вернись в главное меню '
                                  ':)'.format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, send_idea)


def send_idea_anonymous(message):
    if message.chat.type == 'private':
        username = message.from_user.username
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                start(message)
            elif message.text == '/help_me':
                help_me(message)
            elif message.text == 'Вернуться в главное меню':
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="Реши, что хочешь сделать :)", reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            else:
                add_idea(message.text, username, 'anonymous')
                markup.add(types.KeyboardButton('Всё круто, отправить идеи админу 💃'),
                           types.KeyboardButton('Нет, поправлю немного 👀'),
                           types.KeyboardButton('Передумал отправлять идеи 🌚'))
                bot.send_message(message.chat.id, text='{0.first_name}, ещё раз прочитай и проверь свою идеи '
                                                       '😌'.format(message.from_user))
                bot.send_message(message.chat.id, text=message.text, reply_markup=markup)
                bot.register_next_step_handler(message, finally_send_idea)
        else:
            markup.add(types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь😌 или шлешь нам картинки вместо своих '
                                  'идей 🙃\nНапиши свою идеи или вернись в главное меню '
                                  ':)'.format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, send_idea_anonymous)


def finally_send_idea(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if type(message.text) is str:
            if message.text == '/start':
                delete_idea()
                start(message)
            elif message.text == '/help_me':
                delete_idea()
                help_me(message)
            elif message.text == 'Всё круто, отправить идеи админу 💃':
                bot.send_message(message.chat.id, text='Твои идеи отправлены админу :)\nЕсли у админа '
                                                       'возникнут вопросы - он тебе напишет :)')
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="{0.first_name}, реши, что хочешь сделать :)"
                                 .format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            elif message.text == 'Нет, поправлю немного 👀':
                delete_idea()
                markup.add(types.KeyboardButton('Пусть все знают моё имя! 💃'),
                           types.KeyboardButton('Нет, я стесняшка, хочу быть анонимным 👀'),
                           types.KeyboardButton('Вернуться в главное меню'))
                bot.send_message(message.chat.id, text='Напомни, пожалуйста, хочешь ли ты остаться анонимным или '
                                                       'пусть все знают автора идеи? 😏', reply_markup=markup)
                bot.register_next_step_handler(message, idea)
            elif message.text == 'Передумал отправлять идеи 🌚':
                delete_idea()
                markup.add(types.KeyboardButton('Прислать новость 📝'),
                           types.KeyboardButton('Прислать мем 🦄'))
                bot.send_message(message.chat.id, text="{0.first_name}, реши, что хочешь сделать :)"
                                 .format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, user_actions)
            else:
                markup.add(types.KeyboardButton('Всё круто, отправить идеи админу 💃'),
                           types.KeyboardButton('Нет, поправлю немного 👀'),
                           types.KeyboardButton('Передумал отправлять идеи 🌚'))
                bot.send_message(message.chat.id,
                                 text='{0.first_name}, ты что-то не то нажимаешь😌 \nВыбери один из этих вариантов, '
                                      'что делать с твоими идеями :)'.format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, finally_send_idea)
        else:
            markup.add(types.KeyboardButton('Всё круто, отправить идеи админу 💃'),
                       types.KeyboardButton('Нет, поправлю немного 👀'),
                       types.KeyboardButton('Передумал отправлять идеи 🌚'))
            bot.send_message(message.chat.id,
                             text='{0.first_name}, ты что-то не то нажимаешь или шлешь нам картинки вместо текста 😌'
                                  '\nВыбери один из этих вариантов, что делать с твоими идеями '
                                  ':)'.format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, finally_send_idea)


# if __name__ == "__main__":
#     try:
#         print("Removing webhook...")
#         bot.remove_webhook()
#
#         print("Setting webhook...")
#         success = bot.set_webhook(url=WEBHOOK_URL)
#         print("Webhook set result:", success)
#     except Exception as e:
#         print("Webhook setup error:", e)
#
#     port = int(os.environ.get("PORT", 8080))
#     print(f"Starting Flask on port {port}")
#     app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    print('in if __name__ == "__main__"')
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
