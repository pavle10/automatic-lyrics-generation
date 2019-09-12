import lyrics_generation.helper as hlp
from lyrics_generation.constants import SOURCE_PATH
import re


def remove_square_brackets(data):
    cleaner_data = ""

    for sentence in data.split('\n'):
        match = re.search(r'[\[\]]', sentence)

        if match:
            sentence = sentence.replace(sentence[sentence.find('['): sentence.find(']')+1], '').strip()

            if sentence == '':
                continue

        cleaner_data += sentence + "\n"

    return cleaner_data


def remove_bad_chars(data):
    cleaner_data = ""

    for sentence in data.split('\n'):
        match_dollar = re.search(r'[]', sentence)
        match_cent = re.search(r'[¢]', sentence)
        match_star = re.search(r'[*]', sentence)

        if match_dollar:
            idx = match_dollar.span()[0] - 1
            sentence = sentence.replace(sentence[idx:idx+3], "'")
        elif match_cent:
            idx = match_cent.span()[0] - 1
            sentence = sentence.replace(sentence[idx:idx+2], '')
        elif match_star:
            sentence = sentence.replace('*', '')

        cleaner_data += sentence + '\n'

    return cleaner_data


def remove_brackets(data):
    cleaner_data = ""

    for sentence in data.split('\n'):
        match = re.findall(r'[()]', sentence)

        if match:
            sentence = sentence.replace('(', '')
            sentence = sentence.replace(')', '')

        cleaner_data += sentence + '\n'

    return cleaner_data


def remove_double_quotes(data):
    cleaner_data = ""

    for sentence in data.split('\n'):
        match = re.search(r'["]', sentence)

        if match:
            sentence = sentence.replace('"', '')

        cleaner_data += sentence + '\n'

    return cleaner_data


def fix_newlines(data):
    cleaner_data = ""
    prev = False

    for sentence in data.split('\n'):
        if sentence == '' and prev:
            continue
        elif sentence == '':
            prev = True
        else:
            prev = False

        cleaner_data += sentence + '\n'

    return cleaner_data


def save_dataset(data):
    with open(f"{SOURCE_PATH}data.txt", 'w') as file:
        file.write(data)


if __name__ == '__main__':
    text = hlp.get_data(True)
    dataset = remove_bad_chars(text)
    dataset = remove_square_brackets(dataset)
    dataset = remove_brackets(dataset)
    dataset = remove_double_quotes(dataset)
    dataset = fix_newlines(dataset)

    save_dataset(dataset)
