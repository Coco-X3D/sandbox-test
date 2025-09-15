# Worlde： Client-Server Implementation with Cheating Host
This is an implementation of the popular word-guessing game Wordle.

## Something besides the project
This game is very similar to one of my favorite games on the Nintendo Switch: Color Guessing from Clubhouse Games: 51 Worldwide Classics. I spent hundreds of hours playing it. In Color Guessing, two players simultaneously try to guess a secret code of 4 colors (with possible overlaps) selected from 7 possible colors. There are 8 rounds, and each player has 4 attempts. You can refine your next guess based on the Hit, Presence, and Miss feedback from both your own attempts and your opponent's. When I first read the task document, this game immediately came to mind.

## Features

- **Classic Wordle Game**: A faithful implementation of the original Wordle game mechanics in the console.
- **Client-Server Architecture**: Play the game over a network through TCP. The server hosts the game logic, while the client provides the interface.
- **Cheating Host Mode**: A special mode where the server can attempt to cheat by changing the target word after the client has started guessing. The client includes logic to detect this.

## Project Structure
```
wordle-game/
├── server.py              # Main server implementation
├── client.py              # Client implementation
├── common_words.txt       # Word database
├── main_q1.txt            # The local implementation of Feature 1
└── README.md
```              

## Prerequisites

- Python 3.6 or higher

## Installation

Clone the repository:
```bash
git clone https://github.com/Coco-X3D/sandbox-test.git
cd sandbox-test
```

## Game Rules
```
1. Start the game by running the appropriate mode
2. Enter your guess - a 5-letter English word
3. Receive feedback:
    🟩 Green background: Correct letter in correct position
    🟨 Yellow background: Correct letter in wrong position
    ⬜ Gray background: Letter not in the word
4. Use the feedback to make your next guess
5. Win by guessing the word within 6 attempts (Of course, you can change it as you like).
```

## How to run
### 1. Classic mode
To play a standrad game of Wordle locally
```bash
python main_q1.py
```

### 2. Client Server Game
Step 1: Start the Server
```bash
# Open a new cmd/powershell window for running server
# Set the number of attempts in main()

# Please note that the standrad game server is created by the following lines in main():
#    server = WordleServer(host='localhost', max_attempt=6, port=8800)
#    server.start_server()

python server.py
```

Step 2: Connect the Client
```bash
# Open a new cmd/powershell window for client side

python client.py
```

### 3. Host Cheating Mode
```bash
# Using CheatingWordleServer() to replace WordleServer() in main() of server.py 
# num_candiates indicates the number of words hold for cheating
cheating_server = CheatingWordleServer(max_attempt = 6, num_candidates=10)
cheating_server.start_server()
```






## An example
```bash
###            From Serve Side 
###

PS E:\sandbox-test> PYTHON .\server.py
==================================================
Wordle Game - TCP Server Mode
==================================================
This is SERVER mode - clients will connect to this server
The answer is generated and validated on the server side
==================================================
Server started on localhost:8800
Waiting for client connections...
==================================================
New connection from ('127.0.0.1', 55028)
Received from ('127.0.0.1', 55028): START
Created cheating session 0cd5bc11 with 10 candidates
Initial candidates (10): ['maria', 'palau', 'madam', 'seize', 'discs', 'breed', 'depot', 'offer', 'roman', 'vivid']
Received from ('127.0.0.1', 55028): MAX_ITER
Received from ('127.0.0.1', 55028): GUESS:abuse
📊 Worst score (H, P): (0, 0), Candidates: 1
🔍 Candidates reduced to 1
   Remaining: ['vivid']
🔒 Final answer locked: vivid
Received from ('127.0.0.1', 55028): GUESS:right
📊 Worst score (H, P): (1, 0), Candidates: 1
🔍 Candidates reduced to 1
   Remaining: ['vivid']
🔒 Final answer locked: vivid
Received from ('127.0.0.1', 55028): GUESS:urban
📊 Worst score (H, P): (0, 0), Candidates: 1
🔍 Candidates reduced to 1
   Remaining: ['vivid']
🔒 Final answer locked: vivid
Received from ('127.0.0.1', 55028): GUESS:opose
Received from ('127.0.0.1', 55028): GUESS:upper
📊 Worst score (H, P): (0, 0), Candidates: 1
🔍 Candidates reduced to 1
   Remaining: ['vivid']
🔒 Final answer locked: vivid
Received from ('127.0.0.1', 55028): GUESS:watch
📊 Worst score (H, P): (0, 0), Candidates: 1
🔍 Candidates reduced to 1
   Remaining: ['vivid']
🔒 Final answer locked: vivid
Received from ('127.0.0.1', 55028): GUESS:lucky
📊 Worst score (H, P): (0, 0), Candidates: 1
🔍 Candidates reduced to 1
   Remaining: ['vivid']
🔒 Final answer locked: vivid
Session 0cd5bc11 cleaned up
Connection closed: ('127.0.0.1', 55028)

###              From Client Side
###

E:\sandbox-test>python client.py
==================================================
🎯 Wordle Game - TCP Client Mode
==================================================
This is CLIENT mode - connecting to remote server
The answer is on the server side, not in this client!
==================================================
Connected to server at localhost:8800
Game started. Session ID: 0cd5bc11

🎮 Game started! You have 6 attempts to guess the word.
💡 Commands:
  - Enter a 5-letter word to guess
  - 'quit' - exit game
--------------------------------------------------

status of all letters:
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
 A  B  C  D  E  F  G  H  I  J  K  L  M
 N  O  P  Q  R  S  T  U  V  W  X  Y  Z
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
💡 Attempt 1/6: Enter your 5-letter guess: abuse
 A  B  U  S  E

status of all letters:
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
 A  B  C  D  E  F  G  H  I  J  K  L  M
 N  O  P  Q  R  S  T  U  V  W  X  Y  Z
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
💡 Attempt 2/6: Enter your 5-letter guess: right
 R  I  G  H  T

status of all letters:
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
 A  B  C  D  E  F  G  H  I  J  K  L  M
 N  O  P  Q  R  S  T  U  V  W  X  Y  Z
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
💡 Attempt 3/6: Enter your 5-letter guess: urban
 U  R  B  A  N

status of all letters:
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
 A  B  C  D  E  F  G  H  I  J  K  L  M
 N  O  P  Q  R  S  T  U  V  W  X  Y  Z
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
💡 Attempt 4/6: Enter your 5-letter guess: opose
❌ Error: Input word must be a 5-letter English word

status of all letters:
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
 A  B  C  D  E  F  G  H  I  J  K  L  M
 N  O  P  Q  R  S  T  U  V  W  X  Y  Z
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
💡 Attempt 4/6: Enter your 5-letter guess: upper
 U  P  P  E  R

status of all letters:
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
 A  B  C  D  E  F  G  H  I  J  K  L  M
 N  O  P  Q  R  S  T  U  V  W  X  Y  Z
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
💡 Attempt 5/6: Enter your 5-letter guess: watch
 W  A  T  C  H

status of all letters:
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
 A  B  C  D  E  F  G  H  I  J  K  L  M
 N  O  P  Q  R  S  T  U  V  W  X  Y  Z
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
💡 Attempt 6/6: Enter your 5-letter guess: lucky
😢 You've used all attempts!
😢 GAME OVER! The word was: VIVID

==================================================
Game ended. Thanks for playing!
==================================================
``` 


## License
This project is licensed under the MIT License.

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.