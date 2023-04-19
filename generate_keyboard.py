from vkbottle import Keyboard, KeyboardButtonColor, Text
from db_grammar import DB


# Клавиатура по умолчанию
KEYBOARD_DEFAULT = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Правила", {"cmd": "rules"}))
    .add(Text("Тренировка", {"cmd": "practice"}))
    .get_json()
)

# Клавиатура начала тренировки
KEYBOARD_START_PRACTICE = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Старт", {"cmd": "start_practice"}))
    .add(Text("Назад", {"cmd": "back_to_start"}))
    .get_json()
)

# Получаем клавиатуру, состоящую из тем, имеющих статус ACTIVE
db = DB()
topic_list = db.get_topic_list_from_db()
def get_topic_keyboard(t_list, key_board):
    btn_in_row = 0
    for btn in t_list:
        if btn_in_row < 2:
            key_board.add(Text(str(btn)))
            btn_in_row += 1
        else:
            key_board.row()
            key_board.add(Text(str(btn)))
            btn_in_row = 1

    return key_board

KEYBOARD_TOPICS = get_topic_keyboard(topic_list, Keyboard(one_time=False, inline=True))


