"""This module contains utility functions and constants for the spam filter."""

SPAM_TAG = 'SPAM'
HAM_TAG = 'OK'
PREDICTION_FILE = '!prediction.txt'
TRUTH_FILE = '!truth.txt'
SYMBOLS_LIST = ['.', ',', '!', '?', ':', ';', '@', '#', '$',
               '%', '^', '&', '*', '(', ')', '-', '_', '+',
               '=', '<', '>', '[', ']', '{', '}', '|', '\\',
               '/', '~', '`', '1', '2', '3', '4', '5', '6',
                '7', '8', '9', '0', '"', "'", '№', '—', '–', '«', '»']


def read_classification_from_file(filename):
    """Reads the classification from a file and
    returns a dictionary with email names as keys and their classification as values."""
    spam_or_ham = dict()
    with open(filename, 'rt', encoding='UTF-8') as f:
        for line in f:
            temp = line.split()
            if len(temp) >= 2:
                spam_or_ham[temp[0]] = temp[1]
            else:
                return EOFError
    return spam_or_ham

def count_each_word(text) -> dict:
    words = set(text.split())
    word_dict = dict()
    for word in words:
        word_dict[word] = text.count(word)
    return word_dict

def count_spam_or_ham(truth_dict, tag) -> int:
    return len([value for value in truth_dict.values() if value == tag])

def replace_symbols(email) -> str:
    """Replaces all 'non-word' symbols in the email with an empty string."""
    for symbol in SYMBOLS_LIST:
        email = email.replace(symbol, '')
    return email
