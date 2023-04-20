import os, sys
from typing import Union
from vkbottle.bot import Bot, Message
from vkbottle import BaseStateGroup
# from vkbottle.dispatch.rules import ABCRule
from vkbottle import GroupEventType, GroupTypes, Keyboard, Text, VKAPIError
from loguru import logger
from config import api, state_dispenser, labeler
from handlers import labelers
from generate_keyboard import KEYBOARD_DEFAULT, KEYBOARD_START_PRACTICE, KEYBOARD_TOPICS
# from handlers.practice import Practice
from db_grammar import DB
from handlers.practice import Practice

# Logging (loguru) settings
logger.remove()
logger.add(sys.stderr, level='INFO')


# Creating a bot
bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser
)

class MenuState(BaseStateGroup):
    START_MENU = 'start'
    RULES = 'rules'
    START_PRACTICE = 'start_practice'
    PRACTICE = 'practise'

class PracticeState(BaseStateGroup):
    Q0 = 'q0'
    Q1 = 'q1'
    Q2 = 'q2'
    Q3 = 'q3'
    Q4 = 'q4'
    Q5 = 'q5'
    Q6 = 'q6'
    Q7 = 'q7'
    Q8 = 'q8'
    Q9 = 'q9'
    Q10 = 'q10'
    Q11 = 'q11'
    Q12 = 'q12'
    Q13 = 'q13'
    Q14 = 'q14'
    Q15 = 'q15'
    QR = 'qr'


# Loading handlers to global labeler
for labeler in labelers:
    bot.labeler.load(labeler)


# Test handler
@labeler.private_message(text='Начать')
async def hello_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer(f'Привет, {users_info[0].first_name}!', keyboard=KEYBOARD_DEFAULT)
    await bot.state_dispenser.set(message.peer_id, MenuState.START_MENU)


@labeler.private_message(state=MenuState.START_MENU, payload={'cmd': 'rules'}, text='Правила')
async def bot_rules_handler(message: Message):
    await message.answer('Правила', keyboard=KEYBOARD_DEFAULT)


@labeler.private_message(state=MenuState.START_MENU, payload={'cmd': 'practice'}, text='Тренировка')
async def chose_topic_handler(message: Message):
    await message.answer('Выбери тему:', keyboard=KEYBOARD_TOPICS)
    await bot.state_dispenser.set(message.peer_id, MenuState.START_PRACTICE)


# Создаем класс БД и получаем список активных наборов
db = DB()
active_topic_list = db.get_active_topic_list_from_db()

# Создаем класс Тренировки
practice = Practice()

@labeler.private_message(state=MenuState.START_PRACTICE, text=active_topic_list)
async def pre_start_practice_handler(message: Message):
    await message.answer(f'Вы выбрали тему {message.text}. Начать тренировку?', keyboard=KEYBOARD_START_PRACTICE)
    practice.words_from_db = db.get_words_from_set(message.text)

@labeler.private_message(state=MenuState.START_PRACTICE, payload={'cmd': 'start_practice'}, text='Старт')
async def start_practice_handler(message: Message):
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q0)
    practice.make_words_to_practise()
    await message.answer(practice.words_to_practise[0][1])
    practice.start_timer()


@labeler.private_message(state=PracticeState.Q0)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 0, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q1)
    await message.answer(practice.words_to_practise[1][1])

@labeler.private_message(state=PracticeState.Q1)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 1, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q2)
    await message.answer(practice.words_to_practise[2][1])

@labeler.private_message(state=PracticeState.Q2)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 2, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q3)
    await message.answer(practice.words_to_practise[3][1])


@labeler.private_message(state=PracticeState.Q3)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 3, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q4)
    await message.answer(practice.words_to_practise[4][1])

@labeler.private_message(state=PracticeState.Q4)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 4, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q5)
    await message.answer(practice.words_to_practise[5][1])

@labeler.private_message(state=PracticeState.Q5)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 5, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q6)
    await message.answer(practice.words_to_practise[6][1])

@labeler.private_message(state=PracticeState.Q6)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 6, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q7)
    await message.answer(practice.words_to_practise[7][1])

@labeler.private_message(state=PracticeState.Q7)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 7, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q8)
    await message.answer(practice.words_to_practise[8][1])

@labeler.private_message(state=PracticeState.Q8)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 8, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q9)
    await message.answer(practice.words_to_practise[9][1])

@labeler.private_message(state=PracticeState.Q9)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 9, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q10)
    await message.answer(practice.words_to_practise[10][1])

@labeler.private_message(state=PracticeState.Q10)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 10, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q11)
    await message.answer(practice.words_to_practise[11][1])

@labeler.private_message(state=PracticeState.Q11)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 11, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q12)
    await message.answer(practice.words_to_practise[12][1])

@labeler.private_message(state=PracticeState.Q12)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 12, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q13)
    await message.answer(practice.words_to_practise[13][1])

@labeler.private_message(state=PracticeState.Q13)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 13, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q14)
    await message.answer(practice.words_to_practise[14][1])

@labeler.private_message(state=PracticeState.Q14)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 14, message.text)
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q15)
    await message.answer(practice.words_to_practise[15][1])

@labeler.private_message(state=PracticeState.Q15)
async def practice_handler(message: Message):
    practice.check_answer(message.peer_id, 15, message.text)
    await bot.state_dispenser.set(message.peer_id, MenuState.START_MENU)
    practice_result = practice.get_practice_score()
    practice.stop_timer()
    practice_time = practice.get_practice_time()
    await message.answer(f'Вы завершили тренировку.\nВаш результат: {practice_result} за {practice_time} секунд!')
    await stop_handler(message)


@labeler.private_message(state=MenuState.START_PRACTICE, payload={'cmd': 'back_to_start'}, text='Назад')
async def back_to_start_menu_handler(message: Message):
    await message.answer('Начнем с начала!?', keyboard=KEYBOARD_DEFAULT)
    await bot.state_dispenser.set(message.peer_id, MenuState.START_MENU)


@labeler.private_message(state=MenuState.PRACTICE, command='q')
async def stop_handler(message: Message):
    await message.answer('Тренировка завершена, возвращаюсь в главное меню.', keyboard=KEYBOARD_DEFAULT)
    await bot.state_dispenser.set(message.peer_id, MenuState.START_MENU)


# Running Bot
if __name__ == '__main__':
    bot.run_forever()