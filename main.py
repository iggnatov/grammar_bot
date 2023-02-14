import grammar

if __name__ == '__main__':
    while True:
        us = input('Menu: \n'
                    'Type \'A\' to create a word_set \n'
                    'Type \'R\' to remove a word set\n'
                    'Type \'Q\' to quit \n')

        if us == 'A':
            word_set = grammar.WordSet()
            word_set.create()

        elif us == 'R':
            print('Removing a word set\n')
            word_set = grammar.WordSet()
            word_set.remove()

        elif us == 'Q':
            break

        else:
            continue
