# Project Go

## Overview
This project is a Python implementation of the classic board game "Go". The game includes a graphical user interface (GUI) built using the `pyglet` library. It follows the Model-View-Controller (MVC) design pattern to ensure clean separation of game logic, user interface, and control flow.

## Features
- **Interactive GUI**: Allows players to place stones on a 9x9 board.
- **Game Rules**: Implements core Go rules, including capturing stones and checking for valid moves.
- **Territory Marking**: Automatically claims territory and computes scores.
- **MVC Architecture**: Clean separation of concerns for maintainability and scalability.

## Installation
1. Clone the repository
2. Install dependencies:
    ```bash
    pip install pyglet
    ```
    
## How to Run
1. Navigate to the project directory
2. Run the game:
    ```bash
    python3 controller.py
    ```

## File Structure
- `controller.py`: Contains the Controller class that manages the game flow.
- `client.py`: Contains the View class which renders the game interface using `pyglet`.
- `game_model.py`: Contains the Model class which handles game logic.
- `graphics.py`: Contains helper classes for rendering graphical elements.
- `template.py`: Contains template classes for territory marking and group handling.

## How to Play
1. **Start a new game**: Click the "New Game" button.
2. **Place a stone**: Click on the board to place a stone. The game will automatically check for captures and update the board.
3. **Pass**: Click the "Pass" button to pass your turn.
4. **End the game**: The game will end when both players pass consecutively, and the final score will be calculated.

## Acknowledgements
This project was developed as part of the MAT101 Programming course at the University of Zurich.
