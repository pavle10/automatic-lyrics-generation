from lyrics_generation import charlm as clm
from lyrics_generation import wordlm as wlm
import time

if __name__ == '__main__':
    char_model = clm.CharLangModel(5, True)
    word_model = wlm.WordLangModel(5, True)

    print("Start training char model...")
    start_time = time.time()
    char_model.train_model()
    end_time = time.time()
    print(f"Finished with char model training!\nTime: {end_time - start_time}\n")

    print("Start training word model...")
    wstart_time = time.time()
    word_model.train_model()
    wend_time = time.time()
    print(f"Finished with word model training!\nTime: {wend_time - wstart_time}\n")

    print("Char model sample:\n")
    print(char_model.generate_text())

    print()

    print("Word model sample:\n")
    print(word_model.generate_text(100))
