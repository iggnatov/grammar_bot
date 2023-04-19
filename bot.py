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
    START = 'start'
    RULES = 'rules'
    START_PRACTICE = 'start_practice'
    PRACTICE = 'practise'

class PracticeState(BaseStateGroup):
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
    Q16 = 'q16'


# Loading handlers to global labeler
for labeler in labelers:
    bot.labeler.load(labeler)


# Test handler
@labeler.private_message(text='Начать')
async def hello_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer(f'Привет, {users_info[0].first_name}!', keyboard=KEYBOARD_DEFAULT)
    await bot.state_dispenser.set(message.peer_id, MenuState.START)


@labeler.private_message(state=MenuState.START, payload={'cmd':'rules'}, text='Правила')
async def bot_rules_handler(message: Message):
    await message.answer('Правила', keyboard=KEYBOARD_DEFAULT)


@labeler.private_message(state=MenuState.START, payload={'cmd': 'practice'}, text='Тренировка')
async def practice_handler(message: Message):
    await message.answer('Начать тренировку?', keyboard=KEYBOARD_START_PRACTICE)
    await bot.state_dispenser.set(message.peer_id, MenuState.START_PRACTICE)


@labeler.private_message(state=MenuState.START_PRACTICE, payload={'cmd': 'start_practice'}, text='Старт')
async def start_practice_handler(message: Message):
    await message.answer('Выбери тему:', keyboard=KEYBOARD_TOPICS)
    await bot.state_dispenser.set(message.peer_id, MenuState.PRACTICE)


@labeler.private_message(state=MenuState.START_PRACTICE, payload={'cmd': 'back_to_start'}, text='Назад')
async def start_practice_handler(message: Message):
    await message.answer('Начнем с начала!?', keyboard=KEYBOARD_DEFAULT)
    await bot.state_dispenser.set(message.peer_id, MenuState.START)


db = DB()
topic_list = db.get_topic_list_from_db()


@labeler.private_message(state=MenuState.PRACTICE, text=topic_list)
async def start_practice_handler(message: Message):
    await message.answer(message.text + '\nТренировка началась')


@labeler.private_message(state=MenuState.PRACTICE, command='q')
async def stop_handler(message: Message):
    await message.answer('Тренировка завершена, возвращаюсь в главное меню.', keyboard=KEYBOARD_DEFAULT)
    await bot.state_dispenser.set(message.peer_id, MenuState.START)


# Running Bot
if __name__ == '__main__':
    bot.run_forever()