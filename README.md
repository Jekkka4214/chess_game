                                                Chess Game in Python
A classic Chess game built from scratch using Python and the Pygame library. The project follows Object-Oriented Programming (OOP) principles and implements a clean Separation of Concerns architecture.

 
                                                   Key Features:

1. Complete Chess Logic: Unique movement rules implemented for all pieces (Pawn, Knight, Bishop, Rook, Queen, and King).


2. Special Rules Support: Includes logic for castling (both short and long), checks, checkmates, and stalemates.


3. Move Highlights: Selecting a piece displays subtle dots indicating all its valid squares, fully calculating king safety before allowing a move.


4. Audio Atmosphere: Integrated sound effects for standard moves, captures, castling, checks, and game-over scenarios.


5. State Persistence: Ability to pause your game, save its current state to a JSON file, and load it back instantly.


6. Move History Logging: Every move played is automatically appended to a local game_log.txt file for match analysis.


                                        Architecture & Codebase Structure:

1. The application's logic is split into standalone, decoupled modules:


2. Board.py — Manages the 8x8 matrix state, coordinates turn flags, and handles move validation/checks.


3. Piece.py — Houses the base Piece class along with specialized subclasses for each individual chess piece type.


4. JSON.py (SaveManager) — An isolated serialization module utility that extracts board data to JSON format and reconstructs objects upon loading.


5. main.py — Houses the core Pygame execution loop, handles user input (mouse clicks, key binds), and draws the user interface.


                                                 Controls & Hotkeys
Left Mouse Button (LMC) — Click to select a piece / Click on a highlighted dot to make a move.

S Key — Save the current state of the game to savegame.json.

L Key — Load the last saved game layout back into the active session.

                                                   Requirements
1. To launch and run the game, you will need Python 3.10+ and the Pygame package installed
2. Install the required Pygame package wrapper via your system terminal: pip install pygame
3. Execute the main script from the root directory of the project: python main.py
