from vkbottle.bot import Bot, BotLabeler, Message, rules
from generate_keyboard import KEYBOARD_DEFAULT, KEYBOARD_TOPICS, KEYBOARD_START_PRACTICE

labeler = BotLabeler()









#
# class Practice:
#     def __init__(self, bot, message):
#         self.bot = bot
#         self.message = message
#
#
#     async def start_practice(self):
#         await self.message.answer('Начать тренировку?', keyboard=KEYBOARD_START_PRACTICE)
#
#
#     @labeler.private_message(text='Старт')
#     async def start_practice_handler(self, message = Message):
#         await message.answer('Тренировка', keyboard=KEYBOARD_TOPICS)
