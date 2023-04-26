from vkbottle.bot import BotLabeler, Message, rules
from db_grammar import DB
from config import state_dispenser
from vkbottle import BaseStateGroup


admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule(1250100)]

db = DB()

class AdminMenuState(BaseStateGroup):
    ADMIN_HELP = 'admin_help'
    CHANGE_STATUS = 'change_status'

admin_commands = {'admin_help': ' - показать список доступных команд администратора',
                  'show': ' - show',
                  'show_sets': ' - показать список всех наборов в формате: \n'
                               'id : {set_id}\n'
                               'name : {set_name}\n'
                               'status : {set_status}\n',
                  'change_set_status': ' - изменить статус набора слов'
                  }

@admin_labeler.private_message(command='admin_help')
async def show(message: Message):
    answer = 'Список доступных команд администратора:\n'
    for key, value in admin_commands.items():

        answer += ('\'/' + key + '\'' + value + '\n')

    await message.answer(answer)


@admin_labeler.private_message(command='show')
async def show(message: Message):
    await message.answer('show')


@admin_labeler.private_message(command='show_sets')
async def show(message: Message):
    all_sets = db.admin_get_active_topic_array_from_db() + db.admin_get_inactive_topic_array_from_db()
    print(all_sets)

    answer = ''
    for elem in all_sets:
        answer += (f'id : {elem[0]}\n'
                   f'name : {elem[1]}\n'
                   f'status : {elem[2]}\n\n'
                   )

    await message.answer(answer)


@admin_labeler.private_message(command='change_set_status')
async def show(message: Message):
    await message.answer('Укажи id набора, статус которого нужно изменить.')
    await state_dispenser.set(message.peer_id, AdminMenuState.CHANGE_STATUS)


@admin_labeler.private_message(state=AdminMenuState.CHANGE_STATUS)
async def show(message: Message):
    set_id = message.text
    db.change_set_status(set_id)
    await message.answer(f'Готово.')
    await state_dispenser.set(message.peer_id, AdminMenuState.ADMIN_HELP)
