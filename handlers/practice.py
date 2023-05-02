import time
from vkbottle.bot import Bot, BotLabeler, Message, rules

# from generate_keyboard import KEYBOARD_DEFAULT, KEYBOARD_TOPICS, KEYBOARD_START_PRACTICE

labeler = BotLabeler()

class Practice:

    # Подсчет времени тренировки
    @staticmethod
    def start_timer():
        return time.perf_counter()

    @staticmethod
    def stop_timer():
        return time.perf_counter()


    # --- Обработка слова из БД для Тренировки --- #

    # Вспомогательная функция для обработки слов
    @staticmethod
    def erase_letters(word, index):
        correct_letter = word[index]
        word_with_gap = word[:index] + '_' + word[index + 1:]
        return word_with_gap, correct_letter.lower()

    # Формирования списка Кортежей - [('АБСОЛЮТИЗМ', 3), ('АРАПНИК', 0)]
    def make_words_to_practise(self, words_from_db):
        words_to_practice = []
        for elem in words_from_db:
            word_with_gap = self.erase_letters(elem[1], elem[2])[0]
            correct_letter = self.erase_letters(elem[1], elem[2])[1]
            my_tuple = (elem[0], word_with_gap, correct_letter)
            words_to_practice.append(my_tuple)
        return words_to_practice


    # Проверка ответа и запись неверного ответа в список wrong_answers
    @staticmethod
    def check_answer(correct_letter, answer_letter):
        if answer_letter.lower() == correct_letter:
            return 1
        else:
            return 0


    # Из списка кортежей делаем список вторых элементов каждого кортежа
    @staticmethod
    def make_topic_list(db_array):
        topic_list = []
        for elem in db_array:
            topic = elem[1]
            topic_list.append(topic)
        return topic_list

    @staticmethod
    def get_final_message(result):
        if 0 < result <= 3:
            return f"Ты завершил тренировку. Твой результат {result} из 16. У тебя всё ещё впереди. Дорогу осилит идущий. Попробуем ещё разок?"
        elif 4 <= result <= 6:
            return f"{result} из 16! Дерзай! Ты движешься в правильном направлении. Главное, не забывать о повторении. Ещё попытка?"
        elif 7 <= result <= 10:
            return f"Твой результат {result} из 16! Неплохо. Я в тебя верю. Может, ещё одну тему;)?"
        elif 11 <= result <= 13:
            return f"{result} из 16! Молодец! Осталось несколько шагов до идеала. У меня есть для тебя персональная тренировка. Готов?"
        elif 14 <= result <= 16:
            return f"{result} из 16! Так держать! В наше время такого знатока языка редко встретишь. А новую тему потянешь?"