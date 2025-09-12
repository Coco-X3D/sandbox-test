import numpy as np 
import random


# Let's first select a common 5-word list, since the first step is to test whether the input is a English word, only valid word input counts for one attempt
def load_word_list():
    word_list = np.loadtxt('./common_words.txt', dtype=str)
    word_list_lower = np.char.lower(word_list)
    mask = np.array([len(word) == 5 and word.isalpha() for word in word_list_lower])
    five_letter_words = word_list_lower[mask]
    return five_letter_words

def is_5_english_word(word, word_list):
    word = word.lower()
    if len(word) != 5 or not word.isalpha() or word not in word_list:
        raise ValueError("Input word must be a 5-letter English word")
    return word in word_list

# Second, we have to set a correct answer for the game, which is also a 5-letter English word
def select_answer(word_list, seed=None):
    if seed is not None:
        random.seed(seed)
    if word_list is None or len(word_list) == 0:
        raise ValueError("word_list is empty")
    
    answer = random.choice(word_list).lower()
    # logging.info(f"从 {len(word_set)} 个单词中选择了答案: {answer}")
    return answer


def __main__():
    ### Initialize the game
    MAX_ATTEMPTS = 6
    ### Claim the game rules
    print("Welcome to the Wordle game!")
    print(f"You have {MAX_ATTEMPTS} attempts to guess the correct 5-letter English word.")
    print("After each guess, you will receive feedback on your guess.")

    try:
        five_words_list = load_word_list()
    except Exception as e:
        print(f"Error loading word list: {e}")
        return
    answer = select_answer(five_words_list, seed=2025)
    print("Let's start the game!")

    for i in range(MAX_ATTEMPTS):
        while True:
            guess = input(f"Attempt {i+1}/{MAX_ATTEMPTS}: Enter your 5-letter guess: ").strip().lower()
            try:
                if is_5_english_word(guess, five_words_list):
                    break
                else:
                    print("Invalid input. Please enter a valid 5-letter English word.")
            except ValueError as ve:
                print(ve)
        
        if guess == answer:
            print(f"Congratulations! You've guessed the correct word: {answer}")
            return
        else:
            feedback = []
            for j in range(5):
                if guess[j] == answer[j]:
                    feedback.append('G')  # Green
                elif guess[j] in answer:
                    feedback.append('Y')  # Yellow
                else:
                    feedback.append('B')  # Black
            print("Feedback: " + ''.join(feedback))
    print(f"Sorry, you've used all attempts. The correct word was: {answer}")




if __name__ == '__main__':
    __main__()