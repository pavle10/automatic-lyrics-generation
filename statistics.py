from lyrics_generation import helper as hlp
from collections import Counter, defaultdict
import re


# Character level
def number_of_chars():
    data = hlp.get_data()
    total_count = 0
    count_by_char = Counter()
    alpha_chars = 0
    numeric_chars = 0
    other_chars = 0

    for char in data:
        total_count += 1
        count_by_char[char] += 1

        if char.isalpha():
            alpha_chars += 1
        elif char.isnumeric():
            numeric_chars += 1
        else:
            other_chars += 1

    print(f"Total number of characters: {total_count}")
    print(f"Number of alphabet characters: {alpha_chars}")
    print(f"Number of numeric characters: {numeric_chars}")
    print(f"Number of other characters: {other_chars}")
    print("Count by characters")
    for key, value in count_by_char.items():
        print(f"{key}: {value}")


# Word level
def number_of_words():
    data = hlp.get_data()
    total_count = 0
    count_by_length = defaultdict(Counter)
    words_with_punc = Counter()

    for word in data.split():
        total_count += 1
        count_by_length[len(word)][word] += 1
        match = re.search(r'[^a-zA-Z0-9,?!\.\']', word)

        if match:
            words_with_punc[word] += 1

    print(f"Total number of words: {total_count}")
    print("Count by length:")
    for key, value in count_by_length.items():
        print(f"{key}: {value}")
    print("Words that contain some other characters that are not alpha numeric:")
    for key, value in words_with_punc.items():
        print(f"{key}: {value}")


# Sentence level


# Paragraph level


# Lyrics level


if __name__ == '__main__':
    number_of_words()
