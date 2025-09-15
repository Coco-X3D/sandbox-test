# Worlde： Client-Server Implementation with Cheating Host
This is an implementation of the popular word-guessing game Wordle.

## Something besides the project
This game is very similar to one of my favorite games on the Nintendo Switch: Color Guessing from Clubhouse Games: 51 Worldwide Classics. I spent hundreds of hours playing it. In Color Guessing, two players simultaneously try to guess a secret code of 4 colors (with possible overlaps) selected from 7 possible colors. There are 8 rounds, and each player has 4 attempts. You can refine your next guess based on the Hit, Presence, and Miss feedback from both your own attempts and your opponent's. When I first read the task document, this game immediately came to mind.

## Features

- **Classic Wordle Game**: A faithful implementation of the original Wordle game mechanics in the console.
- **Client-Server Architecture**: Play the game over a network. The server hosts the game logic, while the client provides the interface.
- **Cheating Host Mode**: A special mode where the server can attempt to cheat by changing the target word after the client has started guessing. The client includes logic to detect this.

## Project Structure

wordle-game/
├── server.py              # Main server implementation
├── client.py              # Client implementation
├── common_words.txt       # Word database
├── main_q1.txt            # The local implementation of Feature 1
└── README.md              

## Prerequisites

- Python 3.6 or higher

## Installation

Clone the repository:
```bash
git clone https://github.com/Coco-X3D/sandbox-test.git
cd sandbox-test
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
# Please note that the standrad game server is created by the following lines in main():
#    server = WordleServer(host='localhost', max_attempt=6, port=8800)
#    server.start_server()

python server.py

```
