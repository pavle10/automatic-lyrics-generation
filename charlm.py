import lyrics_generation.helper as hlp
from collections import *
from random import random


class CharLangModel:

    def __init__(self, n=5, separated=False):
        self.data = hlp.get_data(separated)
        self.backwards = n
        self.lang_model = dict()
        self.start_seq = self.get_starts()

    def get_starts(self):
        counter = Counter()

        for line in self.data.split("\n"):
            counter[line[:self.backwards]] += 1

        return hlp.normalize(counter)

    def train_model(self):
        temp = defaultdict(Counter)

        for i in range(len(self.data) - self.backwards):
            backwards, char = self.data[i:i+self.backwards], self.data[i+self.backwards]
            temp[backwards][char] += 1

        self.lang_model = {back: hlp.normalize(chars) for back, chars in temp.items()}

    def generate_text(self, nletters=1000):
        sequence = self.choose_start_seq()
        res = list()
        res.append(sequence)

        for _ in range(nletters):
            char = self.choose_letter(sequence)
            sequence = sequence[1:] + char
            res.append(char)

        return "".join(res)

    def choose_start_seq(self):
        value = random()

        for seq, val in self.start_seq:
            value = value - val

            if value <= 0:
                return seq

    def choose_letter(self, seq):
        dist = self.lang_model[seq]
        value = random()

        for char, val in dist:
            value = value - val
            if value <= 0:
                return char

    def print_model(self):
        for key, value in self.lang_model.items():
            print(f"{key}: {value}")

    def print_data(self):
        print(self.data)

    def print_start_words(self):
        for word in self.start_seq.elements():
            print(word)
