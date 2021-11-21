#####################################################################-
#                    Tic Tac Toe with MinMax
# 
#           Copyright (C) 2010 By Ulrik Hørlyk Hjort
#
#  This Program is Free Software; You Can Redistribute It and/or
#  Modify It Under The Terms of The GNU General Public License
#  As Published By The Free Software Foundation; Either Version 2
#  of The License, or (at Your Option) Any Later Version.
#
#  This Program is Distributed in The Hope That It Will Be Useful,
#  But WITHOUT ANY WARRANTY; Without Even The Implied Warranty of
#  MERCHANTABILITY or FITNESS for A PARTICULAR PURPOSE.  See The
#  GNU General Public License for More Details.
#
# You Should Have Received A Copy of The GNU General Public License
# Along with This Program; if not, See <Http://Www.Gnu.Org/Licenses/>.
#######################################################################
import random
import numpy as np
from random import randrange

###########################################################
#
# Game class
#
###########################################################
class Game:

        X = 1
        O = -1

        ###################################################
        #
        #
        ###################################################
        def __init__(self):
                self.initGame()
                self.EMPTY = 0
                
        ###################################################
        #
        #
        ###################################################
        def initGame(self):
                self.board = [0]*9

        ###################################################
        #
        # Returns list with all valid moves == all empty sqoares 
        #
        ###################################################
        def getValidMoves(self):
                moves = []
                for i in range (9):
                        if self.board[i] == self.EMPTY:
                                moves.append(i)
                return moves

        ###################################################
        #
        #
        ###################################################
        def isMoves(self):
                return (self.EMPTY in self.board)


        ###################################################
        #
        #
        ###################################################
        def isBoardEmpty(self):
                if self.board.count(self.EMPTY) == 9:
                        return True
                return False
                

        ###################################################
        #
        # Evaluate boaedposition for winning position 
        # for the given color
        #
        ###################################################
        def isWin(self, color):         
                if ((self.board[0] == self.board[1] == self.board[2] == color) or
                        (self.board[3] == self.board[4] == self.board[5] == color) or
                        (self.board[6] == self.board[7] == self.board[8] == color) or
                        (self.board[0] == self.board[3] == self.board[6] == color) or
                        (self.board[1] == self.board[4] == self.board[7] == color) or
                        (self.board[2] == self.board[5] == self.board[8] == color) or
                        (self.board[0] == self.board[4] == self.board[8] == color) or
                        (self.board[2] == self.board[4] == self.board[6] == color)):
                                return True
                return False

        ###################################################
        #
        # Plot currebt board position
        #
        ###################################################
        def plotBoard(self):            
                for i in range(9):
                        if i%3 == 0:
                                print()

                        if self.board[i] == self.X:
                                print("X ", end = '')
                        elif self.board[i] == self.O:
                                print("O ", end = '')
                        else:
                                print("  ", end = '')
                print()
                print("----------------------")


###########################################################
#
# Player base class
#
###########################################################
class Player:

        ###################################################
        #
        #
        ###################################################    
        def __init__(self, color):
                self.color = color

        ###################################################
        #
        #
        ###################################################
        def swapColor(self, color):
                return (color*-1)

        ###################################################
        #
        #
        ###################################################
        def getColor(self):
                return self.color

        ###################################################
        #
        #
        ###################################################
        def move(self, game):
                raise NotImplementedError()


###################################################
#
# Human player class
#
###################################################
class PlayerHuman(Player):
        ###################################################
        #
        #
        ###################################################
        def __init__(self, color):
                super().__init__(color)

        ###################################################
        #
        #
        ###################################################
        def info(self):
                print("012")
                print("345")
                print("678")                

        ###################################################
        #
        #
        ###################################################                
        def move(self, game):
                move = -1
                while (move not in game.getValidMoves()):
                        valid = game.getValidMoves()
                        move = int(input("Enter move: %s " % str(tuple(valid))))
                        if move not in valid:
                                print("Invalid move: %d" % move)
                game.board[move] = self.color
                
                if (game.isWin(self.color)):
                        return True        

###########################################################
#
# Random computer player class
#
###########################################################
class PlayerRandom(Player):
        def __init__(self, color):
                super().__init__(color)

        ###################################################
        #
        # Make random valid move
        #
        ###################################################
        def move(self, game):
                if (game.isWin(self.swapColor(self.color))):
                        return True

                game.board[random.choice(game.getValidMoves())] = self.color

                if (game.isWin(self.color)):
                        return True

###########################################################
#
# Minmax computer player class
#
###########################################################
class PlayerMinMax(Player):
        ###################################################
        #
        #
        ###################################################
        def __init__(self, color):
                super().__init__(color)

        ###################################################
        #
        # Minmax 
        #
        ###################################################        
        def minmax(self, game, color):
                validMoves = game.getValidMoves()
       
                if game.isWin(self.swapColor(color)): # Was previous move a winning move ? 
                        # If last move was a winning move return score 
                        # Positive score for "us" (maximize) (1*1*moves or -1*-1*moves), 
                        # negative score for "them" (minimize) (1*-1*moves or -1*1*moves)
                        bonus = 0 if color==self.color else 0
                        return [((color * self.swapColor(self.color)) * (len(validMoves) +1))+bonus,-1]
                elif len(validMoves) == 0:
                        return [0,-1]   

                scoreAndMove = [-np.inf if color == self.color else np.inf, -1]
                
                for move in validMoves:
                        game.board[move] = color
                        returnedScoreAndMove = self.minmax(game, self.swapColor(color))                        
                        game.board[move] = game.EMPTY 

                        returnedScoreAndMove[1]=move

                        # Maximize/minimize
                        if color == self.color: # Maximize "our" move                         
                                if returnedScoreAndMove[0] > scoreAndMove[0]:
                                        scoreAndMove = returnedScoreAndMove                                        
                        else: # Minimize "their" move                         
                                if returnedScoreAndMove[0] < scoreAndMove[0]:
                                        scoreAndMove = returnedScoreAndMove

                return scoreAndMove
                
        ###################################################
        #
        # Make minmax move
        #
        ###################################################
        def move(self, game):
                if game.isBoardEmpty(): # if board is empty make random first move
                        game.board[random.choice(game.getValidMoves())] = self.color
                else: 
                        move = self.minmax(game, self.color)
                        if (move[1] == -1):
                                return True
                        game.board[move[1]] = self.color
                return False

##################################################################################################

###################################################
#
# Play game
#
###################################################
def playGame(game, players):  
        activePlayer = 0

        while (True):   
                if (not game.isMoves()):                        
                        return 0
                
                if players[activePlayer].move(game):                    
                        return players[activePlayer].getColor()
                activePlayer = (activePlayer + 1) % 2
                game.plotBoard()

###################################################
#
# Run game configuration
#
###################################################
def run(games=1000, gameConfiguration = [PlayerMinMax(Game.X),PlayerMinMax(Game.O)]):
        x = 0
        o = 0
        d = 0
        game = Game()
        for i in range(games):
                game.initGame()
                res = playGame(game, gameConfiguration)

                if game.isWin(game.X):
                        print("X")
                        x+=1
                elif game.isWin(game.O):
                        print("O")
                        o+=1
                else:
                        print("D")                      
                        d+=1
                game.plotBoard()

        print(x,o,d) 


###################################################
#
# Initialize game(s)
#
###################################################
def initGame():
    print("Players: ")
    print("1. Human")
    print("2. Random move computer")
    print("3. Minmax move computer")

    playerList = []
    for p,g in zip(["one","two"], [Game.X, Game.O]):
        pp = int(input("Enter player %s:" % p))
        if not pp in [1,2,3]:
          assert False, "Choose 1,2 or 3"
        playerList.append([PlayerHuman(g), PlayerRandom(g), PlayerMinMax(g)][pp-1])

    games = int(input("Enter number of games:"))
    run(games, playerList)


###################################################
#
# Main
#
###################################################

def main():
    #run(10, [PlayerMinMax(Game.X),PlayerHuman(Game.O)])
    #run(10, [PlayerHuman(Game.X),PlayerMinMax(Game.O)])                
    #run(10, [PlayerMinMax(Game.X),PlayerRandom(Game.O)])
    #run(10, [PlayerRandom(Game.X),PlayerMinMax(Game.O)])
    #run(10, [PlayerMinMax(Game.X),PlayerMinMax(Game.O)])
    #run(10)
    initGame()


if __name__ == "__main__":
    main()