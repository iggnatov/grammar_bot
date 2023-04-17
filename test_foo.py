import json
import psycopg2
from psycopg2 import Error

def erase_letter(word, index):
    correct_letter = word[index]
    word_with_gap = word[:index] + '_' + word[index+1:]
    print(word_with_gap, correct_letter)

def check(quiz_dict):
    print(quiz_dict)
    for word, letter in quiz_dict.items():
        print(word, letter)
        erase_letter(word, letter)

def test_foo(topic_text):
    # getting connection configs
    db_config_path = '/Users/iggnatov/Documents/dev/grammar_bot/sql_setting_files/config_file.txt'
    with open(db_config_path, 'r') as db_json_file:
        db_j_data = json.load(db_json_file)

    # connecting to database
    try:
        conn = psycopg2.connect(user=db_j_data['user'], password=db_j_data['password'],
                                host=db_j_data['host'], port='5433', database=db_j_data['dbname'])
        cur = conn.cursor()

        cur.execute("SELECT version();")
        record = cur.fetchone()
        print(f'You\'re connected to - ",{record}')

    except (Exception, Error) as error:
        print("Error working with PostgreSQL", error)

    finally:
        print('Finally block of def connect()')
    # get word_sets.id / now for example it's 42 - История
    word_set_id = 42

    # get words
    cur.execute(f"""SELECT word, gap_index FROM words
            JOIN rel_words_sets
            ON words.id = rel_words_sets.id
            AND rel_words_sets.set_id = {word_set_id};""")

    word_list = cur.fetchall()
    word_dict = {}
    cur.close()
    conn.close()
    print("Connection to PostgreSQL closed\n")
    for elem in word_list:
        word_dict[elem[0]] = elem[1]

    check(word_dict)



test_foo('История')
