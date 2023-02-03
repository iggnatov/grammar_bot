import admin_functions as af
import psycopg2
# from contextlib import closing
from psycopg2 import Error
import json

class WordSet:

    def __init__(self, set_name):
        self.set_name = set_name

    def create (self):
        file_name = input('Type the full file name of the set (including the path). Don\'t forget to type \'.txt\'\n')
        file_name = '/home/admin/grammar_bot/word_sets/test_words_1.txt'
        f = open(file_name, 'r')
        # print(f"file {file_name} has been opened")
        print('test_words_1.txt has been opened')
        try:
            word_list = f.readlines()
            word_list = [s_word.strip() for s_word in word_list]
            print('word_list has been read')
            for each_word in word_list[0:]:
                print(f"taking the {each_word}")
                # making a word
                word = Word(each_word, self.set_name)
                # word.add_to_sql_file()
                command = word.get_word_full_command()
                print(f"Command {command} has been got")
                cursor.execute(command)
                print(cursor)
                connection.commit()
                print('connection comitted')
                count = cursor.rowcount
                print(count, "Запись успешно добавлена в таблицу")

        finally:
            f.close()


class Word:
    """definition"""

    # def __init__(self, word='', gap_index=0, gap_type='', mistakes=0.00, word_sets=''):
    def __init__(self, word='', word_set_name=''):
        self.word = word
        self.gap_index = self.get_gap_index()
        self.gap_type = self.get_gap_type()
        self.mistakes = 0
        self.word_set = '{' + word_set_name + '}'
        print(f"New word object {self.word} has been initialised \n"
              f"word :      {self.word}         \n"
              f"gap_index : {self.gap_index}    \n"
              f"gap_type :  {self.gap_type}     \n"
              f"mistakes :  {self.mistakes}     \n"
              f"word_set :  {self.word_set}"
              )

    def get_gap_index(self):
        gap_index = self.word.index('[')
        return gap_index

    def get_word_without_brackets(self):
        word_without_brackets = self.word.replace('[', '').replace(']', '')
        return word_without_brackets

    def get_gap_type(self):
        if self.word.index(']') - self.word.index('[') == 1:
            gap_type = 'no_gap'
        else:
            gap_type = 'gap'
        return gap_type

    def get_word_full_command(self):
        print('starting to get word full command...')
        return f"""INSERT INTO words (word, gap_index, gap_type, mistakes, word_sets) 
        VALUES ('{self.word}', {self.gap_index}, '{self.gap_type}', {self.mistakes}, '{self.word_set}');\n"""

    # def add_to_sql_file(self):
    #     sql_file = open('sql_setting_files/tempdata.sql', 'a')
    #
    #     try:
    #         sql_file.write(
    #             f"INSERT INTO words (word, gap_index, gap_type, mistakes, word_sets) \
    #             VALUES ('{self.word}',{self.gap_index}, {self.gap_type}, {self.mistakes}, {self.word_set});\n"
    #         )
    #
    #     finally:
    #         sql_file.close()


if __name__ == '__main__':
    #
    # my_word = Word('test_word', 2)
    # print(my_word.word, my_word.gap_index, my_word.mistakes)

    # while True:
    #     us = input('My small menu: type \'connection\' or \'q\' \n')
    #     if us == 'connection':
    #         continue
    #     elif us == 'q':
    #         break
    #     else:
    #         continue



    # get database configs: dbname, user, password, host
    with open('/home/admin/grammar_bot/sql_setting_files/config_file.txt', 'r') as json_file:
        j_data = json.load(json_file)
        # print(data['dbname'])
        # for elem in data:
        #     # print(type(data), elem, '-', data[elem])

    # connection = ''
    # connect to db
    try:
        # with closing(psycopg2.connect(dbname=data['dbname'], user=data['user'],
        #                     password=data['password'], host=data['host'])) as connection:
        #     with connection.cursor() as cursor:
        #         print('Ok')
        #
        #         pass
        connection = psycopg2.connect(user=j_data['user'],password=j_data['password'],
                                      host=j_data['host'], port='5432', database=j_data['dbname'])

        cursor = connection.cursor()
        # Распечатать сведения о PostgreSQL
        print("Информация о сервере PostgreSQL")
        print(connection.get_dsn_parameters(), "\n")
        # Выполнение SQL-запроса
        cursor.execute("SELECT version();")
        # Получить результат
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")

        while True:
            us = input('Menu: \n'
                       'Type \'A\' to add a word_set \n'
                       'Type \'Q\' to quit \n')
            if us == 'A':
                input_name = input('...adding a new word_set \n Type the set_name, please! \n')
                word_set = WordSet(input_name)
                word_set.create()



            elif us == 'Q':
                break
            else:
                continue




    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        # print('finally')
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

    # pass
    # create a sql_file from text file
    # file_name = 'word_sets/test_words.txt'
    # af.get_word_list(file_name)
