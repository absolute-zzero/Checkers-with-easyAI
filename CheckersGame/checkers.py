"""
Group Members: Romari Bartley, Gerrel Bones, David Porter
Date: 6/12/2022
Project: #1
Project Description: This code is for a simple and modified version
                     of the board game checkers. The difference is
that once there is a one move between two pieces, a piece is able
to jump or skip over the other, whether ally or foe. In other words,
there is no "killing" in this version of checkers since no piece is
removed. Finally, the a player is considered to win the game if they
are the first to have one of their pieces become king. This would also
mean that there is no backward moves since the game ends after any
player becomes king.
"""

from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
from easyAI import solve_with_iterative_deepening
import numpy as np

# black_square
even = [0,2,4,6]
odd = [1,3,5,7]

# init
even_row = [(i,j) for i in even for j in odd]
odd_row = [(i,j) for i in odd for j in even]

black_squares = even_row + odd_row

class Checker(TwoPlayerGame):
    def __init__(self, players):
        """
        initializes the class
        Creates a blank board
        Completes it by placing each piece in their initial positions
        """

        self.players = players
        # self.board = np.arange(8 * 8).reshape(8,8)

        #####self.blank_board = np.full((8,8),['0'],dtype=str)

        self.blank_board = np.zeros((8,8), dtype=object)

        self.board = self.blank_board.copy()
        self.black_pieces = [
            (0,1), (0,3), (0,5), (0,7),
            (1,0), (1,2), (1,4), (1,6)
        ]
        self.white_pieces = [
            (6,1), (6,3), (6,5), (6,7),
            (7,0), (7,2), (7,4), (7,6)
        ]
        for i,j in self.black_pieces:
            self.board[i,j] = "B"
        for i,j in self.white_pieces:
            self.board[i,j] = "W"

        self.white_territory = [(7,0), (7,2), (7,4), (7,6)]
        self.black_territory = [(0,1), (0,3), (0,5), (0,7)]


        self.players[0].pos = self.white_pieces
        self.players[1].pos = self.black_pieces

        self.current_player = 1  # player 1 starts.

    def possible_moves_on_white_turn(self):
    # returns the possible moves for the white pieces
        table_pos = []
        old_new_piece_pos = []

        # board position before move
        board = self.blank_board.copy()
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l

        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player-1].pos:
            old_piece_pos = v

            step_pos = [(v[0]-1, v[1]-1), (v[0]-1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B","W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j))
                    else:
                        old_new_piece_pos.append((old_piece_pos,n))

        # board position after  move
        for i,j in old_new_piece_pos:
            #print(f"i = {i}")
            b = board.copy()
            b[i[0], i[1]] = 0 # old position
            b[j[0], j[1]] = "W" # new position
            # print(b)
            table_pos.append(b)
            assert len(np.where(b != 0)[0]) == 16, f"In possible_moves_on_white_turn(), there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"


        self.board = board
        return table_pos

    def possible_moves_on_black_turn(self):
    #returns the possible moves for the black pieces
        table_pos = []
        old_new_piece_pos = []

        # board position before move
        board = self.blank_board.copy()
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l

        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player-1].pos:
            old_piece_pos = v

            step_pos = [(v[0]+1, v[1]-1), (v[0]+1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B","W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j))
                    else:
                        old_new_piece_pos.append((old_piece_pos,n))

        # board position after  move

        for i,j in old_new_piece_pos:
            b = board.copy()
            b[i[0], i[1]] = 0
            b[j[0], j[1]] = "B"
            table_pos.append(b)
            assert len(np.where(b != 0)[0]) == 16, f"In possible_moves_on_black_turn(), there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"

        self.board = board
        return table_pos

    def possible_moves(self):
    #checks the current player and returns a function that returns the possible moves for that player
        if self.current_player == 2:
            return self.possible_moves_on_black_turn()
        else:
            return self.possible_moves_on_white_turn()

    def get_piece_pos_from_table(self, table_pos):
    #returns the current positions of the pieces on the board
        if self.current_player-1 == 0:
            x = np.where(table_pos == "W")
        elif self.current_player-1 == 1:
            x = np.where(table_pos == "B")
        else:
            raise ValueError("There can be at most 2 players.")

        assert len(np.where(table_pos != 0)[0]) == 16, f"In get_piece_pos_from_table(), there are {len(np.where(table_pos != 0)[0])} pieces on the board  \n {table_pos}"
        return [(i,j) for i,j in zip(x[0], x[1])]

    def make_move(self, pos):
    #assigning the new positions of the pieces as the current positions

        # empty list that will hold new positions
        new_p1_pos = []
        new_p2_pos = []

        for i in range(8):
            for j in range(8):
                if pos[i,j] == "W":  #looking for piece 'W'
                    pos_tup=(i,j)
                    new_p1_pos.append(pos_tup)  #adding postion of piece 'W' to list
                if pos[i,j] == "B":  #looking for piece 'B'
                    pos_tup=(i,j)
                    new_p2_pos.append(pos_tup)  #adding postion of piece 'B' to list


        self.players[0].pos = new_p1_pos  #assigning new player positions for player 1
        self.players[1].pos = new_p2_pos  #assigning new player positions for player 2

        pass

    def lose(self):

        for i in range(8):
            if self.board[0,i]=="W": #checking to see if any white pieces are in the black territory
                return True
        for i in range(8):
            if self.board[7,i]=="B": #checking to see if any black pieces are in the white territory
                return True


    def is_over(self):
        #game is over if there are no possible moves or one of the players lose
        return (self.possible_moves() == []) or self.lose()


    def show(self):

        # board position before move
        board = self.blank_board.copy()
        print(f"player 1 positions = {self.players[0].pos}")
        print(f"player 2 positions = {self.players[1].pos}")
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l
        print('\n')
        #print(board)
        print(board.astype('str'))


    def scoring(self):
       """
       win = 0
       lose = -100
       """
       return -100 if self.lose() else 0
       pass



if __name__ == "__main__":
    ai = Negamax(1)
    ai2 = Negamax(4)
    game = Checker([Human_Player(), AI_Player(ai)])
    history = game.play()
    if game.lose(): #congratulate opposite player since switch_player() was called
        if game.current_player==1:
            print("\nPlayer 2 is crowned!!")
            print("Player 2 wins!!")
        else:
            print("\nPlayer 1 is crowned!!")
            print("Player 1 wins!!")
        print("\nGAME OVER!!\n")
    else: #draw
        print("Looks like we have a draw.")

    #game.play()
# questions:1 ends here

#AI_Player(ai)
#Human_Player()
#AI_Player(ai2)