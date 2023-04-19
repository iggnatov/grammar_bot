from vkbottle.bot import BotLabeler, Message, rules

admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule(1250100)]

@admin_labeler.private_message(command='show')
async def show(message: Message):
    await message.answer('show')
