from corpus import TrainingCorpus
from math import log
from utils import (
    count_spam_or_ham,
    count_each_word,
    replace_symbols,
    SPAM_TAG,
    HAM_TAG,
    PREDICTION_FILE
    )




class MyFilter:
    """MyFilter class is a spam filter that uses the Naive Bayes algorithm to classify emails as spam or ham."""
    def __init__(self):
        self.corpus = TrainingCorpus(None)
        self.truth_dict = dict()
        self.word_occurrences = dict()
        self.emails_dict = dict()
        self.freq_of_spam = dict()
        self.freq_of_ham = dict()
        self.spam_probability = 0.5
        self.ham_probability = 0.5
        self.logged_spam_probability = None
        self.logged_ham_probability = None

    def train(self, path):
        """Train the filter on the given corpus."""
        self.corpus.filepath = path
        self.truth_dict = self.corpus.get_truth_dict()

        amount_of_emails = len(self.truth_dict)
        self.ham_probability = count_spam_or_ham(self.truth_dict, HAM_TAG) / amount_of_emails
        self.spam_probability = count_spam_or_ham(self.truth_dict, SPAM_TAG) / amount_of_emails

        # Create a dictionary with email names as keys and their refactored texts as values.
        for name, body in self.corpus.emails():
            self.emails_dict[name] = body.lower()
            self.emails_dict[name] = replace_symbols(self.emails_dict[name])

        # Create a dictionary with words as keys and their occurrences as values.
        for body in self.emails_dict.values():
            self.word_occurrences.update(count_each_word(body))

        # Set up the frequency dictionaries.
        for key in self.word_occurrences.keys():
            self.freq_of_spam[key] = 1
            self.freq_of_ham[key] = 1

        # Calculate the amount of each word in spam and ham emails.
        for name, body in self.emails_dict.items():
            words = body.split()
            for word in words:
                if word in self.word_occurrences.keys():
                    if self.truth_dict[name] == SPAM_TAG:
                        self.freq_of_spam[word] += self.word_occurrences[word]
                    elif self.truth_dict[name] == HAM_TAG:
                        self.freq_of_ham[word] += self.word_occurrences[word]

        # Calculate the frequency of each word in spam and ham emails.
        words_in_spam = sum(self.freq_of_spam.values())
        words_in_ham = sum(self.freq_of_ham.values())
        for key in self.word_occurrences.keys():
            self.freq_of_spam[key] /= words_in_spam
            self.freq_of_ham[key] /= words_in_ham
        #On each key there is amount of word in spam/ham emails divided by the total amount of words in spam/ham emails

    def is_spam(self, email):
        """Return True if the email is spam, False otherwise."""
        # Refactor the email text.
        email = email.lower()
        email = replace_symbols(email)

        #Take the logarithm of the spam and ham probabilities for calculations.
        self.logged_spam_probability = log(self.spam_probability)
        self.logged_ham_probability = log(self.ham_probability)

        # Calculate the probability of the email being spam or ham.
        for word in email.split():
            if word in self.freq_of_spam and word in self.freq_of_ham:
                self.logged_spam_probability += log(self.freq_of_spam[word])
                self.logged_ham_probability += log(self.freq_of_ham[word])

        return self.logged_spam_probability > self.logged_ham_probability

    def test(self, path):
        """Test the filter on the given corpus and write the predictions to the corpus directory."""
        self.corpus.filepath = path
        f = open(path + '/' + PREDICTION_FILE, 'w+', encoding='UTF-8')
        for name, body in self.corpus.emails():
            f.write(name + ' ' + (SPAM_TAG if self.is_spam(body) else HAM_TAG) + '\n')
        f.close()
