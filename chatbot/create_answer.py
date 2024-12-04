import os
import re

from .language_prepro import PreproText
from .persianswear import PersianSwear
from .rag import RAGModel


persian_swear = PersianSwear()
text_cleaner = PreproText()


class CreateAnswer:
    def __init__(self):
        self.pipline = RAGModel()
        
    @staticmethod
    def __validate_input(text):
        pattern = re.compile(r'[^\u0600-\u06FF0-9\s]+|[^\w\s]+')
        illegal_pattern = re.compile(r'^[0-9]+$|^[0-9\u0600-\u06FF\s]+$')
        number_pattern = re.compile(r'^[0-9]+$')

        text = re.sub(pattern, '', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(number_pattern, '', text)

        if text is None or not isinstance(text, str):
            return False
        elif not illegal_pattern.match(text):
            return False
        elif len(text.strip()) == 0:
            return False
        else:
            return True

    def get_question(self, question, user_id):
        print(f"\t------ question: {question}")
        if not self.__validate_input(question):
            return os.getenv('INVALID_QUESTION'), False

        elif persian_swear.has_swear(question):
            return os.getenv('SWEAR_QUESTION'), False

        elif "سلام" in question:
            return os.getenv('GREETING_ANSWER'), True

        else:
            clean_question = text_cleaner.cleaning_text(question)
            answer = self.pipline.run_rag(clean_question, user_id)
            
            print(f"\t------ answers: {answer}")
            if not answer:
                return os.getenv('RETRIEVE_NO_ANSWER_FOUND'), True
            return answer, True
