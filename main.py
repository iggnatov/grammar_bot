# function get_words from file to database
# def get_correct_letter(word):
#     # try  \ finally ?
#     pass
#
#
# def get_just_word(word):
#     pass
#
#
# def get_gap_index(word):
#     pass


# def get_word_list():
#     f = open('test_words.txt', 'r')
#     try:
#         word_list = f.readlines()
#         word_list = [word.strip() for word in word_list]
#         list_name = word_list[0]
#         print(list_name)
#         print(word_list[1:2])
#     finally:
#         f.close()


def test(t_word):
    try:
        b1 = t_word.index('[')
        b2 = t_word.index(']')

        # gap_index
        gap_index = b1

        # get word without brackets
        word = t_word.replace('[', '')
        word = word.replace(']', '')

        # word_with_gap
        word_part_1 = word[0:gap_index]
        if (b2 - b1) > 1:
            word_part_2 = word[gap_index + 1:]
        else:
            word_part_2 = word[gap_index:]
            word_with_gap = word_part_1 + '_' + word_part_2
            print(t_word, word, b2, b1, b2 - b1, gap_index, word_with_gap,
                  'There is no symbol. Type @ between brackets!')
            return 0

        word_with_gap = word_part_1 + '_' + word_part_2
        print(t_word, word, b2, b1, b2 - b1, gap_index, word_with_gap)

        # check letter
        answer = input('Type the correct letter, please! \n').strip().lower()
        if word[gap_index] == answer:
            print('Yes')
        else:
            print('No')

    except ValueError:
        print(t_word, '- Attention! There is no brackets! Please, fix it out!')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    set_name = 'test_words.txt'
    # get_word_list()

    test_words = ['б[а]гаж', 'бил[]ет', 'баллон', 'береч[ь]']
    for test_word in test_words:
        test(test_word)
    pass
