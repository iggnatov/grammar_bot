from vkbottle.bot import BotLabeler, Message, rules
from db_grammar import DB
from vkbottle import BaseStateGroup
from config import state_dispenser
from generate_keyboard import KBoard

admins = [1250100, 52826876]
admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule(admins)]


db = DB()

class AdminMenuState(BaseStateGroup):
    ADMIN_HELP = 'admin_help'
    CHANGE_STATUS = 'change_status'
    SHOW_WORDS = 'show_words'


admin_commands = {'admin_help': ' - показать список доступных команд администратора\n',
                  'show_sets': ' - показать список всех наборов в формате: \n'
                               'id : {set_id}\n'
                               'name : {set_name}\n'
                               'status : {set_status}\n',
                  'show_active_sets': ' - показать список только активных наборов\n',
                  'change_set_status': ' - изменить статус набора слов\n',
                  'show_words': ' - показать слова в выбранном наборе слов'
                  }


@admin_labeler.private_message(command='admin_help')
async def admin_help(message: Message):
    answer = 'Список доступных команд администратора:\n\n'
    for key, value in admin_commands.items():
        answer += ('\'/' + key + '\'' + value + '\n')

    await message.answer(answer, keyboard=KBoard.KEYBOARD_ADMIN)


@admin_labeler.private_message(command='show_active_sets')
async def show_active_sets(message: Message):
    all_active_sets = db.admin_get_active_topic_array_from_db()
    answer = ''
    for elem in all_active_sets:
        answer += (f'id : {elem[0]}\n'
                   f'name : {elem[1]}\n'
                   f'status : {elem[2]}\n\n'
                   )
    await message.answer(answer, keyboard=KBoard.KEYBOARD_ADMIN)


@admin_labeler.private_message(command='show_sets')
async def show_sets(message: Message):
    all_sets = db.admin_get_active_topic_array_from_db() + db.admin_get_inactive_topic_array_from_db()
    # print(all_sets)

    answer = ''
    for elem in all_sets:
        answer += (f'id : {elem[0]}\n'
                   f'name : {elem[1]}\n'
                   f'status : {elem[2]}\n\n'
                   )

    await message.answer(answer, keyboard=KBoard.KEYBOARD_ADMIN)


@admin_labeler.private_message(command='change_set_status')
async def change_set_status(message: Message):
    await message.answer('Укажи id набора, статус которого нужно изменить.')
    await state_dispenser.set(message.peer_id, AdminMenuState.CHANGE_STATUS)


@admin_labeler.private_message(state=AdminMenuState.CHANGE_STATUS)
async def change_status(message: Message):
    set_id = message.text
    db.change_set_status(set_id)
    await message.answer(f'Готово.', keyboard=KBoard.KEYBOARD_ADMIN)
    await state_dispenser.set(message.peer_id, AdminMenuState.ADMIN_HELP)



@admin_labeler.private_message(command='show_words')
async def show_words_set(message: Message):
    await message.answer('Укажи id набора, слова которого хочешь посмотреть.')
    await state_dispenser.set(message.peer_id, AdminMenuState.SHOW_WORDS)


@admin_labeler.private_message(state=AdminMenuState.SHOW_WORDS)
async def change_status(message: Message):
    set_id = message.text
    word_list = db.get_words_from_set_id(set_id)

    answer = 'word_id : word : gap_index\n'
    for elem in word_list:
        answer += f'{elem[0]} : {elem[1]} : {elem[2]}\n'

    await message.answer(answer, keyboard=KBoard.KEYBOARD_ADMIN)
    await state_dispenser.set(message.peer_id, AdminMenuState.ADMIN_HELP)
