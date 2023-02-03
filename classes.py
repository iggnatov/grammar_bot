class WordSet:

    def __init__(self, set_name):
        self.set_name = set_name

    def create (self):
        file_name = input('Type the file name of the set. Don\'t forget to type \'.txt\'')
        f = open(file_name, 'r')
        try:
            word_list = f.readlines()
            word_list = [s_word.strip() for s_word in word_list]

            for each_word in word_list[0:]:

                # making a word
                word = Word(each_word, self.set_name)
                word.add_to_sql_file()

        finally:
            f.close()


class Word:
    """definition"""

    # def __init__(self, word='', gap_index=0, gap_type='', mistakes=0.00, word_sets=''):
    def __init__(self, word='', word_set=''):
        self.word = word
        self.gap_index = self.get_gap_index()
        self.gap_type = self.get_gap_type()
        self.mistakes = 0
        self.word_set = word_set

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
            gap_type = ''
        return gap_type

    def add_to_sql_file(self):
        sql_file = open('sql_setting_files/tempdata.sql', 'a')

        try:
            sql_file.write(
                f"INSERT INTO words (word, gap_index, gap_type, mistakes, word_sets) \
                VALUES ('{self.word}',{self.gap_index}, {self.gap_type}, {self.mistakes}, {self.word_set});\n"
            )

        finally:
            sql_file.close()

class User:
    """definition"""

    def __init__(self, vk_id=0, team_id=0):
        self.vk_id = vk_id
        self.team_id = team_id

#
# # check letter
#         answer = input('Type the correct letter, please! \n').strip().lower()
#         if word[gap_index] == answer:
#             print('Yes')
#         else:
#             print('No')
#  mistakes - must be a relation mistakes / uses

#
# # word_with_gap
#         word_part_1 = word[0:gap_index]
#         if (b2 - b1) > 1:
#             word_part_2 = word[gap_index + 1:]
#         else:
#             word_part_2 = word[gap_index:]
#             word_with_gap = word_part_1 + '_' + word_part_2
#             print(t_word, word, b2, b1, b2 - b1, gap_index, word_with_gap,
#                   'There is no symbol. Type @ between brackets!')
#             return 0
#
#         word_with_gap = word_part_1 + '_' + word_part_2
#         print(t_word, word, b2, b1, b2 - b1, gap_index, word_with_gap)