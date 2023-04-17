import grammar
# import vk

if __name__ == '__main__':
    while True:
        us = input('Menu: \n'
                    'Type \'S\' to show all word sets\n'
                    'Type \'A\' to create a word set\n'
                    'Type \'R\' to remove a word set\n'
                    'Type \'Q\' to quit\n'
                    'Type \'C\' to test VK\n')

        if us == 'S':
            word_set = grammar.WordSet()
            word_set.show()

        elif us == 'A':
            word_set = grammar.WordSet()
            word_set.create()
        elif us == 'R':
            print('Removing a word set\n')
            word_set = grammar.WordSet()
            word_set.remove()
        elif us == 'C':
            # r = vk.test_foo()
            print('r')

        elif us == 'Q':
            break

        else:
            continue
