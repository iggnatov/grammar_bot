from vkbottle.bot import BotLabeler, Message, rules
from vkbottle_types.objects import MessagesConversation

chat_labeler = BotLabeler()
@chat_labeler.message(text='где я')
async def where_am_i(message: Message, chat: MessagesConversation):
    await message.answer(f'Вы в <<{chat.chat_settings.title}>>')