from vkbottle.bot import BotLabeler

labeler = BotLabeler()

@labeler.private_message(text='ping')
async def ping_handler(message):
    await message.answer('pong')
