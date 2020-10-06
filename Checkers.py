# Author - IIT2018032
# Question - Checkers game simulator using game trees (added alpha beta pruning)
# Version - Alpha prototype 2
# Features - AI vs AI mode + Human vs AI mode with 3 difficulty modes (for now)
# Pre-requisites - Python + Tkinter (for GUI)
# This one is done in python due to lines of code heuristics I had in my mind
# To run the code simply type python3 FILE_NAME.py on your terminal

"""
    Board values

    BLACK_NORMAL - For black checker (normal)
    RED_NORMAL   - For red checker (normal)
    BLACK_KING   - For black king checker
    RED_KING     - For red king checker
    EMPTY        - For empty space in board

    Board Rules
    # Standard 8 x 8 checkers rules (see report for detail)

    Initial Board

    BLACK_NORMAL  EMPTY         BLACK_NORMAL  EMPTY         BLACK_NORMAL  EMPTY         BLACK_NORMAL  EMPTY
    EMPTY         BLACK_NORMAL  EMPTY         BLACK_NORMAL  EMPTY         BLACK_NORMAL  EMPTY         BLACK_NORMAL
    BLACK_NORMAL  EMPTY         BLACK_NORMAL  EMPTY         BLACK_NORMAL  EMPTY         BLACK_NORMAL  EMPTY
    EMPTY         EMPTY         EMPTY         EMPTY         EMPTY         EMPTY         EMPTY         EMPTY
    EMPTY         EMPTY         EMPTY         EMPTY         EMPTY         EMPTY         EMPTY         EMPTY
    EMPTY         RED_NORMAL    EMPTY         RED_NORMAL    EMPTY         RED_NORMAL    EMPTY         RED_NORMAL
    RED_NORMAL    EMPTY         RED_NORMAL    EMPTY         RED_NORMAL    EMPTY         RED_NORMAL    EMPTY
    EMPTY         RED_NORMAL    EMPTY         RED_NORMAL    EMPTY         RED_NORMAL    EMPTY         RED_NORMAL

"""

# some useful imports
import copy as CLONE
import time
from tkinter import *
from tkinter import messagebox as MSG
import tkinter.font as TkFont


# main checkers menu GUI class
class main_GUI:

    # button handler function for playing AI vs AI mode
    def play_AIvsAI_OnAction(self):
        self.mainGUI.destroy()
        BOARD_DIMENSION = 8  # size of board (N x N)
        PLAYMODE = MODE.AI_vs_AI  # current playMode (Red AI vs Black AI)

        # for black AI improvement for more optimal moves
        lvl_of_Difficulty = DIFFICULTY.NORMAL if self.diffVar.get() == 'normal' else DIFFICULTY.HARD if self.diffVar.get() == 'hard' else DIFFICULTY.BOSS_LVL

        play_AIvsAI = playMode_GUI(BOARD_DIMENSION, PLAYMODE, lvl_of_Difficulty)
        play_AIvsAI.setInitials(PLAYMODE)
        play_AIvsAI.start_AIvsAI()

    # button handler function for playing H vs AI mode
    def play_HvsAI_OnAction(self):
        self.mainGUI.destroy()
        BOARD_DIMENSION = 8  # size of board (N x N)
        PLAYMODE = MODE.H_vs_AI  # current playMode (Human vs Black AI)

        # for black AI improvement for more optimal moves
        lvl_of_difficulty = DIFFICULTY.NORMAL if self.diffVar.get() == 'normal' else DIFFICULTY.HARD if self.diffVar.get() == 'hard' else DIFFICULTY.BOSS_LVL

        play_HvsAI = playMode_GUI(BOARD_DIMENSION, PLAYMODE, lvl_of_difficulty)
        play_HvsAI.setInitials(PLAYMODE)
        play_HvsAI.start_HvsAI()

    # button handler for exiting the game menu
    def quit_OnAction(self):
        self.mainGUI.destroy()

    # initializer function for main menu GUI
    def __init__(self):

        # sys.setrecursionlimit(1000)
        # print("Recursion limit = " + str(sys.getrecursionlimit()))

        # mainMenu GUI object
        self.mainGUI = Tk()
        self.mainGUI.configure(bg='black')

        # Main Frame
        self.mainFrame = Frame(self.mainGUI)
        self.mainFrame.configure(bg='black')
        self.mainFrame.pack()

        # Some custom fonts used
        titleFont = TkFont.Font(family='Helvetica', size=36, weight=TkFont.BOLD)
        buttonFont = TkFont.Font(family='Helvetica', size=12, weight=TkFont.BOLD)

        # Window dimensions
        windowWidth = 700
        windowHeight = 500

        # Screen dimensions
        scrWidth = self.mainGUI.winfo_screenwidth()
        scrHeight = self.mainGUI.winfo_screenheight()

        # To place the left corner of the window
        winX = (scrWidth / 2) - (windowWidth / 2)
        winY = (scrHeight / 2) - (windowHeight / 2)

        # Setting the location of the mainMenu Window on screen
        self.mainGUI.geometry(f'{windowWidth}x{windowHeight}+{int(winX)}+{int(winY)}')

        # Window Title
        self.mainGUI.title("CHECKERS MENU")

        # Game Title (I chose this title to make myself motivated to make this game)
        Label(self.mainFrame, text="HEHE BOII CHECKERS", pady=40, fg="white", bg='black', font=titleFont).pack()

        # Play Button (red AI vs black AI) (Primary)
        Button(self.mainFrame, text="Play AI vs AI", pady=15, padx=20, fg="yellow", bg='black',
                                        font=buttonFont, command=self.play_AIvsAI_OnAction).pack()

        # spacer to add space
        Label(self.mainFrame,text="spacer",bg='black',fg='black').pack()

        # Play Button (Human vs AI) (Secondary)
        Button(self.mainFrame, text="Play Human vs Ai", pady=15, padx=20, fg="blue",
                                       bg='black', font=buttonFont, command=self.play_HvsAI_OnAction).pack()

        # spacer to add space
        Label(self.mainFrame,text="spacer",bg='black',fg='black').pack()


        self.diffVar = StringVar()
        self.diffVar.set("normal")

        # some radios for difficulty settings
        Radiobutton(self.mainFrame, text="Normal", variable=self.diffVar,value="normal",bg='black',fg='green').pack()
        Radiobutton(self.mainFrame, text="Hard", variable=self.diffVar,value="hard",bg='black',fg='orange').pack()
        Radiobutton(self.mainFrame, text="BOSS_LVL", variable=self.diffVar,value="bossLvl",bg='black',fg='red').pack()

        # spacer to add space
        Label(self.mainFrame,text="spacer",bg='black',fg='black').pack()

        # Quit button at last
        self.QuitButton = Button(self.mainFrame, text="Wanna Quit", pady=15, padx=20, fg="red",
                                 bg='black', font=buttonFont, command=self.quit_OnAction)
        self.QuitButton.pack(side='bottom')


        # Start displaying
        self.mainGUI.mainloop()


# enum class for board elements
class BOARD_ELEMENT(enum.Enum):
    BLACK_KING = 1
    BLACK_NORMAL = 2
    RED_KING = 3
    RED_NORMAL = 4
    EMPTY = 5


# enum for players
class PLAYER(enum.Enum):
    RED = 1
    BLACK = 2
    HUMAN_1 = 3
    HUMAN_2 = 4


# for different playModes for checkers
class MODE(enum.Enum):
    AI_vs_AI = 1
    H_vs_AI = 2
    H_vs_H = 3  # not made


# for making game sessions for varying difficulty levels
class DIFFICULTY(enum.Enum):
    EASY = 1
    NORMAL = 2
    HARD = 4
    BOSS_LVL = 8


# for making possible movements SETS for king and normal checkers
class MOVE:

    def __init__(self, desc, x, y):
        self.tx = x
        self.ty = y
        self.description = desc

    def getX(self):
        return self.tx

    def getY(self):
        return self.ty

    def getDescription(self):
        return self.description


# Game Board State class
class GAME_STATE:

    def __init__(self, board=None):

        if board is None:
            self.status = "dead"
        else:
            self.status = "active"

        self.boardTiles = board
        self.staticScore = -1

    def getStatus(self):
        return self.status

    def setStaticScore(self, score):
        self.staticScore = score

    def getStaticScore(self):
        return self.staticScore

    def getBoardTiles(self):
        return self.boardTiles


class playMode_GUI:

    # playMode window parameters and other useful game parameters initialization
    def __init__(self, dimensions, mode, difficulty=DIFFICULTY.NORMAL):

        # Checkers border rows (for king formation)
        self.redBorder = 0
        self.blackBorder = 7

        # Move sets (Initially empty)
        self.blackMovements = []
        self.blackAtkMoves = []
        self.redMovements = []
        self.redAtkMoves = []
        self.kingMovements = []
        self.kingAtkMoves = []

        # Board dimensions
        self.dim = dimensions

        # Internal Board
        self.boardTiles = [[BOARD_ELEMENT.EMPTY for y in range(dimensions)] for x in range(dimensions)]
        self.makeInternalBoard()

        # playMode GUI object
        self.playGUI = Tk()
        self.playGUI.configure(bg='white')
        Grid.rowconfigure(self.playGUI, 0, weight=1)
        Grid.columnconfigure(self.playGUI, 0, weight=1)

        # Main Frame
        self.MainFrame = Frame(self.playGUI)
        self.MainFrame.grid(row=0, column=0, sticky=N + S + E + W)

        # GUI Board
        self.gBoard = [[Button(self.MainFrame) for x in range(dimensions)] for y in
                       range(dimensions)]

        # Window dimensions
        windowWidth = 850
        windowHeight = 850

        # Screen dimensions
        scrWidth = self.playGUI.winfo_screenwidth()
        scrHeight = self.playGUI.winfo_screenheight()

        # To place the left corner of the window
        winX = (scrWidth / 2) - (windowWidth / 2)
        winY = (scrHeight / 2) - (windowHeight / 2)

        # Setting the location of the mainMenu Window on screen
        self.playGUI.geometry(f'{windowWidth}x{windowHeight}+{int(winX)}+{int(winY)}')

        # Setting the difficulty parameter
        self.difficulty = difficulty
        print(f"Current difficulty = {self.difficulty.name}")

        # Window Title
        if mode == MODE.AI_vs_AI:
            self.playGUI.title("PLAYING CHECKERS AI vs AI")
        elif mode == MODE.H_vs_AI:
            self.playGUI.title("PLAYING CHECKERS H vs AI")
        elif mode == MODE.H_vs_H:
            self.playGUI.title("PLAYING CHECKERS H vs H")

        # Some extra parameters for these modes
        if mode == MODE.H_vs_H or mode == MODE.H_vs_AI:
            self.hasPlayed = False
            self.hasMarked = False
            self.isAttackReady = False
            self.lastMarkedChecker = [NONE, NONE]

    # makes the internal checkers board
    def makeInternalBoard(self):

        for i in range(3):
            for j in range(self.dim):
                if (i + j) % 2 == 0:
                    self.boardTiles[i][j] = BOARD_ELEMENT.BLACK_NORMAL

        for i in range(self.dim - 3, self.dim):
            for j in range(self.dim):
                if (i + j) % 2 == 0:
                    self.boardTiles[i][j] = BOARD_ELEMENT.RED_NORMAL


    # makes list of all possible moves for both red and black checkers
    def generateMoveSets(self):

        # black Movements
        self.blackMovements.append(MOVE("Bottom Diagonally Right", 1, 1))
        self.blackMovements.append(MOVE("Bottom Diagonally Left", 1, -1))

        # blackAtkMoves
        self.blackAtkMoves.append(MOVE("Atk BDR", 2, 2))
        self.blackAtkMoves.append(MOVE("Atk BDL", 2, -2))

        # redMovements
        self.redMovements.append(MOVE("Top Diagonally Right", -1, 1))
        self.redMovements.append(MOVE("Top Diagonally Left", -1, -1))

        # redAtkMoves
        self.redAtkMoves.append(MOVE("Atk TDR", -2, 2))
        self.redAtkMoves.append(MOVE("Atk TDL", -2, -2))

        # kingMovements
        self.kingMovements = self.blackMovements + self.redMovements

        # kingAtkMoves
        self.kingAtkMoves = self.blackAtkMoves + self.redAtkMoves

    # GUI board initialization function
    def setInitials(self, mode):

        self.generateMoveSets()

        for i in range(self.dim):
            Grid.rowconfigure(self.MainFrame, i, weight=1)
            for j in range(self.dim):
                Grid.columnconfigure(self.MainFrame, j, weight=1)

                if (i + j) % 2 == 0:
                    self.gBoard[i][j].configure(bg='white')
                else:
                    self.gBoard[i][j].configure(bg='green')

                if mode == MODE.H_vs_AI or mode == MODE.H_vs_H:
                    self.gBoard[i][j].configure(command=lambda row=i, col=j: self.onButtonClick_H1(row, col))

                self.gBoard[i][j].grid(row=i, column=j, sticky=N + S + E + W)

        for i in range(3):
            for j in range(self.dim):
                if (i + j) % 2 == 0:
                    self.gBoard[i][j].configure(bg='black', text="N")

        for i in range(self.dim - 3, self.dim, 1):
            for j in range(self.dim):
                if (i + j) % 2 == 0:
                    self.gBoard[i][j].configure(bg='red', text="N")

    # for printing the current state of internal checkers board
    def printBoard(self, board):
        for i in range(self.dim):
            for j in range(self.dim):
                if board[i][j] == BOARD_ELEMENT.RED_NORMAL:
                    print("RN ", end="")
                elif board[i][j] == BOARD_ELEMENT.BLACK_NORMAL:
                    print("BN ", end="")
                elif board[i][j] == BOARD_ELEMENT.BLACK_KING:
                    print("BK ", end="")
                elif board[i][j] == BOARD_ELEMENT.RED_KING:
                    print("RK ", end="")
                else:
                    print("E  ", end="")
            print("")

    # updates the GUI window
    def updater(self, sec):
        time.sleep(sec)
        self.playGUI.update_idletasks()
        self.playGUI.update()

    # checker function to check whether either of the player has won the game or not
    def checkForWin(self, board, human_Playing=False):
        redCount = 0
        blackCount = 0

        for i in range(self.dim):
            for j in range(self.dim):
                if board[i][j] == BOARD_ELEMENT.RED_NORMAL or board[i][j] == BOARD_ELEMENT.RED_KING:
                    redCount += 1
                if board[i][j] == BOARD_ELEMENT.BLACK_NORMAL or board[i][j] == BOARD_ELEMENT.BLACK_KING:
                    blackCount += 1

        if redCount == 0:
            if not human_Playing:
                self.showInformation("HEHE BOII", "Black AI BEATS the red AI")
            else:
                self.showInformation("HEHE BOII", "HEHE you lost by black AI")
            return True

        if blackCount == 0:
            if not human_Playing:
                self.showInformation("HEHE BOII", "Red AI BEATS the black AI")
            else:
                self.showInformation("HEHE BOII", "HEHE lucky you won against black AI")
            return True

        return False

    # kick starter function for playing AI vs AI mode
    def start_AIvsAI(self):

        movesPlayed = 0
        counter = 0
        delay = 1

        self.updater(0)
        while True:

            # red's turn
            if not self.redAI_Turn():
                self.showInformation("HEHE BOII", "No valid move left for red, BLACK won")
                break

            movesPlayed += 1

            # update for red's move
            self.updater(delay)

            # check if red won
            if self.checkForWin(self.boardTiles):
                break

            # black's turn
            if not self.blackAI_Turn():
                self.showInformation("HEHE BOII", "No valid move left for black, RED won")
                break

            movesPlayed += 1

            # update for black's move
            self.updater(delay)

            # check if black won
            if self.checkForWin(self.boardTiles):
                break

            counter += 1

        # print(f"MOVES PLAYED = {movesPlayed}")

    # kick starter function for playing human vs AI mode
    def start_HvsAI(self):

        movesPlayed = 0
        counter = 0
        delay = 1

        self.updater(0)
        while True:

            if self.miniMax(GAME_STATE(self.boardTiles), 0, 1, -99999, 99999, PLAYER.RED).getStatus() == 'dead':
                self.showInformation("HEHE BOII", "No valid move left for human(red), BLACK won")
                break

            self.human_Turn()
            movesPlayed += 1

            self.updater(delay)

            # check if human won
            if self.checkForWin(self.boardTiles, human_Playing=True):
                break

            if not self.blackAI_Turn():
                self.showInformation("HEHE BOII", "No valid move left for black, human(Red) won")
                break

            movesPlayed += 1

            self.updater(delay)

            # check if black AI won
            if self.checkForWin(self.boardTiles, human_Playing=True):
                break

            self.hasPlayed = False
            counter += 1

        # print(f"Moves played = {movesPlayed}")

    # makes a move for red AI
    def redAI_Turn(self):

        Inf = 99999
        nInf = -99999

        RED_MAX_DEPTH = 1  # this depth is fixed to see the difference in outcomes for various difficulty levels

        startNode = GAME_STATE(self.boardTiles)
        moveState = self.miniMax(startNode, 0, RED_MAX_DEPTH, nInf, Inf, PLAYER.RED)

        if moveState.getStatus() == "active":
            self.boardTiles = moveState.getBoardTiles()
            self.updateGBoard(self.boardTiles, PLAYER.RED)
            return True
        else:
            print("NO VALID MOVE FOR RED " + moveState.getStatus())
            return False

    # makes a move for black AI
    def blackAI_Turn(self):

        Inf = 99999
        nInf = -99999

        BLACK_MAX_DEPTH = self.difficulty.value

        startNode = GAME_STATE(self.boardTiles)
        moveState = self.miniMax(startNode, 0, BLACK_MAX_DEPTH, nInf, Inf, PLAYER.BLACK)

        if moveState.getStatus() == "active":
            self.boardTiles = moveState.getBoardTiles()
            self.updateGBoard(self.boardTiles, PLAYER.BLACK)
            return True
        else:
            print("NO VALID MOVE FOR BLACK " + moveState.getStatus())
            return False

    # for making a human move from user
    def human_Turn(self):

        self.hasPlayed = False
        while not self.hasPlayed:
            # Do nothing
            self.updater(0)

            # Update when that lazy human (that's me) has made a move
            if self.hasPlayed:
                print("Human played")
                self.updateGBoard(self.boardTiles, PLAYER.HUMAN_1)

    # posX and posY are indices of that button in that button grid (for human player only) (playing red checkers)
    # button handler for reading human moves (for human vs AI mode)
    def onButtonClick_H1(self, posX, posY):

        if self.hasMarked:

            # UN-mark the last checker and its highlighted possible moves
            if posX == self.lastMarkedChecker[0] and posY == self.lastMarkedChecker[1]:

                # For red normals
                if self.boardTiles[posX][posY] == BOARD_ELEMENT.RED_NORMAL:

                    # undo the highlights of all possible moves (for red normal checkers)
                    for mov in self.redAtkMoves + self.redMovements:
                        if 0 <= (posX + mov.getX()) < 8 and 0 <= (posY + mov.getY()) < 8:

                            if self.gBoard[posX + mov.getX()][posY + mov.getY()].cget('bg') == 'blue':
                                # color possible move => blue tile
                                # print('Coloring')
                                if (posX + mov.getX() + posY + mov.getY()) % 2 == 0:
                                    self.gBoard[posX + mov.getX()][posY + mov.getY()].configure(bg='white')
                                else:
                                    self.gBoard[posX + mov.getX()][posY + mov.getY()].configure(bg='green')

                                self.hasMarked = False

                # for red king checkers
                if self.boardTiles[posX][posY] == BOARD_ELEMENT.RED_KING:

                    # undo the highlights of all possible moves (for red king checkers)
                    for mov in self.kingAtkMoves + self.kingMovements:
                        if 0 <= (posX + mov.getX()) < 8 and 0 <= (posY + mov.getY()) < 8:

                            if self.gBoard[posX + mov.getX()][posY + mov.getY()].cget('bg') == 'blue':
                                # color possible move => blue tile
                                # print('Coloring')
                                if (posX + mov.getX() + posY + mov.getY()) % 2 == 0:
                                    self.gBoard[posX + mov.getX()][posY + mov.getY()].configure(bg='white')
                                else:
                                    self.gBoard[posX + mov.getX()][posY + mov.getY()].configure(bg='green')

                                self.hasMarked = False

                return

            else:

                if self.gBoard[posX][posY].cget('bg') == 'blue':

                    # For red normal
                    if self.boardTiles[self.lastMarkedChecker[0]][self.lastMarkedChecker[1]] == BOARD_ELEMENT.RED_NORMAL:

                        if not self.isAttackReady:
                            if posX != self.redBorder:
                                self.boardTiles[posX][posY] = BOARD_ELEMENT.RED_NORMAL
                            else:
                                self.boardTiles[posX][posY] = BOARD_ELEMENT.RED_KING

                            self.boardTiles[self.lastMarkedChecker[0]][self.lastMarkedChecker[1]] = BOARD_ELEMENT.EMPTY

                            self.lastMarkedChecker = [NONE, NONE]
                            self.hasMarked = False
                            self.hasPlayed = True
                        else:
                            if posX != self.redBorder:
                                self.boardTiles[posX][posY] = BOARD_ELEMENT.RED_NORMAL
                            else:
                                self.boardTiles[posX][posY] = BOARD_ELEMENT.RED_KING

                            self.boardTiles[int((self.lastMarkedChecker[0] + posX) / 2)][
                                int((self.lastMarkedChecker[1] + posY) / 2)] = BOARD_ELEMENT.EMPTY
                            self.boardTiles[self.lastMarkedChecker[0]][self.lastMarkedChecker[1]] = BOARD_ELEMENT.EMPTY

                            self.hasMarked = False
                            self.lastMarkedChecker = [NONE, NONE]
                            isStill_Attackable = False

                            for mov in self.redAtkMoves:
                                if 0 <= (posX + mov.getX()) < 8 and 0 <= (posY + mov.getY()) < 8:
                                    if self.boardTiles[posX + mov.getX()][
                                        posY + mov.getY()] == BOARD_ELEMENT.EMPTY and (
                                            self.boardTiles[posX + int(mov.getX() / 2)][
                                                posY + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_NORMAL or
                                            self.boardTiles[posX + int(mov.getX() / 2)][
                                                posY + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_KING):
                                        isStill_Attackable = True

                            if not isStill_Attackable:
                                self.hasPlayed = True
                                self.isAttackReady = False

                        return

                # For red king
                if self.boardTiles[self.lastMarkedChecker[0]][self.lastMarkedChecker[1]] == BOARD_ELEMENT.RED_KING:

                    if not self.isAttackReady:

                        self.boardTiles[posX][posY] = BOARD_ELEMENT.RED_KING
                        self.boardTiles[self.lastMarkedChecker[0]][self.lastMarkedChecker[1]] = BOARD_ELEMENT.EMPTY

                        self.lastMarkedChecker = [NONE, NONE]
                        self.hasMarked = False
                        self.hasPlayed = True
                    else:

                        self.boardTiles[posX][posY] = BOARD_ELEMENT.RED_KING
                        self.boardTiles[int((self.lastMarkedChecker[0] + posX) / 2)][
                            int((self.lastMarkedChecker[1] + posY) / 2)] = BOARD_ELEMENT.EMPTY
                        self.boardTiles[self.lastMarkedChecker[0]][self.lastMarkedChecker[1]] = BOARD_ELEMENT.EMPTY

                        # self.lastMarkedChecker = [posX, posY]
                        self.hasMarked = False
                        isStill_Attackable = False

                        for mov in self.kingAtkMoves:
                            if 0 <= (posX + mov.getX()) < 8 and 0 <= (posY + mov.getY()) < 8:
                                if self.boardTiles[posX + mov.getX()][posY + mov.getY()] == BOARD_ELEMENT.EMPTY and (
                                        self.boardTiles[posX + int(mov.getX() / 2)][
                                            posY + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_NORMAL or
                                        self.boardTiles[posX + int(mov.getX() / 2)][
                                            posY + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_KING):
                                    isStill_Attackable = True

                        if not isStill_Attackable:
                            self.lastMarkedChecker = [NONE, NONE]
                            self.hasPlayed = True
                            self.isAttackReady = False

                    return


        else:  # not marked yet

            # Red Normal (highlight possible moves from that selected piece)
            if self.gBoard[posX][posY].cget('bg') == 'red' and self.gBoard[posX][posY].cget('text') == 'N':

                self.isAttackReady = False
                # highlight all possible atk (for red normal checkers)
                for mov in self.redAtkMoves:
                    if 0 <= (posX + mov.getX()) < 8 and 0 <= (posY + mov.getY()) < 8:

                        if self.boardTiles[posX + mov.getX()][posY + mov.getY()] == BOARD_ELEMENT.EMPTY and (
                                self.boardTiles[posX + int(mov.getX() / 2)][
                                    posY + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_NORMAL or
                                self.boardTiles[posX + int(mov.getX() / 2)][
                                    posY + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_KING):
                            # color possible move => blue tile

                            self.gBoard[posX + mov.getX()][posY + mov.getY()].configure(bg='blue')
                            self.hasMarked = True
                            self.isAttackReady = True

                if not self.isAttackReady:
                    # highlight all possible moves (for normal red checkers)
                    for mov in self.redMovements:
                        if 0 <= (posX + mov.getX()) < 8 and 0 <= (posY + mov.getY()) < 8:

                            if self.boardTiles[posX + mov.getX()][posY + mov.getY()] == BOARD_ELEMENT.EMPTY:
                                # color possible move => blue tile
                                self.gBoard[posX + mov.getX()][posY + mov.getY()].configure(bg='blue')
                                self.hasMarked = True

                if self.hasMarked:
                    self.lastMarkedChecker = [posX, posY]

            elif self.gBoard[posX][posY].cget('bg') == 'red' and self.gBoard[posX][posY].cget('text') == 'K':

                self.isAttackReady = False
                # highlight all possible atk (for red normal checkers)
                for mov in self.kingAtkMoves:
                    if 0 <= (posX + mov.getX()) < 8 and 0 <= (posY + mov.getY()) < 8:

                        if self.boardTiles[posX + mov.getX()][posY + mov.getY()] == BOARD_ELEMENT.EMPTY and (
                                self.boardTiles[posX + int(mov.getX() / 2)][
                                    posY + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_NORMAL or
                                self.boardTiles[posX + int(mov.getX() / 2)][
                                    posY + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_KING):
                            # color possible move => blue tile
                            self.gBoard[posX + mov.getX()][posY + mov.getY()].configure(bg='blue')
                            self.hasMarked = True
                            self.isAttackReady = True

                if not self.isAttackReady:
                    # highlight all possible moves (for normal red checkers)
                    for mov in self.kingMovements:
                        if 0 <= (posX + mov.getX()) < 8 and 0 <= (posY + mov.getY()) < 8:

                            if self.boardTiles[posX + mov.getX()][posY + mov.getY()] == BOARD_ELEMENT.EMPTY:
                                # color possible move => blue tile
                                self.gBoard[posX + mov.getX()][posY + mov.getY()].configure(bg='blue')
                                self.hasMarked = True

                if self.hasMarked:
                    self.lastMarkedChecker = [posX, posY]

    # minimax function for computing optimal move
    def miniMax(self, state, depth, depthLimit, alpha, beta, player):
        if depth >= depthLimit:
            # Static score calculation
            score = self.computeStaticScore(state)
            state.setStaticScore(score)
            return state

        # PLAYER BLACK
        if player == PLAYER.BLACK:
            return self.traverseState(state, depth, depthLimit, alpha, beta, PLAYER.BLACK)
        else:  # for PLAYER RED
            return self.traverseState(state, depth, depthLimit, alpha, beta, PLAYER.RED)

    # checks if attack is possible for a specific player
    def isAttackingPossible(self, state, player):

        # print("checking if atk possible")
        currBoard = state.getBoardTiles()

        # Black normals will attack diagonally downwards
        if player == PLAYER.BLACK:

            for i in range(8):
                for j in range(8):

                    if currBoard[i][j] == BOARD_ELEMENT.BLACK_NORMAL:

                        for mov in self.blackAtkMoves:
                            if 0 <= (i + mov.getX()) < 8 and 0 <= (j + mov.getY()) < 8:
                                if (currBoard[i + int(mov.getX() / 2)][
                                        j + int(mov.getY() / 2)] == BOARD_ELEMENT.RED_NORMAL or
                                    currBoard[i + int(mov.getX() / 2)][
                                        j + int(mov.getY() / 2)] == BOARD_ELEMENT.RED_KING) and \
                                        currBoard[i + mov.getX()][j + mov.getY()] == BOARD_ELEMENT.EMPTY:
                                    return True

                    if currBoard[i][j] == BOARD_ELEMENT.BLACK_KING:

                        for mov in self.kingAtkMoves:
                            if 0 <= (i + mov.getX()) < 8 and 0 <= (j + mov.getY()) < 8:
                                if (currBoard[i + int(mov.getX() / 2)][
                                        j + int(mov.getY() / 2)] == BOARD_ELEMENT.RED_NORMAL or
                                    currBoard[i + int(mov.getX() / 2)][
                                        j + int(mov.getY() / 2)] == BOARD_ELEMENT.RED_KING) and \
                                        currBoard[i + mov.getX()][j + mov.getY()] == BOARD_ELEMENT.EMPTY:
                                    return True


        else:  # RED normals will attack diagonally upwards
            for i in range(8):
                for j in range(8):

                    if currBoard[i][j] == BOARD_ELEMENT.RED_NORMAL:

                        for mov in self.redAtkMoves:
                            if 0 <= (i + mov.getX()) < 8 and 0 <= (j + mov.getY()) < 8:  # BOTTOM RIGHT
                                if (currBoard[i + int(mov.getX() / 2)][
                                        j + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_NORMAL or
                                    currBoard[i + int(mov.getX() / 2)][
                                        j + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_KING) and \
                                        currBoard[i + mov.getX()][j + mov.getY()] == BOARD_ELEMENT.EMPTY:
                                    return True

                    if currBoard[i][j] == BOARD_ELEMENT.RED_KING:

                        for mov in self.kingAtkMoves:
                            if 0 <= (i + mov.getX()) < 8 and 0 <= (j + mov.getY()) < 8:  # BOTTOM RIGHT
                                if (currBoard[i + int(mov.getX() / 2)][
                                        j + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_NORMAL or
                                    currBoard[i + int(mov.getX() / 2)][
                                        j + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_KING) and \
                                        currBoard[i + mov.getX()][j + mov.getY()] == BOARD_ELEMENT.EMPTY:
                                    return True

        return False

    # helper function for minimax
    def traverseState(self, state, depth, depthLimit, alpha, beta, player):

        currBoard = state.getBoardTiles()
        bState = GAME_STATE()

        # For max player (Black AI)
        if player == PLAYER.BLACK:

            bestScore = -99999
            if self.isAttackingPossible(state, player):
                # Attacking moves here
                for i in range(self.dim):
                    for j in range(self.dim):
                        if currBoard[i][j] == BOARD_ELEMENT.BLACK_NORMAL or currBoard[i][j] == BOARD_ELEMENT.BLACK_KING:

                            newState = self.isAttacking_BlackChecker(currBoard, i, j, depth, depthLimit, alpha, beta)

                            if newState.getBoardTiles() == currBoard:
                                continue

                            s = self.miniMax(newState, depth + 1, depthLimit, alpha, beta, PLAYER.RED)

                            if s.getStatus() == "dead":
                                bState = newState
                            else:
                                if s.getStaticScore() > bestScore:
                                    # print("for black atk updates ")
                                    bestScore = s.getStaticScore()
                                    bState = newState

                        if alpha < bestScore:
                            alpha = bestScore

                        if beta <= alpha:
                            return bState

            else:
                # Movement moves here
                for i in range(self.dim):
                    for j in range(self.dim):
                        # print("Inside loop")
                        if currBoard[i][j] == BOARD_ELEMENT.BLACK_NORMAL or currBoard[i][j] == BOARD_ELEMENT.BLACK_KING:
                            # print("passed condition")
                            newState = self.isMovable_BlackChecker(currBoard, i, j, depth, depthLimit, alpha, beta)

                            if newState.getStatus() == "dead":
                                continue

                            if newState.getStaticScore() > bestScore:
                                bestScore = newState.getStaticScore()
                                bState = newState

                        if alpha < bestScore:
                            alpha = bestScore

                        if beta <= alpha:
                            return bState

            return bState

        else:  # For min player (Red AI)

            bestScore = 99999
            if self.isAttackingPossible(state, player):

                # Attacking moves here
                for i in range(self.dim):
                    for j in range(self.dim):

                        if currBoard[i][j] == BOARD_ELEMENT.RED_NORMAL or currBoard[i][j] == BOARD_ELEMENT.RED_KING:

                            newState = self.isAttacking_RedChecker(currBoard, i, j, depth, depthLimit, alpha, beta)
                            if newState.getBoardTiles() == currBoard:
                                continue

                            s = self.miniMax(newState, depth + 1, depthLimit, alpha, beta, PLAYER.BLACK)

                            if s.getStatus() == "dead":
                                bState = newState
                            else:
                                if s.getStaticScore() < bestScore:
                                    # print("for red atk updates ")
                                    bestScore = s.getStaticScore()
                                    bState = newState

                        if beta > bestScore:
                            beta = bestScore

                        if beta <= alpha:
                            return bState

            else:
                # Movement moves here
                for i in range(self.dim):
                    for j in range(self.dim):

                        if currBoard[i][j] == BOARD_ELEMENT.RED_NORMAL or currBoard[i][j] == BOARD_ELEMENT.RED_KING:

                            newState = self.isMovable_RedChecker(currBoard, i, j, depth, depthLimit, alpha, beta)
                            if newState.getStatus() == "dead":
                                continue

                            if newState.getStaticScore() < bestScore:
                                bestScore = newState.getStaticScore()
                                bState = newState

                        if beta > bestScore:
                            beta = bestScore

                        if beta <= alpha:
                            return bState

            return bState

    # For Movements
    def isMovable_BlackChecker(self, currBoard, i, j, depth, depthLimit, alpha, beta):

        # Updated n[] working
        if currBoard[i][j] == BOARD_ELEMENT.BLACK_NORMAL:

            best = GAME_STATE()
            bstScore = -99999

            for mov in self.blackMovements:

                if self.dim > (i + mov.getX()) >= 0 and self.dim > (j + mov.getY()) >= 0:

                    if currBoard[i + mov.getX()][j + mov.getY()] == BOARD_ELEMENT.EMPTY:
                        newBoard = CLONE.deepcopy(currBoard)

                        if (i + mov.getX()) != self.blackBorder:
                            newBoard[i + mov.getX()][j + mov.getY()] = BOARD_ELEMENT.BLACK_NORMAL
                        else:
                            newBoard[i + mov.getX()][j + mov.getY()] = BOARD_ELEMENT.BLACK_KING

                        newBoard[i][j] = BOARD_ELEMENT.EMPTY

                        # NEW GAME_STATE
                        newState = GAME_STATE(newBoard)
                        s = self.miniMax(newState, depth + 1, depthLimit, alpha, beta, PLAYER.RED)

                        if s.getStatus() == "dead":
                            continue

                        newState.setStaticScore(s.getStaticScore())
                        if bstScore < s.getStaticScore():
                            best = newState
                            bstScore = s.getStaticScore()

                        if alpha < bstScore:
                            alpha = bstScore

                        if beta <= alpha:
                            break


        else:  # Black King + Updated n[] working not verified

            best = GAME_STATE()
            bstScore = -99999

            for mov in self.kingMovements:

                if self.dim > (i + mov.getX()) >= 0 and self.dim > (j + mov.getY()) >= 0:

                    if currBoard[i + mov.getX()][j + mov.getY()] == BOARD_ELEMENT.EMPTY:
                        newBoard = CLONE.deepcopy(currBoard)

                        # MOVING PIECE
                        newBoard[i + mov.getX()][j + mov.getY()] = BOARD_ELEMENT.BLACK_KING
                        newBoard[i][j] = BOARD_ELEMENT.EMPTY

                        # NEW GAME_STATE
                        newState = GAME_STATE(newBoard)
                        s = self.miniMax(newState, depth + 1, depthLimit, alpha, beta, PLAYER.RED)

                        if s.getStatus() == "dead":
                            continue

                        newState.setStaticScore(s.getStaticScore())
                        if bstScore < s.getStaticScore():
                            best = newState
                            bstScore = s.getStaticScore()

                        if alpha < bstScore:
                            alpha = bstScore

                        if beta <= alpha:
                            break

        return best

    def isMovable_RedChecker(self, currBoard, i, j, depth, depthLimit, alpha, beta):  # Diagonally Up - normal

        # Updated n[] working
        if currBoard[i][j] == BOARD_ELEMENT.RED_NORMAL:

            best = GAME_STATE()
            bstScore = 99999

            for mov in self.redMovements:

                if self.dim > (i + mov.getX()) >= 0 and self.dim > (j + mov.getY()) >= 0:

                    if currBoard[i + mov.getX()][j + mov.getY()] == BOARD_ELEMENT.EMPTY:
                        newBoard = CLONE.deepcopy(currBoard)

                        if (i + mov.getX()) != self.redBorder:
                            newBoard[i + mov.getX()][j + mov.getY()] = BOARD_ELEMENT.RED_NORMAL
                        else:
                            newBoard[i + mov.getX()][j + mov.getY()] = BOARD_ELEMENT.RED_KING

                        newBoard[i][j] = BOARD_ELEMENT.EMPTY

                        # NEW GAME_STATE
                        newState = GAME_STATE(newBoard)
                        s = self.miniMax(newState, depth + 1, depthLimit, alpha, beta, PLAYER.BLACK)

                        if s.getStatus() == "dead":
                            continue

                        newState.setStaticScore(s.getStaticScore())
                        if bstScore > s.getStaticScore():
                            best = newState
                            bstScore = s.getStaticScore()

                        if beta > bstScore:
                            beta = bstScore

                        if beta <= alpha:
                            break


        else:  # Red King + Updated n[] working not verified

            best = GAME_STATE()
            bstScore = 99999

            for mov in self.kingMovements:

                if self.dim > (i + mov.getX()) >= 0 and self.dim > (j + mov.getY()) >= 0:

                    if currBoard[i + mov.getX()][j + mov.getY()] == BOARD_ELEMENT.EMPTY:
                        newBoard = CLONE.deepcopy(currBoard)

                        # MOVING PIECE
                        newBoard[i + mov.getX()][j + mov.getY()] = BOARD_ELEMENT.RED_KING
                        newBoard[i][j] = BOARD_ELEMENT.EMPTY

                        # NEW GAME_STATE
                        newState = GAME_STATE(newBoard)
                        s = self.miniMax(newState, depth + 1, depthLimit, alpha, beta, PLAYER.BLACK)

                        if s.getStatus() == "dead":
                            continue

                        newState.setStaticScore(s.getStaticScore())
                        if bstScore > s.getStaticScore():
                            best = newState
                            bstScore = s.getStaticScore()

                        if beta > bstScore:
                            beta = bstScore

                        if beta <= alpha:
                            break

        return best

    # For Attacking
    def isAttacking_BlackChecker(self, currBoard, i, j, depth, depthLimit, alpha, beta):

        # Removed n[] working
        if currBoard[i][j] == BOARD_ELEMENT.BLACK_NORMAL:

            best = GAME_STATE()
            bstScore = -99999

            for mov in self.blackAtkMoves:

                if self.dim > (i + mov.getX()) >= 0 and self.dim > (j + mov.getY()) >= 0:

                    if currBoard[i + mov.getX()][j + mov.getY()] == BOARD_ELEMENT.EMPTY and (
                            currBoard[i + int(mov.getX() / 2)][j + int(mov.getY() / 2)] == BOARD_ELEMENT.RED_NORMAL or
                            currBoard[i + int(mov.getX() / 2)][j + int(mov.getY() / 2)] == BOARD_ELEMENT.RED_KING):
                        newBoard = CLONE.deepcopy(currBoard)

                        if (i + mov.getX()) != self.blackBorder:
                            newBoard[i + mov.getX()][j + mov.getY()] = BOARD_ELEMENT.BLACK_NORMAL
                        else:
                            newBoard[i + mov.getX()][j + mov.getY()] = BOARD_ELEMENT.BLACK_KING

                        newBoard[i + int(mov.getX() / 2)][j + int(mov.getY() / 2)] = BOARD_ELEMENT.EMPTY
                        newBoard[i][j] = BOARD_ELEMENT.EMPTY

                        s = self.isAttacking_BlackChecker(newBoard, i + mov.getX(), j + mov.getY(), depth, depthLimit,
                                                          alpha, beta)

                        if s.getStatus() == "dead":
                            continue

                        if bstScore < s.getStaticScore():
                            best = s
                            bstScore = s.getStaticScore()

                        if alpha < bstScore:
                            alpha = bstScore

                        if beta <= alpha:
                            break

            if best.getStatus() == "dead":
                best = GAME_STATE(currBoard)
                best.setStaticScore(self.computeStaticScore(best))

        else:  # Black King + Removed n[] working not verified

            best = GAME_STATE()
            bstScore = -99999

            for mov in self.kingAtkMoves:

                if self.dim > (i + mov.getX()) >= 0 and self.dim > (j + mov.getY()) >= 0:

                    if currBoard[i + mov.getX()][j + mov.getY()] == BOARD_ELEMENT.EMPTY and (
                            currBoard[i + int(mov.getX() / 2)][j + int(mov.getY() / 2)] == BOARD_ELEMENT.RED_NORMAL or
                            currBoard[i + int(mov.getX() / 2)][j + int(mov.getY() / 2)] == BOARD_ELEMENT.RED_KING):
                        newBoard = CLONE.deepcopy(currBoard)

                        # ATTACKING PIECE
                        newBoard[i + mov.getX()][j + mov.getY()] = BOARD_ELEMENT.BLACK_KING
                        newBoard[i + int(mov.getX() / 2)][j + int(mov.getY() / 2)] = BOARD_ELEMENT.EMPTY
                        newBoard[i][j] = BOARD_ELEMENT.EMPTY

                        s = self.isAttacking_BlackChecker(newBoard, i + mov.getX(), j + mov.getY(), depth, depthLimit,
                                                          alpha, beta)

                        if s.getStatus() == "dead":
                            continue

                        if bstScore < s.getStaticScore():
                            best = s
                            bstScore = s.getStaticScore()

                        if alpha < bstScore:
                            alpha = bstScore

                        if beta <= alpha:
                            break

            if best.getStatus() == "dead":
                best = GAME_STATE(currBoard)
                best.setStaticScore(self.computeStaticScore(best))

        return best

    def isAttacking_RedChecker(self, currBoard, i, j, depth, depthLimit, alpha, beta):

        # Removed n[] working
        if currBoard[i][j] == BOARD_ELEMENT.RED_NORMAL:

            best = GAME_STATE()
            bstScore = 99999

            for mov in self.redAtkMoves:

                if self.dim > (i + mov.getX()) >= 0 and self.dim > (j + mov.getY()) >= 0:

                    if currBoard[i + mov.getX()][j + mov.getY()] == BOARD_ELEMENT.EMPTY and (
                            currBoard[i + int(mov.getX() / 2)][j + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_NORMAL or
                            currBoard[i + int(mov.getX() / 2)][j + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_KING):
                        newBoard = CLONE.deepcopy(currBoard)

                        if (i + mov.getX()) != self.redBorder:
                            newBoard[i + mov.getX()][j + mov.getY()] = BOARD_ELEMENT.RED_NORMAL
                        else:
                            newBoard[i + mov.getX()][j + mov.getY()] = BOARD_ELEMENT.RED_KING

                        newBoard[i + int(mov.getX() / 2)][j + int(mov.getY() / 2)] = BOARD_ELEMENT.EMPTY
                        newBoard[i][j] = BOARD_ELEMENT.EMPTY

                        # NEW BOARD
                        s = self.isAttacking_RedChecker(newBoard, i + mov.getX(), j + mov.getY(), depth, depthLimit,
                                                        alpha, beta)
                        if s.getStatus() == "dead":
                            continue

                        if bstScore > s.getStaticScore():
                            best = s
                            bstScore = s.getStaticScore()

                        if beta > bstScore:
                            beta = bstScore

                        if beta <= alpha:
                            break

            if best.getStatus() == "dead":
                best = GAME_STATE(currBoard)
                best.setStaticScore(self.computeStaticScore(best))

        else:  # Red King + Removed n[] working not verified

            best = GAME_STATE()
            bstScore = 99999

            for mov in self.kingAtkMoves:

                if self.dim > (i + mov.getX()) >= 0 and self.dim > (j + mov.getY()) >= 0:

                    if currBoard[i + mov.getX()][j + mov.getY()] == BOARD_ELEMENT.EMPTY and (
                            currBoard[i + int(mov.getX() / 2)][j + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_NORMAL or
                            currBoard[i + int(mov.getX() / 2)][j + int(mov.getY() / 2)] == BOARD_ELEMENT.BLACK_KING):
                        newBoard = CLONE.deepcopy(currBoard)

                        # ATTACKING PIECE
                        newBoard[i + mov.getX()][j + mov.getY()] = BOARD_ELEMENT.RED_KING
                        newBoard[i + int(mov.getX() / 2)][j + int(mov.getY() / 2)] = BOARD_ELEMENT.EMPTY
                        newBoard[i][j] = BOARD_ELEMENT.EMPTY

                        # NEW BOARD
                        s = self.isAttacking_RedChecker(newBoard, i + mov.getX(), j + mov.getY(), depth, depthLimit,
                                                        alpha, beta)

                        if s.getStatus() == "dead":
                            continue

                        if bstScore > s.getStaticScore():
                            best = s
                            bstScore = s.getStaticScore()

                        if beta > bstScore:
                            beta = bstScore

                        if beta <= alpha:
                            break

            if best.getStatus() == "dead":
                best = GAME_STATE(currBoard)
                best.setStaticScore(self.computeStaticScore(best))

        return best

    # end state scoring heuristics
    def computeStaticScore(self, state):
        # Scoring parameters
        NORMAL_PIECE_WEIGHT = 300
        KING_PIECE_WEIGHT = 600

        # for count score
        nRedPieces = 0
        nBlackPieces = 0
        nRedKings = 0
        nBlackKings = 0

        # for tile score
        redTileScore = 0
        blackTileScore = 0
        tileConstant = 0.5 if self.dim % 2 == 0 else 0
        mid_x = (self.dim - 1) / 2
        mid_y = (self.dim - 1) / 2

        # for distance score
        redDistanceScore = 0
        blackDistanceScore = 0

        currBoard = state.getBoardTiles()
        for i in range(self.dim):
            for j in range(self.dim):
                if currBoard[i][j] == BOARD_ELEMENT.RED_NORMAL:
                    nRedPieces += 1    # count score
                    redTileScore += int(max(abs(mid_x - i),abs(mid_y - j)) + tileConstant)  # tile score
                    redDistanceScore += self.dim - i   # dist score

                elif currBoard[i][j] == BOARD_ELEMENT.RED_KING:
                    nRedKings += 1     # count score
                    redTileScore += int(max(abs(mid_x - i),abs(mid_y - j)) + tileConstant)  # tile score
                    redDistanceScore += self.dim - i   # dist score

                elif currBoard[i][j] == BOARD_ELEMENT.BLACK_KING:
                    nBlackKings += 1   # count score
                    blackTileScore += int(max(abs(mid_x - i),abs(mid_y - j)) + tileConstant)  # tile score
                    blackDistanceScore += i + 1   # dist score

                elif currBoard[i][j] == BOARD_ELEMENT.BLACK_NORMAL:
                    nBlackPieces += 1  # count score
                    blackTileScore += int(max(abs(mid_x - i),abs(mid_y - j)) + tileConstant)  # tile score
                    blackDistanceScore += i + 1   # dist score


        tileScore = blackTileScore
        distanceScore = blackDistanceScore
        countScore = NORMAL_PIECE_WEIGHT * (nBlackPieces - nRedPieces) + KING_PIECE_WEIGHT * (nBlackKings - nRedKings)

        # for black AI (max) and for red AI (min)
        score = tileScore + distanceScore + countScore
        return score

    # for updating the GUI board
    def updateGBoard(self, board, player):

        if player == PLAYER.RED:
            print("Updating for red player")
        elif player == PLAYER.BLACK:
            print("Updating for black player")
        else:
            print("Updating for Human")

        for i in range(self.dim):
            for j in range(self.dim):

                if board[i][j] == BOARD_ELEMENT.EMPTY:
                    if (i + j) % 2 == 0:
                        self.gBoard[i][j].configure(bg='white', text="")
                    else:
                        self.gBoard[i][j].configure(bg='green', text="")
                elif board[i][j] == BOARD_ELEMENT.RED_NORMAL:
                    self.gBoard[i][j].configure(bg='red', text="N")
                elif board[i][j] == BOARD_ELEMENT.RED_KING:
                    self.gBoard[i][j].configure(bg='red', text="K")
                elif board[i][j] == BOARD_ELEMENT.BLACK_NORMAL:
                    self.gBoard[i][j].configure(bg='black', text="N")
                elif board[i][j] == BOARD_ELEMENT.BLACK_KING:
                    self.gBoard[i][j].configure(bg='black', text="K")

    # for displaying messages to the user
    def showInformation(self, title, info):
        MSG.showinfo(title, info)
        return


if __name__ == "__main__":

    # load the main menu of the game
    mainMenu = main_GUI()
