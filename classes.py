class Word:
    """definition"""

    def __init__(self, word, gap_index, mistakes):
        self.word = word
        self.gap_index = gap_index
        self.mistakes = mistakes

    def create(self, word_list):
        """

        :param word_list:
        :return:
        """

    def update(self, mistakes):
        """

        :param mistakes:
        :return:
        """

    def delete(self):
        """

        :return:
        """

class User:
    """definition"""

    def __init__(self, vk_id, team_id):
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