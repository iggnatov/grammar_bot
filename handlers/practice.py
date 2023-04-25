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


    # Обработка слова из БД для Тренировки

    # Вспомогательная функция для обработки слов
    @staticmethod
    def erase_letters(word, index):
        correct_letter = word[index]
        word_with_gap = word[:index] + '_' + word[index + 1:]
        return word_with_gap, correct_letter.lower()

    # Формирования списка Тапплов (of tupples)
    # Структура - [('АБСОЛЮТИЗМ', 3), ('АРАПНИК', 0)]
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



    # Получение и запись общего счета тренировки (practice_score)
    def get_practice_score(self):
        print(self.wrong_answers)
        return 16 - len(self.wrong_answers)