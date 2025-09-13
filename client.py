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
        # response = self.send_command(f"GUESS:{word}")
        return response
    
    def quit_game(self):
        response = self.send_command("QUIT")
        self.socket.close()
        self.is_connected = False
        return response
    
    def get_status(self):
        """获取字母状态"""
        if not self.session_id:
            print("No active session. Please start a game first.")
            return None
        
        response = self.send_command("STATUS")
        return response



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

def display_letter_status(letter_status_str):
    """显示字母状态"""
    if letter_status_str.startswith("STATUS:"):
        try:
            letter_data = json.loads(letter_status_str[7:])
            print("\n📊 Letter Status:")
            print("⎯" * 40)
            
            # 按状态分类显示
            correct = [l.upper() for l, s in letter_data.items() if s == 'H']
            present = [l.upper() for l, s in letter_data.items() if s == 'P']
            missing = [l.upper() for l, s in letter_data.items() if s == 'M']
            unused = [l.upper() for l, s in letter_data.items() if s is None]
            
            if correct:
                print(f"✅ Correct: {', '.join(sorted(correct))}")
            if present:
                print(f"🟨 Present: {', '.join(sorted(present))}")
            if missing:
                print(f"⬜ Missing: {', '.join(sorted(missing))}")
            if unused:
                print(f"🔲 Unused: {', '.join(sorted(unused))}")
                
            print("⎯" * 40)
        except:
            print("❌ Failed to parse letter status")




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
    print("  - 'status' - show letter status")
    print("  - 'quit' - exit game")
    print("-" * 50)
    
    attempt_count = 0
    MAX_ATTEMPTS = 6

    for i in range(MAX_ATTEMPTS):
        guess = input(f"Attempt {i+1}/{MAX_ATTEMPTS}: Enter your 5-letter guess: ").strip().lower()

        if guess == 'quit':
            client.quit_game()
            print("👋 Game ended")
            break
        elif guess == 'status':
            status = client.get_status()
            if status:
                display_letter_status(status)
            continue

        elif len(guess) == 5 and guess.isalpha():

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
                print(f"😢 GAME OVER! The word was: {answer.upper()}")
                break
            elif response.startswith("ERROR:"):
                print(f"❌ Error: {response[6:]}")
                continue
            elif response.startswith("FEEDBACK:"):
                feedback = list(response[9:])
                print_colored_guess(guess, feedback)
    status = client.get_status()
    if status and status.startswith("STATUS:"):
        letter_data = json.loads(status[7:])
        # 从字母状态中找出答案（H状态的字母）
        answer_chars = []
        for i in range(5):
            for letter, status_val in letter_data.items():
                if status_val == 'H':
                    # 这里需要更复杂的逻辑来重建答案
                    # 简化处理：显示所有正确字母
                    answer_chars.append(letter.upper())
                if answer_chars:
                    print(f"💡 Hint: Correct letters: {', '.join(answer_chars)}")
    print("😢 You've used all attempts!")

    print("\n" + "=" * 50)
    print("Game ended. Thanks for playing!")
    print("=" * 50)



if __name__ == "__main__":
    main()  