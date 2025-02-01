import os
from utils import read_classification_from_file, TRUTH_FILE

class Corpus:
    """Corpus class is a base class for the TrainingCorpus class."""
    def __init__(self, filepath):
        self.filepath = filepath

    def emails(self):
        """Yields the name and body of each email in the corpus."""
        mails = os.listdir(self.filepath)
        for mail in mails:
            if '!' not in mail:
                name = mail
                with open(self.filepath+'/'+mail, 'rt', encoding='UTF-8') as f:
                    body = ''
                    for line in f:
                        body += line
                    yield name, body


class TrainingCorpus(Corpus):
    """TrainingCorpus class is a subclass of the Corpus class."""
    def __init__(self, filepath):
        super().__init__(filepath)
        self.truth_dict = None
        self.filepath = filepath

    def get_truth_dict(self):
        self.truth_dict = read_classification_from_file(self.filepath + '/' + TRUTH_FILE)
        return self.truth_dict

    def get_class(self, key):
        """Functions for testing purposes."""
        return self.truth_dict[key]

    def is_spam(self, key):
        """Functions for testing purposes."""
        return True if self.truth_dict[key] == 'SPAM' else False

    def is_ham(self, key):
        """Functions for testing purposes."""
        return True if self.truth_dict[key] == 'OK' else False

    def spams(self):
        """Functions for testing purposes."""
        name = list(self.emails())
        for key in name:
            if self.truth_dict[key[0]] == 'SPAM':
                yield key[0], key[1]

    def hams(self):
        """Functions for testing purposes."""
        name = list(self.emails())
        for key in name:
            if self.truth_dict[key[0]] == 'OK':
                yield key[0], key[1]
