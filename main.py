import admin_functions as af
import psycopg2

class Word:
    """definition"""

    def __init__(self, word, gap_index, mistakes=0):
        self.word = word
        self.gap_index = gap_index
        self.mistakes = mistakes

    def create(self, word_list):
        """

        :param word_list:
        :return:
        """



if __name__ == '__main__':
    my_word = Word('test_word', 2)
    print(my_word.word, my_word.gap_index, my_word.mistakes)


    # pass
    # create a sql_file from text file
    # file_name = 'word_sets/test_words.txt'
    # af.get_word_list(file_name)
