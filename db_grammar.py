import os
import json
import psycopg2
from psycopg2 import Error

class DB:
    # --- Подключение к базе данных --- #
    # Установление соединения
    @staticmethod
    def get_connection():
        # getting connection configs
        # global conn, cur
        config_path = '/Users/iggnatov/Documents/dev/grammar_bot/sql_setting_files/config_file.txt'
        with open(config_path, 'r') as json_file:
            j_data = json.load(json_file)

        # connecting to database
        try:
            conn = psycopg2.connect(user=j_data['user'], password=j_data['password'],
                                    host=j_data['host'], port='5433', database=j_data['dbname'])
            cur = conn.cursor()

            cur.execute("SELECT version();")
            record = cur.fetchone()
            print("You\'re connected to - ", record, "\n")



        except (Exception, Error) as error:
            print("Error working with PostgreSQL", error)

        finally:
            print('Finally, connection is stable')
            return conn, cur


    # Разрыв соединения
    @staticmethod
    def close_connection(cu, co):
        cu.close()
        co.close()
        print("Connection to PostgreSQL closed.")


    # --- Администрирование наборов слов --- #

    # Выбор наименования файла (темы набора для отображения пользователю)
    @staticmethod
    def choose_word_set_name():
        # add verify for rus letters and digits
        set_name = input('Type the name of the word set, that will be displayed for user:\n')
        return set_name

    # Выбор статуса добавляемого набор
    @staticmethod
    def choose_set_status():
        # add verify on or off
        set_status = input('Choose the status of your set:\n'
                           'Type \'1\' - to set ACTIVE status\n'
                           'Type \'2\' - to turn your set off - INACTIVE status\n')
        return 'ACTIVE' if set_status == '1' else 'INACTIVE'

    # Выбор файла для добавления набора слов
    @staticmethod
    def choose_word_set_to_add():
        # The path for listing items
        path = '/Users/iggnatov/Documents/dev/grammar_bot/word_sets'

        # The list of items
        files = os.listdir(path)

        print('Choose (Type) the file with words to add:')

        # Loop to print each filename separately
        for filename in files:
            print(filename)

        set_file_name = input()
        return set_file_name

    # Вывод имеющихся наборов слов
    def show_word_set(self):
        print(2)
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        # printing existing word sets
        print('All word_sets:')
        cursor.execute(f"""SELECT * FROM word_sets;""")
        word_sets = cursor.fetchall()
        i = 0
        for each_word_set in word_sets:
            i += 1
            print(each_word_set[1])

        self.close_connection(cursor, connection)
        print(f"{i} word_sets were shown")


    # Вывод слов в наборе
    def show_words_in_set_to_add(self):
        pass

    # Вывод слов в добавляемом наборе
    def show_words_in_set(self):
        pass

    # Добавление набора слов
    def create_word_set(self):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        set_file_name = self.choose_word_set_to_add()
        set_status = self.choose_set_status()
        set_name = self.choose_word_set_name()

        # adding word_set to database
        cursor.execute(f"""INSERT INTO word_sets (set_file_name, set_status, set_name) 
                        VALUES (
                        '{set_file_name}', 
                        '{set_status}', 
                        '{set_name}');""")
        connection.commit()

        # getting data from database
        cursor.execute(f"""SELECT id FROM word_sets 
                        WHERE set_file_name = '{set_file_name}';""")
        record_id = cursor.fetchone()

        # working with file
        with open('/Users/iggnatov/Documents/dev/grammar_bot/word_sets/' + set_file_name, 'r') as f:
            print(f"File \'{set_file_name}\' opened")

            # reading words from file
            word_list = f.readlines()
            word_list = [s_word.strip() for s_word in word_list]

            i = 0
            for each_word in word_list[0:]:
                # making a word
                word_without_brackets = each_word.replace('[', '').replace(']', '')
                gap_index = each_word.index('[')

                cursor.execute(f"""SELECT * FROM words WHERE word = '{word_without_brackets}'""")
                quantity_of_words = len(cursor.fetchall())
                # print(quantity_of_words)

                if quantity_of_words != 0:
                    # getting id of existing word
                    cursor.execute(f"""SELECT id FROM words
                                    WHERE word = '{word_without_brackets}';""")
                    word_id = cursor.fetchone()
                    # making only a relation between word and set
                    cursor.execute(f"""INSERT INTO rel_words_sets (word_id, set_id) 
                                    VALUES ({word_id[0]}, {record_id[0]});""")
                    connection.commit()


                else:
                    # adding word
                    i += 1
                    cursor.execute(f"""INSERT INTO words (word, gap_index) 
                                    VALUES ('{word_without_brackets}', {gap_index});""")
                    connection.commit()

                    # getting id of added word
                    cursor.execute(f"""SELECT id FROM words
                                    WHERE word = '{word_without_brackets}';""")
                    word_id = cursor.fetchone()

                    # making a relation between word and set
                    cursor.execute(f"""INSERT INTO rel_words_sets (word_id, set_id) 
                                    VALUES ({word_id[0]}, {record_id[0]});""")
                    connection.commit()

        self.close_connection(cursor, connection)
        print(i, ' words were added to database.')



    # Удаление набора слов
    def remove_word_set(self):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        # printing existing word sets
        print('All word_sets:')
        cursor.execute(f"""SELECT * FROM word_sets;""")
        word_sets = cursor.fetchall()
        for each_word_set in word_sets:
            print(each_word_set[1])

        # SELECT * FROM word_sets WHERE set_name = 'T';
        # id | set_name | set_status | set_file_name

        # input word set to remove
        word_set_to_remove = input('Type a word_set to remove from database\n')

        # set id is
        # SELECT id FROM word_sets WHERE set_name = 'T';
        cursor.execute(f"""SELECT id FROM word_sets WHERE set_name = '{word_set_to_remove}';""")
        word_set_id = cursor.fetchone()[0]

        # выгрузить все слова из этого набора слов
        # SELECT * FROM rel_words_sets WHERE set_id = 24;
        # или
        # выгрузить id всех слов этого наора слов
        # SELECT words.id FROM words
        # JOIN rel_words_sets
        # ON words.id = rel_words_sets.word_id
        # AND rel_words_sets.set_id = 24;
        cursor.execute(f"""SELECT words.id FROM words 
        JOIN rel_words_sets
        ON words.id = rel_words_sets.word_id
        AND rel_words_sets.set_id = {word_set_id};""")
        words_id = []
        words_ids = cursor.fetchall()
        for each_id in words_ids:
            words_id.append(each_id[0])
        print(words_id)

        # для каждого слова (words.id)
        i = 0
        for each_word_id in words_id:

            cursor.execute(f"""SELECT set_id FROM rel_words_sets WHERE word_id = {each_word_id};""")
            quantity_of_sets = len(cursor.fetchall())

            # если слово соержится в 1 наборе
            # SELECT set_id FROM rel_words_sets WHERE word_id = 78;
            if quantity_of_sets == 1:
                i += 1
                print(i)
                # - удалить отношение из таблицы отношений
                # DELETE FROM rel_words_sets WHERE word_id = 77;
                cursor.execute(f"""DELETE FROM rel_words_sets WHERE word_id = {each_word_id};""")
                connection.commit()
                # - b удалить слово из таблицы слова
                # DELETE FROM words WHERE words.id = 77;
                cursor.execute(f"""DELETE FROM words WHERE words.id = {each_word_id};""")
                connection.commit()

            # если слово содержится в 2 наборах
            else:
                print(0)
                # - то удалить только соотношение в таблице отношений
                # DELETE FROM rel_words_sets WHERE word_id = 78 AND set_id = 24;
                cursor.execute(f"""DELETE FROM rel_words_sets 
                WHERE word_id = {each_word_id} AND set_id = {word_set_id};""")
                connection.commit()

        # удалить набор слов из таблицы наборов слов
        # DELETE FROM word_sets WHERE set_name = 'X';
        cursor.execute(f"""DELETE FROM word_sets WHERE word_sets.id = {word_set_id};""")
        connection.commit()
        self.close_connection(cursor, connection)
        print('Word_set deleted successfully.')
        print(i, ' words were removed.')


    # Смена статуса набора слов
    def change_word_set_status(self):
        pass


    # --- Работа с тренировками --- #

    # Запись user_id

    # Запись user_nick
    # Проверка на уже записанный ник

    # Вывод активных наборов / тем
    def get_active_topic_list_from_db(self):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        cursor.execute(f"""SELECT set_name FROM word_sets WHERE set_status = 'ACTIVE';""")

        db_topic_list = cursor.fetchall()

        topic_list = []
        for each_topic in db_topic_list:
            topic = each_topic[0]
            topic_list.append(topic)

        print('List of active word_sets was executed.')
        self.close_connection(cursor, connection)
        return topic_list

    # Вывод набора слов по указанной теме
    def get_words_from_set(self, set_name):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        cursor.execute(f"""SELECT word_sets.id FROM word_sets WHERE set_name = '{set_name}';""")
        word_set_id = cursor.fetchone()[0]

        # get words
        cursor.execute(f"""
        SELECT words.id, word, gap_index FROM words
        JOIN rel_words_sets
        ON words.id = rel_words_sets.id
        AND rel_words_sets.set_id = {word_set_id};""")

        word_list = cursor.fetchall()

        self.close_connection(cursor, connection)
        # word_dict = {}
        # for elem in word_list:
        #     word_dict[elem[0]] = elem[1]
        # print('Word_dict was returned.')
        print(f'Word_list \'{set_name}\' was returned.')
        return word_list

    # Запись результатов тренировки

    # Запись в таблицу ошибки (word_id / train_id / user_id


    # --- Функции администратора --- #
    # --- Функции пользователя --- #


class WordSet:

    # def __init__(self):
    #     print('Object created')
        # self.set_name = self.choose_word_set_name()
        # self.set_status = self.choose_set_status()
        # self.set_file_name = self.choose_word_set_to_add()

    @staticmethod
    def choose_word_set_name():
        # add verify for rus letters and digits
        set_name = input('Type the name of the word set, that will be displayed for user:\n')
        return set_name

    @staticmethod
    def choose_set_status():
        # add verify on or off
        set_status = input('Choose the status of your set:\n'
                           'Type \'1\' - to set ACTIVE status\n'
                           'Type \'2\' - to turn your set off - INACTIVE status\n')
        return 'ACTIVE' if set_status == '1' else 'INACTIVE'

    @staticmethod
    def choose_word_set_to_add():
        # The path for listing items
        path = '/Users/iggnatov/Documents/dev/grammar_bot/word_sets'

        # The list of items
        files = os.listdir(path)

        print('Choose (Type) the file with words to add:')

        # Loop to print each filename separately
        for filename in files:
            print(filename)

        set_file_name = input()
        return set_file_name


    @staticmethod
    def connect():
        # getting connection configs
        config_path = '/Users/iggnatov/Documents/dev/grammar_bot/sql_setting_files/config_file.txt'
        with open(config_path, 'r') as json_file:
            j_data = json.load(json_file)

        # connecting to database
        try:
            conn = psycopg2.connect(user=j_data['user'], password=j_data['password'],
                                    host=j_data['host'], port='5433', database=j_data['dbname'])
            cur = conn.cursor()

            cur.execute("SELECT version();")
            record = cur.fetchone()
            print("You\'re connected to - ", record, "\n")

            return conn, cur

        except (Exception, Error) as error:
            print("Error working with PostgreSQL", error)

        finally:
            print('Finally block of def connect()')

    def show(self):
        db = self.connect()
        connection = db[0]
        cursor = db[1]

        # printing existing word sets
        print('All word_sets:')
        cursor.execute(f"""SELECT * FROM word_sets;""")
        word_sets = cursor.fetchall()
        i = 0
        for each_word_set in word_sets:
            i += 1
            print(each_word_set[1])
        cursor.close()
        connection.close()
        print(f"{i} word_sets were shown")
        print("Connection to PostgreSQL closed")

    def create(self):
        db = self.connect()
        connection = db[0]
        cursor = db[1]

        set_file_name = self.choose_word_set_to_add()
        set_status = self.choose_set_status()
        set_name = self.choose_word_set_name()

        # adding word_set to database
        cursor.execute(f"""INSERT INTO word_sets (set_file_name, set_status, set_name) 
                        VALUES (
                        '{set_file_name}', 
                        '{set_status}', 
                        '{set_name}');""")
        connection.commit()

        # getting data from database
        cursor.execute(f"""SELECT id FROM word_sets 
                        WHERE set_file_name = '{set_file_name}';""")
        record_id = cursor.fetchone()

        # working with file
        with open('/Users/iggnatov/Documents/dev/grammar_bot/word_sets/' + set_file_name, 'r') as f:
            print(f"File \'{set_file_name}\' opened")

            # reading words from file
            word_list = f.readlines()
            word_list = [s_word.strip() for s_word in word_list]

            i = 0
            for each_word in word_list[0:]:
                # making a word
                word_without_brackets = each_word.replace('[', '').replace(']', '')
                gap_index = each_word.index('[')

                cursor.execute(f"""SELECT * FROM words WHERE word = '{word_without_brackets}'""")
                quantity_of_words = len(cursor.fetchall())
                # print(quantity_of_words)

                if quantity_of_words != 0:
                    # getting id of existing word
                    cursor.execute(f"""SELECT id FROM words
                                    WHERE word = '{word_without_brackets}';""")
                    word_id = cursor.fetchone()
                    # making only a relation between word and set
                    cursor.execute(f"""INSERT INTO rel_words_sets (word_id, set_id) 
                                    VALUES ({word_id[0]}, {record_id[0]});""")
                    connection.commit()


                else:
                    # adding word
                    i += 1
                    cursor.execute(f"""INSERT INTO words (word, gap_index) 
                                    VALUES ('{word_without_brackets}', {gap_index});""")
                    connection.commit()

                    # getting id of added word
                    cursor.execute(f"""SELECT id FROM words
                                    WHERE word = '{word_without_brackets}';""")
                    word_id = cursor.fetchone()

                    # making a relation between word and set
                    cursor.execute(f"""INSERT INTO rel_words_sets (word_id, set_id) 
                                    VALUES ({word_id[0]}, {record_id[0]});""")
                    connection.commit()

        print(i, ' words were added to database')
        cursor.close()
        connection.close()
        print("Connection to PostgreSQL closed")

    def remove(self):
        db = self.connect()
        connection = db[0]
        cursor = db[1]

        # printing existing word sets
        print('All word_sets:')
        cursor.execute(f"""SELECT * FROM word_sets;""")
        word_sets = cursor.fetchall()
        for each_word_set in word_sets:
            print(each_word_set[1])

        # SELECT * FROM word_sets WHERE set_name = 'T';
        # id | set_name | set_status | set_file_name

        # input word set to remove
        word_set_to_remove = input('Type a word_set to remove from database\n')

        # set id is
        # SELECT id FROM word_sets WHERE set_name = 'T';
        cursor.execute(f"""SELECT id FROM word_sets WHERE set_name = '{word_set_to_remove}';""")
        word_set_id = cursor.fetchone()[0]

        # выгрузить все слова из этого набора слов
        # SELECT * FROM rel_words_sets WHERE set_id = 24;
        # или
        # выгрузить id всех слов этого наора слов
        # SELECT words.id FROM words
        # JOIN rel_words_sets
        # ON words.id = rel_words_sets.word_id
        # AND rel_words_sets.set_id = 24;
        cursor.execute(f"""SELECT words.id FROM words 
        JOIN rel_words_sets
        ON words.id = rel_words_sets.word_id
        AND rel_words_sets.set_id = {word_set_id};""")
        words_id = []
        words_ids = cursor.fetchall()
        for each_id in words_ids:
            words_id.append(each_id[0])
        print(words_id)

        # для каждого слова (words.id)
        i = 0
        for each_word_id in words_id:

            cursor.execute(f"""SELECT set_id FROM rel_words_sets WHERE word_id = {each_word_id};""")
            quantity_of_sets = len(cursor.fetchall())

            # если слово соержится в 1 наборе
            # SELECT set_id FROM rel_words_sets WHERE word_id = 78;
            if quantity_of_sets == 1:
                i += 1
                print(i)
                # - удалить отношение из таблицы отношений
                # DELETE FROM rel_words_sets WHERE word_id = 77;
                cursor.execute(f"""DELETE FROM rel_words_sets WHERE word_id = {each_word_id};""")
                connection.commit()
                # - b удалить слово из таблицы слова
                # DELETE FROM words WHERE words.id = 77;
                cursor.execute(f"""DELETE FROM words WHERE words.id = {each_word_id};""")
                connection.commit()

            # если слово содержится в 2 наборах
            else:
                print(0)
                # - то удалить только соотношение в таблице отношений
                # DELETE FROM rel_words_sets WHERE word_id = 78 AND set_id = 24;
                cursor.execute(f"""DELETE FROM rel_words_sets 
                WHERE word_id = {each_word_id} AND set_id = {word_set_id};""")
                connection.commit()

        # удалить набор слов из таблицы наборов слов
        # DELETE FROM word_sets WHERE set_name = 'X';
        cursor.execute(f"""DELETE FROM word_sets WHERE word_sets.id = {word_set_id};""")
        connection.commit()
        print('Word_set deleted successfully')
        print(i, ' words were removed')
        cursor.close()
        connection.close()
        print("Connection to PostgreSQL closed")

