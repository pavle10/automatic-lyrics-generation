from lyrics_generation.constants import SOURCE_PATH
import os


def get_data(separated=False):
    os.chdir(SOURCE_PATH)
    result = ""

    for name in os.listdir(os.getcwd()):
        file_path = SOURCE_PATH + name

        result += get_lyrics(file_path, separated)

    return result


def get_lyrics(path, separated=False):
    lyrics = ""

    with open(path, 'r', encoding='utf_8_sig') as file:
        for line in file:
            if not separated and line.isspace():
                continue
            lyrics += line

    return lyrics


def normalize(counter):
    s = float(sum(counter.values()))

    return [(c, cnt/s) for c, cnt in counter.items()]


def get_dataset():
    with open(f"{SOURCE_PATH}data.txt", 'r') as file:
        dataset = file.read()

    return dataset
