import psycopg2
from psycopg2 import Error, errors
import os
import class_word
import json


def choose_word_set_to_add():
    # The path for listing items
    path = '/home/admin/grammar_bot/word_sets/'

    # The list of items
    files = os.listdir(path)

    print('Choose (Type) the file with words to add:')

    # Loop to print each filename separately
    for filename in files:
        print(filename)

    return '/home/admin/grammar_bot/word_sets/' + input()


class WordSet:

    def __init__(self, set_name):
        self.set_name = set_name

    def create (self):
        with open('/home/admin/grammar_bot/sql_setting_files/config_file.txt', 'r') as json_file:
            j_data = json.load(json_file)

        try:
            connection = psycopg2.connect(user=j_data['user'], password=j_data['password'],
                                          host=j_data['host'], port='5432', database=j_data['dbname'])
            cursor = connection.cursor()
            # print(connection.get_dsn_parameters(), "\n")
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You\'re connected to - ", record, "\n")


            file_name = choose_word_set_to_add()
            f = open(file_name, 'r')
            print(f"File {file_name} opened")

            try:
                word_list = f.readlines()
                word_list = [s_word.strip() for s_word in word_list]
                print('Word_list has been read')
                i = 0
                for each_word in word_list[0:]:
                    i += 1
                    print(f"Taking the {i}-element - {each_word}")
                    # making a word
                    word = class_word.Word(each_word, self.set_name)

                    command = word.get_word_full_command()
                    print(f"Command to be used:\n{command}")

                    cursor.execute(command)
                    print(cursor)
                    connection.commit()
                    print('Connection committed')
                    # count = cursor.rowcount
                    print("Line was successfully added")
                print(i, " lines were successfully added")

            finally:
                f.close()

        except psycopg2.errors.UniqueViolation:
            print(f'Such a word already exists')

        except (Exception, Error) as error:
            print("???????????? ?????? ???????????? ?? PostgreSQL", error)

        finally:
            # print('finally')
            if connection:
                cursor.close()
                connection.close()
                print("Connection to PostgreSQL closed")

