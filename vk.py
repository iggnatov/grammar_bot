import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
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
        text = event.text.lower()
        user_id = event.user_id

        if text == 'начать':
            write_msg(user_id, bot_messages['hello_message'], get_default_keyboard())
            print(f'user_id: {user_id}')
            # save to database ?user_nick? & user_id

        elif text == 'правила':
            print('Some rules')
            write_msg(user_id, bot_messages['rules_message'], get_default_keyboard())

        elif text == 'тренировка':
            print('Practice')
            topic_buttons = get_topics_list_from_db()
            write_msg(user_id, bot_messages['choose_the_topic_message'], get_topics_keyboard(topic_buttons))

        else:
            pass
