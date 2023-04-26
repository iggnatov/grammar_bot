from config import labeler

@labeler.private_message(text='ping')
async def ping_handler(message):
    await message.answer('pong')