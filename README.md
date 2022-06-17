Checkers game with easyAI
=========================
 
INTRODUCTION
------------
This is a modified version of the board game checkers. 
It was implemented with the aid of easyAI


INSTALLATION INSTRUCTIONS
-------------------------
To install easyAI follow the instructions below:

navigate to the checkers-with-easyAI and in this folder, in a terminal, type ::
    
    sudo python setup.py install

The checkers game utilizes the Numpy library, as a result, it also needs to be installed.

Two methods for installing Numpt are listed below:
1. Conda method - conda install numpy
2. pip method   - pip install numpy


GAME DESCRIPTION
----------------
Objective:
The objective of the game is to get as many pieces as you can from the opponent.

Material
An 8 x 8 board of checkers is used with two colors one for each opponent.

How to Win
The game can be won when the opponent is unable to make a move. This can be done in two ways:
The entirety of a player’s pieces was captured by the opponent (when the piece is a King)

Additional Rules
1. Only one jump is possible per move.
2. Forward move is only allowed for each opponent.
3. When a player jumps over another opponent’s piece, the piece is not removed by the opponent.
4. There are two types of moves Step or Jump.
5. The pieces always move diagonally only on dark colored squares.
6. When a player’s piece reaches the last row on the opponent’s side of the board, they can use
one of their captured pieces to crown the piece as a king.
7. The first player who has a piece promoted to king wins immediately.