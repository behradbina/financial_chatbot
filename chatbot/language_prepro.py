import re
import os

from hazm import Normalizer, TokenSplitter, Stemmer, InformalNormalizer
from hazm.utils import stopwords_list


class PreproText:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(PreproText, cls).__new__(cls)
            cls.__show_capability()
        return cls._instance

    def __init__(self):
        self.pattern = re.compile(r'[^\u0600-\u06FF0-9\s]+|[^\w\s]+')
        self.normalizer = Normalizer()
        self.formal_normalizer = InformalNormalizer()
        self.splitter = TokenSplitter()
        self.stemmer = Stemmer()
        self.stopwords_list = stopwords_list()

    @staticmethod
    def __show_capability():
        print("_" * 70)
        print(" - Config for Preprocessing input text:")
        print("\t >>> remove specials chars :", os.getenv('REMOVE_SPECIALS_CHARS'))
        print("\t >>> text normalizer: ", os.getenv('NORMAL_TEXT'))
        print("\t >>> InformalNormalizer: ", os.getenv('FORMAL_TEXT'))
        print("\t >>> split stuck words: ", os.getenv('SPLIT_STUCK_WORDS'))
        print("\t >>> remove stop words: ", os.getenv('REMOVE_STOP_WORDS'))
        print("\t >>> text stemming: ", os.getenv('STEMMING_TEXT'))
        print("_" * 70)

    def remove_specials_chars(self, text):
        text = re.sub(self.pattern, '', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def normal_text(self, text):
        return self.normalizer.normalize(text)

    def formal_text(self, text):
        return " ".join(item[-1] for item in self.formal_normalizer.normalize(text)[0])

    def split_stuck_words(self, text):
        try:
            split_tokens = " ".join(item for item in self.splitter.split_token_words(text)[0])
        except IndexError:
            split_tokens = text

        return split_tokens

    def remove_stop_words(self, text):
        return " ".join(item for item in text.split() if item not in self.stopwords_list)

    def stemming_text(self, text):
        return self.stemmer.stem(text)

    def clean_context(self, context):
        # Remove invalid characters from the provided context
        text = re.sub(self.pattern, '', context)
        # Replace consecutive whitespace characters with a single space
        text = re.sub(r'\s+', ' ', text)
        return text

    def cleaning_text(self, text):
        # if os.getenv('REMOVE_SPECIALS_CHARS'):
        text1 = self.remove_specials_chars(text)
        # if os.getenv('REMOVE_STOP_WORDS'):
        #     text = self.remove_stop_words(text)
        # if os.getenv('NORMAL_TEXT'):
        #     text = self.normal_text(text)
        # if os.getenv('FORMAL_TEXT'):
        #     text = self.formal_text(text)
        # if os.getenv('SPLIT_STUCK_WORDS'):
        text1 = self.split_stuck_words(text1)
        # if os.getenv('STEMMING_TEXT'):
        #     text = self.stemming_text(text)

        # add ؟ to end of  sentence
        return text1
