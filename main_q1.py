import numpy as np 


# Let's first select a common 5-word list, since the first step is to test whether the input is a English word, only valid word input counts for one attempt
def load_word_list():
    word_list = np.loadtxt('./common_words.txt', dtype=str)
    word_list_lower = np.char.lower(word_list)
    mask = np.array([len(word) == 5 and word.isalpha() for word in word_list_lower])
    five_letter_words = word_list_lower[mask]
    return five_letter_words


def is_5_english_word(word, word_list):
    word = word.lower()
    print(word.isalpha())
    if len(word) != 5 or not word.isalpha() or not in word_list:
        raise ValueError("Input word must be a 5-letter English word")
    return word in word_list

# def test():
    # return
def __main__():
    print("This is main_q1.py")
    a = load_word_list()
    b = is_5_english_word("apsle", a)
    print(b)



if __name__ == '__main__':
    __main__()