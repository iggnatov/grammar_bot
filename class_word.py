class Word:
    """definition"""

    # def __init__(self, word='', gap_index=0, gap_type='', mistakes=0.00, word_sets=''):
    def __init__(self, word='', word_set_name=''):
        self.word = word
        self.word_without_brackets = self.get_word_without_brackets()
        self.gap_index = self.get_gap_index()
        self.gap_type = self.get_gap_type()
        self.mistakes = 0
        self.word_set = '{' + word_set_name + '}'
        print(f"New word object {self.word} has been initialised \n"
              f"word :      {self.word}         \n"
              f"gap_index : {self.gap_index}    \n"
              f"gap_type :  {self.gap_type}     \n"
              f"mistakes :  {self.mistakes}     \n"
              f"word_set :  {self.word_set}"
              )

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
            gap_type = 'gap'
        return gap_type

    def get_word_full_command(self):
        # Если слово уже сущесвует в таблице, но набор слова указан другой
        # - то необходимо уведомить пользователя
        # и спросить пользователя о добавлении другого набора к этому слову
        #  если да - добавить набор к существующему слову
        #  если нет - пропустить слово и перейти к следующему слову
        print('starting to get word full command...')
        return f"""INSERT INTO words (word, gap_index, gap_type, mistakes, word_sets) 
        VALUES ('{self.word_without_brackets}', {self.gap_index}, '{self.gap_type}', {self.mistakes}, '{self.word_set}');\n"""