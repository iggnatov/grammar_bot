import admin_functions as af
import psycopg2
from contextlib import closing
from psycopg2 import Error
import json




if __name__ == '__main__':
    #
    # my_word = Word('test_word', 2)
    # print(my_word.word, my_word.gap_index, my_word.mistakes)



    # get database configs: dbname, user, password, host
    with open('sql_setting_files/config_file.txt', 'r') as json_file:
        j_data = json.load(json_file)
        # print(data['dbname'])
        # for elem in data:
        #     # print(type(data), elem, '-', data[elem])
    connection = ''
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
        print(connection)
        cursor = connection.cursor()
        # Распечатать сведения о PostgreSQL
        print("Информация о сервере PostgreSQL")
        print(connection.get_dsn_parameters(), "\n")
        # Выполнение SQL-запроса
        cursor.execute("SELECT version();")
        # Получить результат
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")

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
