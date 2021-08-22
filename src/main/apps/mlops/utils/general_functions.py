import json
import re
import unicodedata

from bs4 import BeautifulSoup
from pathlib import Path
from typing import (
    Dict,
    Generic,
    TypeVar,
)

SELFCLASS = TypeVar('SELFCLASS')
ABBREVIATIONS_WORDLIST_PATH = Path(__file__).resolve(
).parent.joinpath("resources/abbreviations_wordlist.json")


class ImdbSentimentTextModificator:
    """
    Generate inputs for the Fashion Mnist model.
    Credits: # https://github.com/laxmimerit/preprocess_kgptalkie (github-based class)
    """

    def __new__(cls, review: str, *args, **kwargs) -> Generic[SELFCLASS]:
        return super(ImdbSentimentTextModificator, cls).__new__(cls, *args, **kwargs)

    def __init__(self, review: str) -> None:
        self.review = review
        self.processed_review = None
        self.abbreviations_wordlist = self.get_abbreviations_wordlist()
        self.special_lowercase_rewiew()
        self.contraction_and_expansion()
        self.email_remover()
        self.urls_remover()
        self.html_tags_remover()
        self.accented_chars_remover()
        self.special_chars_remover()
        self.misspelled_words_proofreader()

    @staticmethod
    def get_abbreviations_wordlist() -> Dict:
        """Get abbreviations words from json."""
        with open(ABBREVIATIONS_WORDLIST_PATH, "r") as aw:
            abbreviations_wordlist = json.load(aw)
        return abbreviations_wordlist

    def special_lowercase_rewiew(self) -> None:
        """Change text to lowercase replacing '\' and '_'."""
        self.processed_review = str(self.review).lower().replace(
            '\\', '').replace('_', ' ')

    def contraction_and_expansion(self) -> None:
        """Change the text to lowercase and work on abbreviating words."""
        if type(self.processed_review) is str:
            for key in self.abbreviations_wordlist:
                value = self.abbreviations_wordlist[key]
                raw_text = r'\b' + key + r'\b'
                self.processed_review = re.sub(
                    raw_text, value, self.processed_review)

    def email_remover(self) -> None:
        """Completely removes all emails from the text."""
        self.processed_review = re.sub(
            r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+)', "", self.processed_review)

    def urls_remover(self) -> None:
        """Completely removes all urls from the text."""
        self.processed_review = re.sub(
            r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', self.processed_review)

    def html_tags_remover(self) -> None:
        """Completely removes all html-tags from the text."""
        self.processed_review = BeautifulSoup(
            self.processed_review, 'lxml').get_text().strip()

    def accented_chars_remover(self) -> None:
        """Completely removes all accented characters from the text."""
        self.processed_review = unicodedata.normalize(
            'NFKD', self.processed_review).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def special_chars_remover(self) -> None:
        """Completely removes all special characters from the text."""
        self.processed_review = re.sub(r'[^\w ]+', "", self.processed_review)
        self.processed_review = ' '.join(self.processed_review.split())

    def misspelled_words_proofreader(self) -> None:
        """Corrects some misspelled or exaggerated words, due to repetition of letters"""
        self.processed_review = re.sub(
            "(.)\\1{2,}", "\\1", self.processed_review)
