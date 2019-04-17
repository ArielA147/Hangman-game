import hangman_helper as hh

import string

VALID_LEN_USER_INPUT = 1
ALPHABET_SIZE = 26
ALPHABET_START_ASCII = 97


def making_pattern(random_word, pattern):
    """
    the function makes a pattern according to the random word in the input
    :param random_word: a string word, taken from list words
    :param pattern: a pattern of the random word, from type string
    :return: a list of the patten of the word. will contain only '_'.
    """
    for i in range(0, len(random_word)):
        pattern += '_'
    return pattern


def is_pattern_revealed(pattern, is_full_revealed):
    """
    the function check if the pattern was revealed
    :param pattern: the pattern of the random word, from type string
    :param is_full_revealed: a boolean True object that will be True if the
    pattern was revealed else, False
    :return: True if the pattern is still not revealed, else False
    """
    for i in range(0, len(pattern)):
        # checking if the pattern was not all revealed
        if pattern[i] is '_':
            is_full_revealed = False
    return is_full_revealed


def are_inputs_valid(word, pattern, letter):
    """
    the function check if word, pattern and letter are in valid types
    :param word:  a random word from word list, from type string
    :param pattern: the pattern of a random word need to be type string
    :param letter:  the letter of the user, need to by type string
    :return: True if all 3 are from type string, else False
    """
    if type(word) is str and type(pattern) is str and type(letter) is str:
        return True
    else:
        return False


def update_word_pattern(word, pattern, letter):
    """
    the function makes an updated pattern according to the word and the letter
    :param word: a random word from word list, from type string
    :param pattern: the pattern of the word , from type list
    :param letter: a letter from type char
    :return: an updated pattern that contain the letter if exist
    """
    # checking if the inputs are in the correct format
    new_pattern = ''  # the new pattern
    num_of_times_in_word = word.count(letter)  # num of shows in word
    place_in_pattern = 0
    for let in word:
        if num_of_times_in_word is not 0 and let is letter:
            new_pattern += let
            num_of_times_in_word -= 1
        elif pattern[place_in_pattern] is not '_':
            new_pattern += pattern[place_in_pattern]
        else:
            new_pattern += '_'
        place_in_pattern += 1
    return new_pattern

def filter_words_list(words_lst, pattern, wrong_guess_lst):
    """
    the function finds all the words that fit the pattern and do not contain
     wrong pattern
    :param words_lst: a list of words
    :param pattern: the pattern of the random word from type string
    :param wrong_guess_lst:list of the wrong letters that were guessed
     and do not fit the word
    :return: a list with all the words that match the pattern and not contain
    wrong letters
    """
    list_possible_words = []
    # checking if the the word is in the pattern length
    for i in range(0, len(words_lst)):
        if len(words_lst[i]) == len(pattern):
            is_word_valid = True
            for let_place in range(0, len(words_lst[i])):
                # checking if the letter was a wrong guessed
                if words_lst[i][let_place] in wrong_guess_lst:
                    is_word_valid = False
                    break
                elif words_lst[i][let_place] is not pattern[let_place] \
                        and pattern[let_place] is not '_':
                    is_word_valid = False
                    break
            if is_word_valid:
                list_possible_words.append(words_lst[i])
    return list_possible_words


def choose_letter(words_lst, pattern):
    """
    the function calculate the letter in the pattern that appears max times
     in the list words
    :param words_lst: list of words that match the pattern
    :param pattern: the pattern of the random word. from type string
    :return: the letter from the given pattern that appears max times in the
    list words
    """
    lst_letters = [0]*ALPHABET_SIZE  # histogram of english letters
    for let in pattern:  # counting how many times letter in a word
        # if the let in the pattern is _ continue to the next letter
        if let is '_':
            continue
    for i in range(0, ALPHABET_SIZE):
        alphabet_letter = string.ascii_lowercase[i]
        if alphabet_letter in pattern:  # if the letter is in the pattern
            continue
        # checking how many times the letter in the words list
        for j in range(0, len(words_lst)):
            lst_letters[i] += words_lst[j].count(alphabet_letter)
    max_value = max(lst_letters)  # the letter that shows max times in list
    place_of_max_letter = lst_letters.index(max_value)
    return chr(place_of_max_letter + ALPHABET_START_ASCII)


def is_user_won(num_wrong_guesses, random_word, pattern, wrong_guess_lst,
                msg, is_full_revealed):
    """
    the function will be updated and present a message to the user according
    to the game final status.
    :param num_wrong_guesses: number of times the user guessed wrong letter,
     from type int
    :param random_word: a random word from word list, from type string
    :param pattern: a string that shows the pattern of the random word
    :param wrong_guess_lst: a list with all the user wrong guesses
    :param msg: a message for the user. type string.
    :param is_full_revealed: a boolean object, True if the pattern was
    revealed, else False
    :return: a display state that fit to the user final status winning or
    loosing
    """
    if num_wrong_guesses == hh.MAX_ERRORS:
        msg = hh.LOSS_MSG + random_word
    elif is_pattern_revealed(pattern, is_full_revealed):
        msg = hh.WIN_MSG
    return hh.display_state(pattern, num_wrong_guesses, wrong_guess_lst, msg,
                            True)


def want_hint(words_lst, pattern, wrong_guess_lst):
    """
    the function calculate and finds possible letter
    :param words_lst: list of words that match the pattern
    :param pattern: the pattern of the word
    :param wrong_guess_lst: a list with all the user wrong guesses
    :return: a possible letter according to the pattern and the words list
    """
    possible_words_lst = filter_words_list(words_lst, pattern, wrong_guess_lst)
    possible_letter = choose_letter(possible_words_lst, pattern)
    return possible_letter


def boot_parameters(words_lst):
    """
    the function calculate and update the parameters for a single game
    :param words_lst: a list with all the words
    :return: all the updated parameters
    """
    word = hh.get_random_word(words_lst)  # choosing a random word
    pattern = making_pattern(word, '')
    is_resolved = True
    wrong_guess_lst = []
    lst_already_letter_guessed = []
    num_wrong_guesses = 0  # number of wrong guesses till now
    msg = hh.DEFAULT_MSG
    return word, pattern, is_resolved, wrong_guess_lst, num_wrong_guesses,\
           msg, lst_already_letter_guessed


def run_single_game(words_lst):
    """
    the function run a full single game with appropriate messages
    :param words_lst: a list with all the possible words
    :return: True if the user wants another game , else False
    """
    word, pattern, is_resolved, wrong_guess_lst, num_wrong_guesses, msg,\
    lst_already_letter_guessed = boot_parameters(words_lst)
    while num_wrong_guesses < hh.MAX_ERRORS and \
            not is_pattern_revealed(pattern, is_resolved):
        hh.display_state(pattern, num_wrong_guesses, wrong_guess_lst, msg)
        inp_type, inp_value = hh.get_input()
        if inp_type == hh.HINT:  # if the user want a hint
            hint = want_hint(words_lst, pattern, wrong_guess_lst)
            msg = hh.HINT_MSG + hint
        # checking if the input is length 1, and a small letter in English
        elif inp_type == hh.LETTER and inp_value.islower() \
                and len(inp_value) == VALID_LEN_USER_INPUT and \
                are_inputs_valid(word, pattern, inp_value):
            if inp_value in lst_already_letter_guessed:  # already guessed
                msg = hh.ALREADY_CHOSEN_MSG+inp_value
            else:
                # updated guessed letters
                lst_already_letter_guessed.append(inp_value)
                if inp_value in word:  # the letter is in the word
                    if update_word_pattern(word, pattern, inp_value) is not \
                            None:
                        pattern = update_word_pattern(word, pattern, inp_value)
                else:
                    wrong_guess_lst.append(inp_value)
                    num_wrong_guesses += 1
                msg = hh.DEFAULT_MSG
        else:
            msg = hh.NON_VALID_MSG
    is_user_won(num_wrong_guesses, word, pattern, wrong_guess_lst, msg,
                is_resolved)


def main():
    """
    the function start a hangman game till the user do not want to continue .
    """
    words_list = hh.load_words()  # loads words from words.txt
    continue_game = True
    # play a game till the user choose not to
    while continue_game:
        run_single_game(words_list)
        # checking if the user wants to continue playing
        continue_game = hh.get_input()[1]

if __name__ == "__main__":
    hh.start_gui_and_call_main(main)
    hh.close_gui()