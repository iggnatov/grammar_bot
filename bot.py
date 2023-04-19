import os, sys
from vkbottle.bot import Bot, Message
from vkbottle import GroupEventType, GroupTypes, Keyboard, Text, VKAPIError
from loguru import logger
from config import api, state_dispenser, labeler
from handlers import labelers
from generate_keyboard import KEYBOARD_DEFAULT

# Logging (loguru) settings
logger.remove()
logger.add(sys.stderr, level='INFO')


# Creating a bot
bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser
)


# Loading handlers to global labeler
for labeler in labelers:
    bot.labeler.load(labeler)


# Test handler
@labeler.private_message(text='Начать')
async def hello_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer(f'Привет, {users_info[0].first_name}!', keyboard=KEYBOARD_DEFAULT)


# Running Bot
bot.run_forever()