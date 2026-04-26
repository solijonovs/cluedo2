# Cluedo Game - Project 2 Part 2

## Student Name
King Solijonov

## Project Overview
This project is a text-based Python implementation of the classic murder mystery game Cluedo, also known as Clue. The Part 2 version expands the original game setup by adding suggestion/refutation logic, deduction tracking, card dealing, and accusation mechanics.

## Features Implemented

### Game Setup
- Mansion layout with connected rooms
- Character definitions and starting positions
- Weapon definitions
- Random murder solution selection
- Card deck creation
- Solution cards removed from deck
- Remaining cards dealt among players

### Player Movement
- Player can move between connected rooms.
- Computer players also move automatically.

### Suggestions and Refutations
- Player can make a suggestion from their current room.
- A suggestion includes:
  - Suspect
  - Weapon
  - Room
- Other players are checked in turn order.
- If a player has a matching card, they refute the suggestion.
- Human player sees the refutation card when applicable.

### Deduction Notebook
The game includes a deduction notebook that tracks:
- Cards the player has seen
- Unknown cards
- Suggestion history
- Refutation history
- Cards shown to the human player

### Accusation Mechanism
- Human player can make an accusation at any time.
- If correct, the player wins.
- If incorrect, the player loses.
- Computer players have a small chance of making an accusation.

## Files Included
- `cluedo_game_part2.py` - Main Python source code
- `KingSolijonov_Readme.md` - Project instructions
- `Project2_Part2_Documentation.pdf` - Project documentation PDF

## Dependencies
No external Python packages are required.

Required:
- Python 3.10 or higher

## How to Run

1. Open Terminal.

2. Navigate to the project folder:

```bash
cd KingSolijonov_Project2_Part2_SourceCode
```

3. Run the game:

```bash
python3 cluedo_game_part2.py
```

## How to Push to GitHub

If this is a new GitHub repository:

```bash
git init
git add .
git commit -m "Add Cluedo Part 2 project"
git branch -M main
git remote add origin https://github.com/solijonovs/Cluedo.git
git push -u origin main
```

If the remote already exists:

```bash
git add .
git commit -m "Add Cluedo Part 2 project"
git push
```

## Suggested Demo Flow for Screen Recording
1. Start the game.
2. Choose a character.
3. Show your cards.
4. Move to another room.
5. Make a suggestion.
6. Show how another player refutes the suggestion.
7. Open the deduction notebook.
8. Make an accusation.
9. Explain the result.

## Presentation Talking Points
- Explain the goal of Cluedo.
- Show how the game randomly chooses a hidden solution.
- Explain how cards are dealt after removing the solution.
- Demonstrate room movement.
- Demonstrate suggestions and refutations.
- Show how the notebook supports deduction.
- Demonstrate the accusation mechanism.
- Discuss challenges and future improvements.

## Future Improvements
- Add a graphical user interface
- Add smarter AI deduction
- Add full multiplayer support
- Add save/load game state
- Improve visual board representation


## Frontend Version

A browser-based frontend has been added in the `frontend` folder.

### How to Run the Frontend

1. Open the project folder.
2. Open the `frontend` folder.
3. Double-click `index.html`.

Or from Terminal:

```bash
cd KingSolijonov_Project2_Part2_SourceCode/frontend
open index.html
```

### Frontend Features
- Visual mansion board
- Room movement buttons
- Suggestion and refutation interface
- Deduction notebook
- Accusation mechanism
- New game button

The frontend is built with plain HTML, CSS, and JavaScript, so it does not require any extra dependencies.
