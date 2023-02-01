def get_word_list(file_name):
    f = open(file_name, 'r')
    try:
        word_list = f.readlines()
        word_list = [s_word.strip() for s_word in word_list]
        list_name = word_list[0]

        sql_file = open(word_list[0], 'a')
        try:
            for start_word in word_list[1:]:
                # making a word
                try:
                    # gap_index
                    gap_index = start_word.index('[')

                    # get word without brackets
                    word = start_word.replace('[', '').replace(']', '')

                    # adding a word to the sql_file
                    sql_file.write(
                        f"INSERT INTO words (word, gap_index, mistakes) VALUES ({word}, {gap_index}, 0);"
                    )

                except ValueError:
                    print('Attention! Somewhere there is no brackets! Please, fix it out!')

        finally:
            sql_file.close()

    finally:
        f.close()
