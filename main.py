import admin_functions as af
import psycopg2





if __name__ == '__main__':
    my_word = Word('test_word', 2)
    print(my_word.word, my_word.gap_index, my_word.mistakes)


    # pass
    # create a sql_file from text file
    # file_name = 'word_sets/test_words.txt'
    # af.get_word_list(file_name)
