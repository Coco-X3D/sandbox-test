import socket
import threading
import random
import uuid
import numpy as np
import json

'''
 =============================Coere Functions for Q1 =============================
'''
# Let's first select a common 5-word list, since the first step is to test whether the input is a English word, only valid word input counts for one attempt
def load_word_list():
    # return a list of common 5-letter English words
    word_list = np.loadtxt('./common_words.txt', dtype=str)
    word_list_lower = np.char.lower(word_list)
    mask = np.array([len(word) == 5 and word.isalpha() for word in word_list_lower])
    five_letter_words = word_list_lower[mask]
    return five_letter_words

def is_5_english_word(word, word_list):
    # check if the input word is a valid 5-letter English word
    word = word.lower()
    if len(word) != 5 or not word.isalpha() or word not in word_list:
        raise ValueError("Input word must be a 5-letter English word")
    return word in word_list

# We need to give  a feedback for each guess, intuitively, we can use colors to represent the feedback
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


# create a TCP server to handle multiple clients
class WordleServer:
    def __init__(self, host='localhost', max_attempt = 6, port=8800):
        self.host = host
        self.port = port
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.word_list = None
        self.running = False
        self.max_attempt = max_attempt

    def load_word_list(self):
        try:
            self.word_list = load_word_list()
        except Exception as e:
            print(f"Error loading word list: {e}")
            raise

    def create_session(self, max_attempts=self.max_attempt):
        """create a new game session and return the session ID"""
       
        session_id = str(uuid.uuid4())[:8]  
        
        # choose a random answer
        answer = random.choice(list(self.word_list)).lower()
        
        # create session data
        self.sessions[session_id] = {
            'answer': answer,
            'attempts': 0,
            'max_attempts':max_attempts,
            'game_over': False
        }
        
        print(f"Created session {session_id} with answer: {answer}")
        return session_id
    
    def process_guess(self, session_id, guess):
        """return feedback for a guess in a session"""
        session = self.sessions.get(session_id)
        if not session:
            return "ERROR:Invalid session"
            
        if session['game_over']:
            return "ERROR:Game over"
            
        # validate guess
        # session['letter_tracker'].display_alphabet()
        guess = guess.lower().strip()
        try:
            is_5_english_word(guess, self.word_list)
        except ValueError as ve:
            return f"ERROR:{str(ve)}"

        session['attempts'] += 1
        answer = session['answer']
        
        # generate a feedback, same as q1
        feedback = []
        for i in range(5):
            if guess[i] == answer[i]:
                feedback.append('H')  # Hit
            elif guess[i] in answer:
                feedback.append('P')  # Present
            else:
                feedback.append('M')  # Miss
        # print_colored_guess(guess, feedback)
        # session['letter_tracker'].update_status(guess, feedback)
        
        # check win/lose conditions
        if guess == answer:
            session['game_over'] = True
            return "WIN"
        elif session['attempts'] >= session['max_attempts']:
            session['game_over'] = True
            return f"LOSE:{answer}"
        else:
            return f"FEEDBACK:{''.join(feedback)}"

    
    def cleanup_session(self, session_id):
        """cleanup session data"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            print(f"Session {session_id} cleaned up")
    
    def handle_client(self, client_socket, client_address):
        # Handle a client connection
        session_id = None
        try:
            while True:
                # accept data from the client
                data = client_socket.recv(1024).decode('utf-8').strip()
                if not data:
                    break
                
                print(f"Received from {client_address}: {data}")
                
                # decode the command and process it
                if data == "START":
                    session_id = self.create_session()
                    response = f"SESSION:{session_id}"
                    
                elif data.startswith("GUESS:"):
                    if not session_id:
                        response = "ERROR:No active session"
                    else:
                        guess = data[6:]
                        response = self.process_guess(session_id, guess)

                elif data == "QUIT":
                    response = "BYE"
                    break
                else:
                    response = "ERROR:Invalid command"
                
                # send response back to the client
                client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            if session_id:
                self.cleanup_session(session_id)
            client_socket.close()
            print(f"Connection closed: {client_address}")
    
    def start_server(self):
        # Start the server
        self.load_word_list()
        # create a TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)  # allow up to 5 pending connections, you can adjust as needed
        print(f"Server started on {self.host}:{self.port}")
        print(f"Waiting for client connections...")
        print("=" * 50)

        self.running = True

        while self.running:
            try:
                # wait for a connection
                client_socket, client_address = server_socket.accept()
                print(f"New connection from {client_address}")
                # Start a new thread to handle the client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
            except KeyboardInterrupt:
                print("Server shutting down...")
                self.running = False
                break
            except Exception as e:
                print(f"Server error: {e}")
                break

        server_socket.close()
        print("Server stopped")

def main():
    print("=" * 50)
    print("Wordle Game - TCP Server Mode")
    print("=" * 50)
    print("This is SERVER mode - clients will connect to this server")
    print("The answer is generated and validated on the server side")
    print("=" * 50)
    server = WordleServer(host='localhost', max_attempt=6, port=8800)
    server.start_server()

if __name__ == "__main__":
    main()

    
    

    
    
    
