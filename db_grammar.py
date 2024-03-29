import os
import psycopg2
from psycopg2 import Error
import dotenv

dotenv.load_dotenv()


class DB:
    # --- Подключение к базе данных --- #
    # Установление соединения
    @staticmethod
    def get_connection():
        # connecting to database
        try:
            conn = psycopg2.connect(
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                host=os.environ.get("DB_HOST"),
                port=os.environ.get("DB_PORT"),
                database=os.environ.get("DB_NAME")
                )
            cur = conn.cursor()

            cur.execute("SELECT version();")
            record = cur.fetchone()
            print("You\'re connected to - ", record)
            # print('conn', conn)
            # print('cur', cur)
            return conn, cur


        except (Exception, Error) as error:
            print("Error working with PostgreSQL", error)


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
        path = '/home/grammar/grammar_bot/word_sets'

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
        # set_status = self.choose_set_status()
        set_name = self.choose_word_set_name()

        # adding word_set to database
        cursor.execute(f"""INSERT INTO word_sets (set_file_name, set_status, set_name) 
                        VALUES (
                        '{set_file_name}', 
                        'INACTIVE', 
                        '{set_name}');""")
        connection.commit()

        # getting data from database
        cursor.execute(f"""SELECT id FROM word_sets 
                        WHERE set_file_name = '{set_file_name}';""")
        record_id = cursor.fetchone()

        # working with file
        with open('/home/grammar/grammar_bot/word_sets/' + set_file_name, 'r') as f:
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
        # выгрузить id всех слов этого набора слов
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

            # если слово содержится в 1 наборе
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

                # и удалить из таблицы mistakes
                cursor.execute(f"""DELETE FROM mistakes WHERE word_id = {each_word_id};""")
                connection.commit()

            # если слово содержится в 2 наборах
            else:
                print(0)
                # - то удалить только соотношение в таблице отношений
                # DELETE FROM rel_words_sets WHERE word_id = 78 AND set_id = 24;
                cursor.execute(f"""DELETE FROM rel_words_sets 
                WHERE word_id = {each_word_id} AND set_id = {word_set_id};""")
                connection.commit()

                # и удалить из таблицы mistakes
                cursor.execute(f"""DELETE FROM mistakes WHERE word_id = {each_word_id};""")
                connection.commit()

        # Удалить из таблицы mistakes все записи с данным набором слов
        cursor.execute(f"""SELECT * FROM trains WHERE set_id = {word_set_id};""")
        temp_trains_to_delete = cursor.fetchall()

        for elem in temp_trains_to_delete:
            cursor.execute(f"""DELETE FROM mistakes WHERE train_id = {elem[0]}""")

        # Удалить все записи из таблицы Trains
        cursor.execute(f"""DELETE FROM trains WHERE set_id = {word_set_id};""")
        connection.commit()

        # удалить набор слов из таблицы наборов слов
        # DELETE FROM word_sets WHERE set_name = 'X';
        cursor.execute(f"""DELETE FROM word_sets WHERE word_sets.id = {word_set_id};""")
        connection.commit()
        self.close_connection(cursor, connection)
        print('Word_set deleted successfully.')
        print(i, ' words were removed.')





    # --- Работа с тренировками --- #

    # Запись user_id
    def add_user(self, user_id):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        try:
            cursor.execute(f"""INSERT INTO users (vk_id) VALUES ({user_id})""")
            connection.commit()
            print(f'User {user_id} was added.')

        except (Exception, Error) as error:
            print("Error working with PostgreSQL", error)

        finally:
            self.close_connection(cursor, connection)


    # Запись user_nick
    # Проверка на уже записанный ник
    def set_user_nick(self, user_nick, user_id):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        try:
            cursor.execute(f"""UPDATE users SET nick = {user_nick} WHERE vk_id = {user_id};""")
            connection.commit()
            print(f'User {user_id} was updated with user_nick {user_nick}.')

        except (Exception, Error) as error:
            print("Error working with PostgreSQL", error)

        finally:
            self.close_connection(cursor, connection)

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

        print(f'List of active word_sets was executed. {topic_list}')

        self.close_connection(cursor, connection)
        return topic_list


    def get_active_topic_array_from_db(self):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        cursor.execute(f"""SELECT word_sets.id, set_name FROM word_sets WHERE set_status = 'ACTIVE';""")

        db_active_topic_array = cursor.fetchall()

        # topic_list = []
        # for each_topic in db_topic_list:
        #     topic = each_topic[0]
        #     topic_list.append(topic)

        print(f'List of active word_sets was executed. {db_active_topic_array}')

        self.close_connection(cursor, connection)
        return db_active_topic_array

    def get_inactive_topic_array_from_db(self):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        cursor.execute(f"""SELECT word_sets.id, set_name FROM word_sets WHERE set_status = 'INACTIVE';""")

        db_inactive_topic_array = cursor.fetchall()

        # topic_list = []
        # for each_topic in db_topic_list:
        #     topic = each_topic[0]
        #     topic_list.append(topic)

        print(f'List of active word_sets was executed. {db_inactive_topic_array}')

        self.close_connection(cursor, connection)
        return db_inactive_topic_array


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
        ON words.id = rel_words_sets.word_id
        AND rel_words_sets.set_id = {word_set_id};""")

        word_list = cursor.fetchall()

        self.close_connection(cursor, connection)
        # word_dict = {}
        # for elem in word_list:
        #     word_dict[elem[0]] = elem[1]
        # print('Word_dict was returned.')
        print(f'Word_list \'{set_name}\' was returned.')
        return word_list


    def get_words_from_set_id(self, set_id):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        # get words
        cursor.execute(f"""
        SELECT words.id, word, gap_index FROM words
        JOIN rel_words_sets
        ON words.id = rel_words_sets.word_id
        AND rel_words_sets.set_id = {set_id};""")

        word_list = cursor.fetchall()

        self.close_connection(cursor, connection)
        # word_dict = {}
        # for elem in word_list:
        #     word_dict[elem[0]] = elem[1]
        # print('Word_dict was returned.')
        print(f'Word_list of set_id: {set_id} was returned.')
        return word_list


    # Получение id указанного набора слов
    def get_word_set_id(self, set_name):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]
        cursor.execute(f"""SELECT word_sets.id FROM word_sets WHERE set_name = '{set_name}';""")
        word_set_id = cursor.fetchone()[0]
        self.close_connection(cursor, connection)
        print(f'Word_set.id {word_set_id} was returned.')
        return word_set_id



    # Запись результатов тренировки и ошибок
    def add_train_results(self, set_id, user_id, practice_time, score, wrong_answers):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        # date will be added by default by PostgresQL as CURRENT_DATE
        cursor.execute(f"""INSERT INTO trains (set_id, user_id, practice_time, practice_score) 
        VALUES ('{set_id}','{user_id}','{practice_time}','{score}');""")
        connection.commit()

        cursor.execute(f"""SELECT trains.id FROM trains ORDER BY created_at  DESC LIMIT 1;""")
        last_train_id = cursor.fetchone()[0]
        print('last_train_id', last_train_id)

        # Запись в таблицу ошибки (word_id / train_id / user_id / wrong_letter
        if len(wrong_answers) > 0:
            for elem in wrong_answers:
                cursor.execute(f"""INSERT INTO mistakes (train_id, user_id, word_id, wrong_letter) 
                                VALUES ('{last_train_id}','{user_id}','{elem[0]}','{elem[1]}');""")
                connection.commit()
                print(f'Mistake was added. \n'
                      f'train_id: {last_train_id}, user_id: {user_id}, word_id: {elem[0]}, wrong_letter: {elem[1]}')

        self.close_connection(cursor, connection)
        print(f'New practice result was added. \n'
              f'set_id: {set_id}, user_id: {user_id}, time: {practice_time}, score: {score}')


    # --- Функции администратора --- #
    # Получение статуса набора слов
    def get_set_status(self, set_id):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        cursor.execute(f"""SELECT set_status FROM word_sets WHERE word_sets.id = {set_id}""")
        set_status = cursor.fetchone()[0]


        self.close_connection(cursor, connection)
        print(f'{set_status} status of the set with id = {set_id} was returned.')
        return set_status

    def admin_get_active_topic_array_from_db(self):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        cursor.execute(f"""SELECT word_sets.id, set_name, set_status FROM word_sets WHERE set_status = 'ACTIVE';""")

        db_active_topic_array = cursor.fetchall()

        # topic_list = []
        # for each_topic in db_topic_list:
        #     topic = each_topic[0]
        #     topic_list.append(topic)

        print(f'List of active word_sets was executed. {db_active_topic_array}')

        self.close_connection(cursor, connection)
        return db_active_topic_array

    def admin_get_inactive_topic_array_from_db(self):
        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        cursor.execute(f"""SELECT word_sets.id, set_name, set_status FROM word_sets WHERE set_status = 'INACTIVE';""")

        db_inactive_topic_array = cursor.fetchall()

        # topic_list = []
        # for each_topic in db_topic_list:
        #     topic = each_topic[0]
        #     topic_list.append(topic)

        print(f'List of active word_sets was executed. {db_inactive_topic_array}')

        self.close_connection(cursor, connection)
        return db_inactive_topic_array

    # Изменение статуса набора слов
    def change_set_status(self, set_id):
        actual_status = self.get_set_status(set_id)

        db = self.get_connection()
        connection = db[0]
        cursor = db[1]

        if actual_status == 'ACTIVE':
            cursor.execute(
                f"""UPDATE word_sets
                 SET set_status = 'INACTIVE' 
                 WHERE id = {set_id};""")
            connection.commit()
            print(f'Status of word_set {set_id} was changed to INACTIVE.')
        else:
            cursor.execute(
                f"""UPDATE word_sets
                SET set_status = 'ACTIVE' 
                WHERE id = {set_id};""")
            connection.commit()
            print(f'Status of word_set {set_id} was changed to ACTIVE.')

        self.close_connection(cursor, connection)

    # Изменение названия набора
    def change_set_name(self):
        pass


    # --- Функции пользователя --- #
