import psycopg2
from psycopg2 import Error, errors
import os
import json

class WordSet:

    def __init__(self):
        self.set_name = self.choose_word_set_name()
        self.set_status = self.choose_set_status()
        self.set_file_name = self.choose_word_set_to_add()

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

    def create(self):
        with open('/Users/iggnatov/Documents/dev/grammar_bot/sql_setting_files/config_file.txt', 'r') as json_file:
            j_data = json.load(json_file)

        try:
            connection = psycopg2.connect(user=j_data['user'], password=j_data['password'],
                                          host=j_data['host'], port='5433', database=j_data['dbname'])
            cursor = connection.cursor()
            # print(connection.get_dsn_parameters(), "\n")
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You\'re connected to - ", record, "\n")

            cursor.execute(f"""INSERT INTO word_sets (set_file_name, set_status, set_name) 
                            VALUES ('{self.set_file_name}', '{self.set_status}', '{self.set_name}');""")
            # record = cursor.fetchone()
            print(record)
            connection.commit()

            cursor.execute(f"""SELECT id FROM word_sets 
                            WHERE set_file_name = '{self.set_file_name}';""")
            record_id = cursor.fetchone()
            print('record_id: ', record_id[0])


            f = open('/Users/iggnatov/Documents/dev/grammar_bot/word_sets/' + self.set_file_name, 'r')
            print(f"File \'{self.set_file_name}\' opened")

            try:
                # making a word
                word_list = f.readlines()
                word_list = [s_word.strip() for s_word in word_list]
                print('Word_list has been read')
                i = 0
                for each_word in word_list[0:]:
                    i += 1
                    print(f"Taking the {i}-element - {each_word}")
                    # making a word
                    word_without_brackets = each_word.replace('[', '').replace(']', '')
                    gap_index = each_word.index('[')
                    word_command = f"""INSERT INTO words (word, gap_index) 
                            VALUES ('{word_without_brackets}', {gap_index});"""
                    print(f"Command to be used:\n{word_command}")

                    cursor.execute(word_command)
                    print(cursor)
                    connection.commit()
                    print('Connection committed')

                    # making a relation between word and set
                    # ...
                    cursor.execute(f"""SELECT id FROM words
                    WHERE word = '{word_without_brackets}';""")
                    word_id = cursor.fetchone()
                    print('word_id: ', word_id[0])

                    relation_command = f"""INSERT INTO rel_words_sets (word_id, set_id) 
                    VALUES ({word_id[0]}, {record_id[0]});"""
                    print(f"Command to be used:\n{relation_command}")

                    cursor.execute(relation_command)
                    print(cursor)
                    connection.commit()
                    print('Connection committed')

                print(i, " lines were successfully added")



            finally:
                print(f"File {self.set_file_name} closed")
                f.close()

        except psycopg2.errors.UniqueViolation:
            print("""Value is already exist.\n
            Check up input values""")

        except (Exception, Error) as error:
            print("Error working with PostgreSQL", error)

        finally:
            # print('finally')
            # if connection:
            cursor.close()
            connection.close()
            print("Connection to PostgreSQL closed")




