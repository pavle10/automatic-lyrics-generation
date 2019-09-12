import lyrics_generation.helper as hlp
from lyrics_generation.constants import END_WORD
from collections import *
import random


class WordLangModel:

    def __init__(self, n=2, separated=False):
        self.data = hlp.get_data(separated)
        self.backwards = n
        self.lang_model = defaultdict(list)
        self.start_words = self.get_start_words()

    def get_start_words(self):
        words = list()

        for line in self.data.split('\n'):
            line = line.split(' ')
            if len(line) < self.backwards:
                continue

            words.append(" ".join(line[:self.backwards]))

        return words

    def train_model(self):
        words = list(map(lambda c: '\n' if c == END_WORD else c, self.data.replace('\n', f" {END_WORD} ").split()))

        for i in range(len(words) - self.backwards):
            self.lang_model[" ".join(words[i:i+self.backwards])].append(words[i+self.backwards])

    def print_model(self):
        for key, value in self.lang_model.items():
            print(f"{key}: {value}")

    def print_start_words(self):
        for entry in self.start_words:
            print(entry)

    def generate_text(self, nwords=50):
        curr = random.choice(self.start_words)
        text = [word for word in curr.split()]

        for _ in range(nwords):
            next_word = random.choice(self.lang_model[curr])
            text.append(next_word)
            curr = " ".join(text[-self.backwards:])

        return " ".join(text)
