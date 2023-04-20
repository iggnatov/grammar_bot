import time
from vkbottle.bot import Bot, BotLabeler, Message, rules

from generate_keyboard import KEYBOARD_DEFAULT, KEYBOARD_TOPICS, KEYBOARD_START_PRACTICE

labeler = BotLabeler()

class Practice:
    words_from_db = [] # структура - [('АБСОЛЮТИЗМ', 3), ('АРАПНИК', 0)]
    words_to_practise = []
    wrong_answers = []
    practice_score = 0
    practice_time_start = 0
    practice_time_finish = 0

    def __init__(self):
        self.wrong_answers = []

    # Подсчет времени тренировки
    def start_timer(self):
        self.practice_time_start = time.perf_counter()


    def stop_timer(self):
        self.practice_time_finish = time.perf_counter()


    def get_practice_time(self):
        return round(self.practice_time_finish - self.practice_time_start, 2)


    # Обработка слова из БД для Тренировки

    # Вспомогательная функция для обработки слов
    @staticmethod
    def erase_letters(word, index):
        correct_letter = word[index]
        word_with_gap = word[:index] + '_' + word[index + 1:]
        return word_with_gap, correct_letter.lower()

    # Формирования списка Тапплов (of tupples)
    # Структура - [('АБСОЛЮТИЗМ', 3), ('АРАПНИК', 0)]
    def make_words_to_practise(self):
        self.words_to_practise = []
        for elem in self.words_from_db:
            my_tuple = (elem[0], self.erase_letters(elem[1], elem[2])[0], self.erase_letters(elem[1], elem[2])[1])
            self.words_to_practise.append(my_tuple)


    # Проверка ответа и запись неверного ответа в список wrong_answers
    def check_answer(self, user_id, word_index, answer_letter):
        if answer_letter.lower() != self.words_to_practise[word_index][2]:
            my_tuple = (self.words_to_practise[word_index][0], user_id, answer_letter)
            self.wrong_answers.append(my_tuple)


    # Получение и запись общего счета тренировки (practice_score)
    def get_practice_score(self):
        print(self.wrong_answers)
        return 16 - len(self.wrong_answers)