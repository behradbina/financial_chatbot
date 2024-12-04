import os
import json
from string import punctuation


class PersianSwear:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(PersianSwear, cls).__new__(cls)
            with open(os.getenv('PERSIAN_SWEAR_PATH'), 'r', encoding='utf-8') as file:
                cls._instance.data = json.load(file)
            cls._instance.swear_words = set(cls._instance.data["word"])
        return cls._instance

    def ignoreSY(self, text):
        translator = str.maketrans("", "", punctuation)
        return text.translate(translator)

    def filter_words(self, text, symbol="*", ignoreOT=False):
        if not self.swear_words:
            return text

        words = text.split()
        filtered_words = []
        for word in words:
            if word in self.swear_words or (
                    ignoreOT and self.ignoreSY(word) in self.swear_words
            ):
                filtered_words.append(symbol)
            else:
                filtered_words.append(word)

        return " ".join(filtered_words)

    def is_empty(self):
        return not self.swear_words

    def add_word(self, word):
        self.swear_words.add(word)
        self.data["word"].append(word)

    def remove_word(self, word):
        if word in self.swear_words:
            self.swear_words.remove(word)
        if word in self.data["word"]:
            self.data["word"].remove(word)

    def is_bad(self, text, ignoreOT=False):
        if ignoreOT:
            text = self.ignoreSY(text)
        text = text.replace("\u200c", "")
        return text in self.swear_words

    def has_swear(self, text, ignoreOT=False):
        if ignoreOT:
            text = self.ignoreSY(text)
        text = text.replace("\u200c", "")
        if not self.swear_words:
            return False

        words = text.split()
        return any(word in self.swear_words for word in words)

    def tostring(self):
        return " - ".join(self.swear_words)
