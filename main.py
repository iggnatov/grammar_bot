import grammar
import json
import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

def vk_connect():
    config_path = '/Users/iggnatov/Documents/dev/grammar_bot/vk_setting_files/config_file.txt'
    with open(config_path, 'r') as json_file:
        j_data = json.load(json_file)

    vk_session = vk_api.VkApi(token=j_data['token'])
    return vk_session

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
        print(btn)
        if btn_in_row < 2:
            topic_keyboard.add_button(btn, VkKeyboardColor.PRIMARY)
            btn_in_row += 1
        else:
            topic_keyboard.add_line()
            topic_keyboard.add_button(btn, VkKeyboardColor.PRIMARY)
            btn_in_row = 1
    return topic_keyboard

def write_msg(user_id_, message, keyboard_=None):
    msg = {
        'user_id': user_id_,
        'message': message,
        'random_id': 0
    }

    if keyboard_ is not None:
        msg['keyboard'] = keyboard_.get_keyboard()

    session.method('messages.send', msg)

def get_bot_messages(case):
    bot_messages_path = '/Users/iggnatov/Documents/dev/grammar_bot/vk_setting_files/messages.json'
    with open(bot_messages_path, 'r') as json_file_bot_messages:
        bot_messages = json.load(json_file_bot_messages)

    if case == 'hello_message':
        return bot_messages['hello_message']
    elif case == 'rules_message':
        return bot_messages['rules_message']
    elif case == 'choose_the_topic_message':
        return bot_messages['choose_the_topic_message']
    elif case == 'result_0003_message':
        return bot_messages['result_0003_message']
    elif case == 'result_0406_message':
        return bot_messages['result_0406_message']
    elif case == 'result_0710_message':
        return bot_messages['result_0710_message']
    elif case == 'result_1113_message':
        return bot_messages['result_1113_message']
    elif case == 'result_1416_message':
        return bot_messages['result_1416_message']

# --- Тренировка --- #

# Тренировка на наборе слов
def check(user_id_, quiz_dict):
    correct_answer = ''
    attempt_score = 0
    tic = time.perf_counter()
    for word, gqp_index in quiz_dict.items():
        quiz_tuple = erase_letter(word, gqp_index)
        write_msg(user_id_, quiz_tuple[0])
        for quiz_event in VkLongPoll(session).listen():
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

# Подготовка набора слов (вырезание букв)
def erase_letter(word, index):
    correct_letter = word[index]
    word_with_gap = word[:index] + '_' + word[index + 1:]
    return word_with_gap, correct_letter

def chat_listen(vk_session):
    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            # text = event.text.lower()
            text = event.text
            user_id = event.user_id

            if text == 'Начать':
                write_msg(user_id, get_bot_messages('hello_message'), get_default_keyboard())
                print(f'user_id: {user_id}')
                # save to database ?user_nick? & user_id

            elif text == 'Правила':
                print('Some rules')
                write_msg(user_id, get_bot_messages('rules_message'), get_default_keyboard())
                # и стоп тренировка?

            elif text == 'Тренировка':
                print('Practice')
                topic_buttons = db.get_topics_list_from_db()
                write_msg(user_id, get_bot_messages('choose_the_topic_message'), get_topics_keyboard(topic_buttons))

            elif text in topic_buttons:
                # Получить набор слов на заданную тему
                check_list = db.get_words_from_set(text)

                result = check(user_id, check_list)
                res = result[0]
                attempt_result_msg = f'Твой результат: {res} правильных слов, за {result[1]} секунд!\n\n'

                if 0 <= res <= 3:
                    attempt_result_msg += get_bot_messages('result_0003_message')
                elif 4 <= res <= 6:
                    attempt_result_msg += get_bot_messages('result_0406_message')
                elif 7 <= res <= 10:
                    attempt_result_msg += get_bot_messages('result_0710_message')
                elif 11 <= res <= 13:
                    attempt_result_msg += get_bot_messages('result_1113_message')
                elif 14 <= res <= 16:
                    attempt_result_msg += get_bot_messages('result_1416_message')

                write_msg(user_id, attempt_result_msg, get_default_keyboard())


            else:
                pass

if __name__ == '__main__':
    db = grammar.DB()

    session = vk_connect()
    chat_listen(session)