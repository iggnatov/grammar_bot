from db_grammar import DB

def console_admin_db():
    while True:
        us = input('Menu: \n'
                    'Type \'S\' to show all word sets\n'
                    'Type \'A\' to create a word set\n'
                    'Type \'R\' to remove a word set\n'
                    'Type \'Q\' to quit\n')

        if us == 'S':
            print(1)
            word_set.show_word_set()
        elif us == 'A':
            word_set.create_word_set()

        elif us == 'R':
            print('Removing a word set\n')
            word_set.remove_word_set()

        elif us == 'Q':
            break

        else:
            continue


if __name__ == '__main__':
    word_set = DB()
    console_admin_db()
