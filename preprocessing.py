import lyrics_generation.helper as hlp
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


def remove_brackets(data):
    cleaner_data = ""

    for sentence in data.split('\n'):
        match = re.search(r'[()]', sentence)

        if match:
            sentence = sentence.replace('(', '')
            sentence = sentence.replace(')', '')

        cleaner_data += sentence + '\n'

    return cleaner_data


def remove_two_dots(data):
    cleaner_data = ""

    for sentence in data.split('\n'):
        match = re.search(r'[:]', sentence)

        if match and sentence.endswith(':'):
            sentence = sentence[:-1]

        cleaner_data += sentence + '\n'

    return cleaner_data


def remove_double_quotes(data):
    cleaner_data = ""

    for sentence in data.split('\n'):
        match = re.search(r'["]', sentence)

        if match:
            sentence = sentence.replace('"', '')
            print(sentence)

        cleaner_data += sentence + '\n'

    return cleaner_data


def remove_anything(data):
    for sentence in data.split('\n'):
        match = re.search(r'[^\w:," ()\[\]\'\.?!-]', sentence)

        if match:
            print(sentence)


if __name__ == '__main__':
    text = hlp.get_data(True)
    cleaner_text = remove_square_brackets(text)
    cleaner_text = remove_brackets(cleaner_text)
    cleaner_text = remove_two_dots(cleaner_text)
    cleaner_text = remove_double_quotes(cleaner_text)
    remove_anything(cleaner_text)
