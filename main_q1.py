import numpy as np 
import random
import socket
import threading
import json
from typing import Dict, Any
import uuid

'''
 =============================Coere Functions for Q1 =============================
'''
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

# Third, we need to give  a feedback for each guess, intuitively, we can use colors to represent the feedback
# Green: correct letter in the correct position
# Yellow: correct letter in the wrong position
# Black: incorrect letter
class Colors:
    # Color codes for letters
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLACK = "\033[30m"
    WHITE = "\033[37m"
    
    # Background colors
    BG_GREEN = "\033[42m"    #  Hit
    BG_YELLOW = "\033[43m"   #  Present  
    BG_BLACK = "\033[40m"    #  Miss
    BG_WHITE = "\033[47m"    #  white background for letter tracker
    
    # final combinations
    HIT = BG_GREEN + WHITE + BOLD
    PRESENT = BG_YELLOW + BLACK + BOLD
    MISS = BG_BLACK + WHITE
    MISS_TRACKER = BG_WHITE + BLACK

def print_colored_guess(guess, feedback):
    ### return colored feedback for the guess.
    colored_output = ""
    for i, (letter, fb) in enumerate(zip(guess.upper(), feedback)):
        if fb == 'H':  # Hit 
            colored_output += f"{Colors.HIT} {letter} {Colors.RESET}"
        elif fb == 'P':  # Present 
            colored_output += f"{Colors.PRESENT} {letter} {Colors.RESET}"
        elif fb == 'M':  # Miss 
            colored_output += f"{Colors.MISS} {letter} {Colors.RESET}"
    print(colored_output)

# Finally, I need to give a prompt (A-Z) to the user, and let them know which gussed letter is not in the answer
class LetterTracker:
    '''Track the status of each letter and display the used letters'''
   
    def __init__(self):
        # initialize all letters to None (not used)
        self.letter_status = {letter: None for letter in 'abcdefghijklmnopqrstuvwxyz'}
    
    def update_status(self, guess, feedback):
        """change the status of letters based on the latest guess and feedback"""
        for letter, status in zip(guess, feedback):

            letter_lower = letter.lower()
            current_status = self.letter_status[letter_lower]
            
            if status == 'H': 
                self.letter_status[letter_lower] = 'H'
            elif status == 'P': 
                self.letter_status[letter_lower] = 'P'
            elif status == 'M':
                self.letter_status[letter_lower] = 'M'
    
    def get_letter_display(self, letter):
        """get the display string for a letter based on its status"""
        status = self.letter_status[letter]
        if status == 'H':
            return f"{Colors.HIT} {letter.upper()} {Colors.RESET}"
        elif status == 'P':
            return f"{Colors.PRESENT} {letter.upper()} {Colors.RESET}"
        elif status == 'M':
            return f"{Colors.MISS_TRACKER} {letter.upper()} {Colors.RESET}"
        else:
            return f" {letter.upper()} "
            
    def display_alphabet(self):
        """show the current status of all letters in the alphabet"""
        print(f"\n{Colors.BOLD}status of all letters:{Colors.RESET}")
        print("⎯" * 40)
        
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for i in range(0, len(alphabet), 13):
            row = alphabet[i:i+13]
            row_display = ""
            for letter in row:
                row_display += self.get_letter_display(letter)
            print(row_display)
        print("⎯" * 40)




def __main__():
    ### Initialize the game
    MAX_ATTEMPTS = 6
    ### Claim the game rules
    print("Welcome to the Wordle game!")
    print(f"You have {MAX_ATTEMPTS} attempts to guess the correct 5-letter English word.")
    print("After each guess, you will receive feedback on your guess.")
    print(f"{Colors.HIT} H {Colors.RESET} - The letter is correct and in the correct position")
    print(f"{Colors.PRESENT} P {Colors.RESET} - The letter is correct but in the wrong position")  
    print(f"{Colors.MISS} M {Colors.RESET} - The letter is not in the word")


    try:
        five_words_list = load_word_list()
    except Exception as e:
        print(f"Error loading word list: {e}")
        return
    answer = select_answer(five_words_list, seed=None)
    letter_tracker = LetterTracker()
    print("Let's start the game!")

    for i in range(MAX_ATTEMPTS):
        letter_tracker.display_alphabet()
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
            print("="*40 + "  ^_^  " + "="*40)
            return
        else:
            feedback = []
            for j in range(5):
                if guess[j] == answer[j]:
                    feedback.append('H')  # Green
                elif guess[j] in answer:
                    feedback.append('P')  # Yellow
                else:
                    feedback.append('M')  # Black
            colored_feedback = print_colored_guess(guess, feedback)
            letter_tracker.update_status(guess, feedback)
    print(f"Sorry, you've used all attempts. The correct word was: {answer}")
    print("="*40 + "  >_<  " + "="*40)




if __name__ == '__main__':
    __main__()