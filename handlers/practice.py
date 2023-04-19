from vkbottle.bot import BotLabeler, Message, rules
from generate_keyboard import KEYBOARD_TOPICS, KEYBOARD_DEFAULT

labeler = BotLabeler()

@labeler.private_message(text='Правила')
async def ping_handler(message):
    await message.answer('Правила', keyboard=KEYBOARD_DEFAULT)

@labeler.private_message(text='Тренировка')
async def ping_handler(message):
    await message.answer('Тренировка', keyboard=KEYBOARD_TOPICS)


