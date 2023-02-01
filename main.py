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
#     f = open('words.txt', 'r')
#     try:
#         word_list = f.readlines()
#         word_list = [word.strip() for word in word_list]
#         list_name = word_list[0]
#         print(list_name)
#         print(word_list[1:2])
#     finally:
#         f.close()

def test(test_word):
    try:
        b1 = test_word.index('[')
        b2 = test_word.index(']')

        # get word without brackets
        word = test_word.replace('[', '')
        word = word.replace(']', '')

        print(test_word, word, b2, b1, b2-b1)
    except ValueError:
        print(test_word, '- no brackets')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # get_word_list()
    test_words = ['б[а]гаж', 'бил[]ет', 'баллон']
    for test_word in test_words:
        test(test_word)
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
