import os, sys
from typing import Union
from vkbottle.bot import Bot, Message
from vkbottle import BaseStateGroup
# from vkbottle.dispatch.rules import ABCRule
from vkbottle import GroupEventType, GroupTypes, Keyboard, Text, VKAPIError
from loguru import logger
from config import api, state_dispenser, labeler
from handlers import labelers
from generate_keyboard import KBoard
# from handlers.practice import Practice
from db_grammar import DB
from handlers.practice import Practice
from vkbottle import CtxStorage



# Logging (loguru) settings
logger.remove()
logger.add(sys.stderr, level='INFO')

# Создаем экземпляр класса для работы БД
db = DB()

# Создаем экземпляр класса для Тренировки
practice = Practice()

# Создаем бота
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
    Q0 = 0
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4
    Q5 = 5
    Q6 = 6
    Q7 = 7
    Q8 = 8
    Q9 = 9
    Q10 = 10
    Q11 = 11
    Q12 = 12
    Q13 = 13
    Q14 = 14
    Q15 = 15
    QR = 'qr'

ctx_storage = CtxStorage()

# Loading handlers to global labeler
for labeler in labelers:
    bot.labeler.load(labeler)


# Test handler
@labeler.private_message(text='Начать')
async def hello_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer(f'Привет, {users_info[0].first_name}!', keyboard=KBoard.KEYBOARD_DEFAULT)
    await bot.state_dispenser.set(message.peer_id, MenuState.START_MENU)


@labeler.private_message(state=MenuState.START_MENU, payload={'cmd': 'rules'}, text='Правила')
async def bot_rules_handler(message: Message):
    await message.answer('Правила', keyboard=KBoard.KEYBOARD_DEFAULT)


@labeler.private_message(state=MenuState.START_MENU, payload={'cmd': 'practice'}, text='Тренировка')
async def chose_topic_handler(message: Message):
    await message.answer('Выбери тему:', keyboard=KBoard.get_topic_keyboard(db.get_active_topic_list_from_db()))
    await bot.state_dispenser.set(message.peer_id, MenuState.START_PRACTICE)


@labeler.private_message(state=MenuState.START_PRACTICE, text=db.get_active_topic_list_from_db())
async def pre_start_practice_handler(message: Message):
    await message.answer(f'Вы выбрали тему {message.text}. Начать тренировку?', keyboard=KBoard.KEYBOARD_START_PRACTICE)
    ctx_storage.set('topic', message.text)
    print('ctx topic', ctx_storage.get('topic'))


@labeler.private_message(state=MenuState.START_PRACTICE, payload={'cmd': 'start_practice'}, text='Старт')
async def start_practice_handler(message: Message):
    await bot.state_dispenser.set(message.peer_id, PracticeState.Q0)
    print('started')
    words_from_db = db.get_words_from_set(ctx_storage.get('topic'))
    print('words_from_db', words_from_db)
    practice_words = practice.make_words_to_practise(words_from_db)
    ctx_storage.set('practice_words', practice_words)
    print('ctx_storage practice_words: ', ctx_storage.get('practice_words'))


    await message.answer(ctx_storage.get('practice_words')[0][1])

    ctx_storage.set('time_start', practice.start_timer())


@labeler.private_message(state=PracticeState.Q0)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[0][0]
    correct_answer = ctx_storage.get('practice_words')[0][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = [attempt]
    ctx_storage.set('user_answers', user_answers)
    print('ctx_ practice_words', ctx_storage.get('practice_words')[0])
    print('ctx user_answers', ctx_storage.get('user_answers')[0])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q1)
    await message.answer(ctx_storage.get('practice_words')[1][1])



@labeler.private_message(state=PracticeState.Q1)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[1][0]
    correct_answer = ctx_storage.get('practice_words')[1][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[1])
    print('ctx user_answers', ctx_storage.get('user_answers')[1])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q2)
    await message.answer(ctx_storage.get('practice_words')[2][1])



@labeler.private_message(state=PracticeState.Q2)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[2][0]
    correct_answer = ctx_storage.get('practice_words')[2][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[2])
    print('ctx user_answers', ctx_storage.get('user_answers')[2])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q3)
    await message.answer(ctx_storage.get('practice_words')[3][1])


@labeler.private_message(state=PracticeState.Q3)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[3][0]
    correct_answer = ctx_storage.get('practice_words')[3][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[3])
    print('ctx user_answers', ctx_storage.get('user_answers')[3])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q4)
    await message.answer(ctx_storage.get('practice_words')[4][1])

@labeler.private_message(state=PracticeState.Q4)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[4][0]
    correct_answer = ctx_storage.get('practice_words')[4][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[4])
    print('ctx user_answers', ctx_storage.get('user_answers')[4])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q5)
    await message.answer(ctx_storage.get('practice_words')[5][1])

@labeler.private_message(state=PracticeState.Q5)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[5][0]
    correct_answer = ctx_storage.get('practice_words')[5][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[5])
    print('ctx user_answers', ctx_storage.get('user_answers')[5])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q6)
    await message.answer(ctx_storage.get('practice_words')[6][1])

@labeler.private_message(state=PracticeState.Q6)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[6][0]
    correct_answer = ctx_storage.get('practice_words')[6][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[6])
    print('ctx user_answers', ctx_storage.get('user_answers')[6])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q7)
    await message.answer(ctx_storage.get('practice_words')[7][1])

@labeler.private_message(state=PracticeState.Q7)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[7][0]
    correct_answer = ctx_storage.get('practice_words')[7][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[7])
    print('ctx user_answers', ctx_storage.get('user_answers')[7])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q8)
    await message.answer(ctx_storage.get('practice_words')[8][1])

@labeler.private_message(state=PracticeState.Q8)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[8][0]
    correct_answer = ctx_storage.get('practice_words')[8][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[8])
    print('ctx user_answers', ctx_storage.get('user_answers')[8])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q9)
    await message.answer(ctx_storage.get('practice_words')[9][1])

@labeler.private_message(state=PracticeState.Q9)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[9][0]
    correct_answer = ctx_storage.get('practice_words')[9][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[9])
    print('ctx user_answers', ctx_storage.get('user_answers')[9])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q10)
    await message.answer(ctx_storage.get('practice_words')[10][1])

@labeler.private_message(state=PracticeState.Q10)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[10][0]
    correct_answer = ctx_storage.get('practice_words')[10][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[10])
    print('ctx user_answers', ctx_storage.get('user_answers')[10])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q11)
    await message.answer(ctx_storage.get('practice_words')[11][1])

@labeler.private_message(state=PracticeState.Q11)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[11][0]
    correct_answer = ctx_storage.get('practice_words')[11][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[11])
    print('ctx user_answers', ctx_storage.get('user_answers')[11])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q12)
    await message.answer(ctx_storage.get('practice_words')[12][1])

@labeler.private_message(state=PracticeState.Q12)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[12][0]
    correct_answer = ctx_storage.get('practice_words')[12][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[12])
    print('ctx user_answers', ctx_storage.get('user_answers')[12])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q13)
    await message.answer(ctx_storage.get('practice_words')[13][1])

@labeler.private_message(state=PracticeState.Q13)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[13][0]
    correct_answer = ctx_storage.get('practice_words')[13][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[13])
    print('ctx user_answers', ctx_storage.get('user_answers')[13])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q14)
    await message.answer(ctx_storage.get('practice_words')[14][1])

@labeler.private_message(state=PracticeState.Q14)
async def practice_handler(message: Message):
    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[14][0]
    correct_answer = ctx_storage.get('practice_words')[14][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[14])
    print('ctx user_answers', ctx_storage.get('user_answers')[14])

    await bot.state_dispenser.set(message.peer_id, PracticeState.Q15)
    await message.answer(ctx_storage.get('practice_words')[15][1])

@labeler.private_message(state=PracticeState.Q15)
async def practice_handler(message: Message):
    ctx_storage.set('time_stop', practice.stop_timer())
    practice_time = round(ctx_storage.get('time_stop') - ctx_storage.get('time_start'), 2)

    user_answer = message.text
    quiz_word_id = ctx_storage.get('practice_words')[15][0]
    correct_answer = ctx_storage.get('practice_words')[15][2]
    attempt_result = practice.check_answer(correct_answer, user_answer)

    attempt = quiz_word_id, user_answer, attempt_result
    user_answers = ctx_storage.get('user_answers')
    user_answers.append(attempt)
    ctx_storage.set('user_answers', user_answers)

    print('ctx_ practice_words', ctx_storage.get('practice_words')[15])
    print('ctx user_answers', ctx_storage.get('user_answers')[15])

    practice_result = 0
    user_answers = ctx_storage.get('user_answers')
    for elem in user_answers:
        practice_result += elem[2]

    await message.answer(f'Вы завершили тренировку.\nВаш результат: {practice_result} из 16 за {practice_time} секунд!')
    await bot.state_dispenser.set(message.peer_id, MenuState.START_MENU)
    await stop_handler(message)


@labeler.private_message(state=MenuState.START_PRACTICE, payload={'cmd': 'back_to_start'}, text='Назад')
async def back_to_start_menu_handler(message: Message):
    await message.answer('Начнем с начала!?', keyboard=KBoard.KEYBOARD_DEFAULT)
    await bot.state_dispenser.set(message.peer_id, MenuState.START_MENU)


@labeler.private_message(state=MenuState.PRACTICE, command='q')
async def stop_handler(message: Message):
    await message.answer('Тренировка завершена, возвращаюсь в главное меню.', keyboard=KBoard.KEYBOARD_DEFAULT)
    await bot.state_dispenser.set(message.peer_id, MenuState.START_MENU)


# Running Bot
if __name__ == '__main__':
    bot.run_forever()