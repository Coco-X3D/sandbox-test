import socket
import json
import sys

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

class WordleTCPClient:
    def __init__(self, host='localhost', port=8800):
        self.host = host
        self.port = port
        self.socket = None
        self.session_id = None
        self.is_connected = False
        # self.letter_tracker = LetterTracker()
    
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            print(f"Connected to server at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            sys.exit(1)
            return False
    
    def send_command(self, command):
        if not self.is_connected:
            print("Not connected to server.")
            return None
        
        try:
            self.socket.sendall(command.encode('utf-8'))
            response = self.socket.recv(4096).decode('utf-8')
            return response
        except Exception as e:
            print(f"Error sending command: {e}")
            return None
        
    def start_game(self):
        response = self.send_command("START")
        if response and response.startswith("SESSION:"):
            self.session_id = response[8:]
            print(f"Game started. Session ID: {self.session_id}")
            return True
        else:
            print(f"Failed to start game: {response}")
            return False
    
    def make_guess(self, guess):
        if not self.session_id:
            print("No active session. Please start a game first.")
            return None
        
        command = f"GUESS:{guess}"
        response = self.send_command(command)
        return response
    
    def quit_game(self):
        response = self.send_command("QUIT")
        self.socket.close()
        self.is_connected = False
        return response
    
    # def get_status(self):
    #     """获取字母状态"""
    #     if not self.session_id:
    #         print("No active session. Please start a game first.")
    #         return None
        
    #     response = self.send_command("STATUS")
    #     return response



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

# def display_letter_status(letter_status_str):
#     """显示字母状态"""
#     if letter_status_str.startswith("STATUS:"):
#         try:
#             letter_data = json.loads(letter_status_str[7:])
#             print("\n📊 Letter Status:")
#             print("⎯" * 40)
            
#             # 按状态分类显示
#             correct = [l.upper() for l, s in letter_data.items() if s == 'H']
#             present = [l.upper() for l, s in letter_data.items() if s == 'P']
#             missing = [l.upper() for l, s in letter_data.items() if s == 'M']
#             unused = [l.upper() for l, s in letter_data.items() if s is None]
            
#             if correct:
#                 print(f"✅ Correct: {', '.join(sorted(correct))}")
#             if present:
#                 print(f"🟨 Present: {', '.join(sorted(present))}")
#             if missing:
#                 print(f"⬜ Missing: {', '.join(sorted(missing))}")
#             if unused:
#                 print(f"🔲 Unused: {', '.join(sorted(unused))}")
                
#             print("⎯" * 40)
#         except:
#             print("❌ Failed to parse letter status")




def main():
    """客户端主函数"""
    print("=" * 50)
    print("🎯 Wordle Game - TCP Client Mode")
    print("=" * 50)
    print("This is CLIENT mode - connecting to remote server")
    print("The answer is on the server side, not in this client!")
    print("=" * 50)
    
    # 创建客户端实例
    client = WordleTCPClient('localhost', 8800)
    
    # 连接到服务器
    if not client.connect():
        print("💡 Tip: Make sure the server is running on port 8800")
        return
    
    # 开始游戏
    if not client.start_game():
        return
    
    print("\n🎮 Game started! You have 6 attempts to guess the word.")
    print("💡 Commands:")
    print("  - Enter a 5-letter word to guess")
    # print("  - 'status' - show letter status")
    print("  - 'quit' - exit game")
    print("-" * 50)
    
    attempt_count = 0
    MAX_ATTEMPTS = 6
    letter_tracker = LetterTracker()

    while attempt_count < MAX_ATTEMPTS:
        letter_tracker.display_alphabet()
        guess = input(f"💡 Attempt {attempt_count + 1}/{MAX_ATTEMPTS}: Enter your 5-letter guess: ").strip().lower()
        
        if guess == 'quit':
            client.quit_game()
            print("👋 Game ended")
            break
            
        # if guess == 'status':
        #     status = client.get_status()
        #     if status:
        #         display_letter_status(status)
        #     continue
            
        try:
            if len(guess) != 5 or not guess.isalpha():
                print("❌ Invalid input. Please enter exactly 5 letters.")
                continue
                
            response = client.make_guess(guess)
            
            if response is None:
                print("❌ Server communication error")
                continue
            elif response == "WIN":
                print_colored_guess(guess, ['H']*5)
                print("🎉 CONGRATULATIONS! You guessed the word!")
                break
            elif response.startswith("LOSE:"):
                answer = response[5:]
                print("😢 You've used all attempts!")
                print(f"😢 GAME OVER! The word was: {answer.upper()}")
                break
            elif response.startswith("ERROR:"):
                print(f"❌ Error: {response[6:]}")
                continue  # 不增加attempt_count
            elif response.startswith("FEEDBACK:"):
                feedback = list(response[9:])
                letter_tracker.update_status(guess, feedback)
                print_colored_guess(guess, feedback)
                attempt_count += 1  # 只有成功提交猜测才增加计数
                
        except Exception as e:
            print(f"❌ Error processing guess: {e}")
            continue

    



    

    print("\n" + "=" * 50)
    print("Game ended. Thanks for playing!")
    print("=" * 50)



if __name__ == "__main__":
    main()  