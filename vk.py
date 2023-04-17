import json
import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import psycopg2
from psycopg2 import Error

# def connect():
#     # getting connection configs
#     db_config_path = '/Users/iggnatov/Documents/dev/grammar_bot/sql_setting_files/config_file.txt'
#     with open(db_config_path, 'r') as db_json_file:
#         db_j_data = json.load(db_json_file)
#
#     # connecting to database
#     try:
#         conn = psycopg2.connect(user=db_j_data['user'], password=db_j_data['password'],
#                                 host=db_j_data['host'], port='5433', database=db_j_data['dbname'])
#         cur = conn.cursor()
#
#         cur.execute("SELECT version();")
#         record = cur.fetchone()
#         print("You\'re connected to - ", record, "\n")
#
#         return conn, cur
#
#     except (Exception, Error) as error:
#         print("Error working with PostgreSQL", error)
#
#     finally:
#
#         print('Finally block of def connect()')

def get_topics_list_from_db():
    # getting connection configs
    db_config_path = '/Users/iggnatov/Documents/dev/grammar_bot/sql_setting_files/config_file.txt'
    with open(db_config_path, 'r') as db_json_file:
        db_j_data = json.load(db_json_file)

    # connecting to database
    try:
        conn = psycopg2.connect(user=db_j_data['user'], password=db_j_data['password'],
                                host=db_j_data['host'], port='5433', database=db_j_data['dbname'])
        cur = conn.cursor()

        cur.execute("SELECT version();")
        record = cur.fetchone()
        print(f'You\'re connected to - ",{record}\n' )

    except (Exception, Error) as error:
        print("Error working with PostgreSQL", error)

    finally:
        print('Finally block of def connect()')

    cur.execute(f"""SELECT set_name FROM word_sets WHERE set_status = 'ACTIVE';""")

    db_topic_list = cur.fetchall()
    cur.close()
    conn.close()
    print("Connection to PostgreSQL closed")

    topic_list = []
    for each_topic in db_topic_list:
        topic = each_topic[0]
        # print(topic)
        topic_list.append(topic)

    return topic_list


def erase_letter(word, index):
    correct_letter = word[index]
    word_with_gap = word[:index] + '_' + word[index+1:]
    return word_with_gap, correct_letter

def check(quiz_dict):
    # print(quiz_dict)
    correct_answer = ''
    attempt_score = 0
    tic = time.perf_counter()
    for word, gqp_index in quiz_dict.items():
        quiz_tuple = erase_letter(word, gqp_index)
        write_msg(user_id, quiz_tuple[0])
        for quiz_event in VkLongPoll(vk_session).listen():
            if quiz_event.type == VkEventType.MESSAGE_NEW and quiz_event.to_me:
                answer = quiz_event.text.lower()
                if answer == quiz_tuple[1].lower():
                    correct_answer = '+'
                    attempt_score += 1
                else:
                    correct_answer = '-'
                print(answer, correct_answer)
                break
    toc = time.perf_counter()
    attempt_time = round(toc - tic, 2)
    return attempt_score, attempt_time

def get_words_from_set(topic_text):
    # getting connection configs
    db_config_path = '/Users/iggnatov/Documents/dev/grammar_bot/sql_setting_files/config_file.txt'
    with open(db_config_path, 'r') as db_json_file:
        db_j_data = json.load(db_json_file)

    # connecting to database
    try:
        conn = psycopg2.connect(user=db_j_data['user'], password=db_j_data['password'],
                                host=db_j_data['host'], port='5433', database=db_j_data['dbname'])
        cur = conn.cursor()

        cur.execute("SELECT version();")
        record = cur.fetchone()
        print(f'You\'re connected to - ",{record}')

    except (Exception, Error) as error:
        print("Error working with PostgreSQL", error)

    finally:
        print('Finally block of def connect()')
    # get word_sets.id / now for example it's 42 - История
    cur.execute(f"""SELECT word_sets.id FROM word_sets WHERE set_name = '{topic_text}';""")
    word_set_id = cur.fetchone()[0]

    # get words
    cur.execute(f"""SELECT word, gap_index FROM words
                JOIN rel_words_sets
                ON words.id = rel_words_sets.id
                AND rel_words_sets.set_id = {word_set_id};""")

    word_list = cur.fetchall()
    word_dict = {}
    cur.close()
    conn.close()
    print("Connection to PostgreSQL closed\n")
    for elem in word_list:
        word_dict[elem[0]] = elem[1]

    return word_dict

def get_default_keyboard():
    default_buttons = ['Правила', 'Тренировка']
    default_keyboard = VkKeyboard(one_time=True)
    default_keyboard.add_button(default_buttons[0], VkKeyboardColor.PRIMARY)
    default_keyboard.add_button(default_buttons[1], VkKeyboardColor.PRIMARY)
    return default_keyboard


def get_topics_keyboard(topics_list):
    topic_keyboard = VkKeyboard(inline=True)
    btn_in_row = 0
    for btn in topics_list:
        btn_in_row += 1
        print(btn)
        if btn_in_row <= 2:
            topic_keyboard.add_button(btn, VkKeyboardColor.PRIMARY)
        else:
            topic_keyboard.add_line()
            btn_in_row = 0
    return topic_keyboard

def write_msg(user_id_, message, keyboard_=None):
    msg = {
        'user_id': user_id_,
        'message': message,
        'random_id': 0
    }

    if keyboard_ is not None:
        msg['keyboard'] = keyboard_.get_keyboard()

    vk_session.method('messages.send', msg)


config_path = '/Users/iggnatov/Documents/dev/grammar_bot/vk_setting_files/config_file.txt'
with open(config_path, 'r') as json_file:
    j_data = json.load(json_file)

vk_session = vk_api.VkApi(token=j_data['token'])

bot_messages_path = '/Users/iggnatov/Documents/dev/grammar_bot/vk_setting_files/messages.json'
with open(bot_messages_path, 'r') as json_file_bot_messages:
    bot_messages = json.load(json_file_bot_messages)


for event in VkLongPoll(vk_session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        # text = event.text.lower()
        text = event.text
        user_id = event.user_id

        if text == 'Начать':
            write_msg(user_id, bot_messages['hello_message'], get_default_keyboard())
            print(f'user_id: {user_id}')
            # save to database ?user_nick? & user_id

        elif text == 'Правила':
            print('Some rules')
            write_msg(user_id, bot_messages['rules_message'], get_default_keyboard())
            # и стоп тренировка

        elif text == 'Тренировка':
            print('Practice')
            topic_buttons = get_topics_list_from_db()
            write_msg(user_id, bot_messages['choose_the_topic_message'], get_topics_keyboard(topic_buttons))

        elif text in topic_buttons:
            # get word_sets.id
            # for example 42 - История
            word_set_id = 42

            # get list of words
            #  request
            # req = f"""SELECT word, gap_index FROM words
            # JOIN rel_words_sets
            # ON words.id = rel_words_sets.id
            # AND rel_words_sets.set_id = {word_set_id};"""
            result = check(get_words_from_set(text))
            res = result[0]
            attempt_result_msg = f'Твой результат: {res} правильных слов, за {result[1]} секунд!\n\n'

            if 0 <= res <= 3:
                attempt_result_msg += bot_messages["result_0003_message"]
            elif 4 <= res <= 6:
                attempt_result_msg += bot_messages["result_0406_message"]
            elif 7 <= res <= 10:
                attempt_result_msg += bot_messages["result_0710_message"]
            elif 11 <= res <= 13:
                attempt_result_msg += bot_messages["result_1113_message"]
            elif 14 <= res <= 16:
                attempt_result_msg += bot_messages["result_1416_message"]

            write_msg(user_id, attempt_result_msg, get_default_keyboard())


        else:
            pass
