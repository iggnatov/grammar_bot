import class_wordset


if __name__ == '__main__':
    while True:
        us = input('Menu: \n'
                    'Type \'A\' to add a word_set \n'
                    'Type \'Q\' to quit \n')
        if us == 'A':
            input_name = input('...adding a new word_set \nType the set_name, please! \n')
            word_set = class_wordset.WordSet(input_name)
            word_set.create()


        elif us == 'Q':
            break
        else:
            continue
