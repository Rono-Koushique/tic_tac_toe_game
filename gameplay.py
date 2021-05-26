import pygame
import sys
import numpy as np
import random
import gridClickMapper
import computerLogic

color_DARKORANGE = (184, 85, 56)
color_DARKERORANGE = (118, 46, 25)
color_BACKGROUND = (228, 101, 63)
color_SCOREBOARDTEXT = (118, 45, 24)
color_BLACK = (0, 0, 0)
color_WHITE = (255, 255, 255)

img_CROSS = pygame.image.load("resources/images/cross.png")
img_CIRCLE = pygame.image.load("resources/images/circle.png")


def selectRandom(array):
    randomIdx = random.randint(0, len(array) - 1)
    return array[randomIdx]

# main gameplay class
class Gameplay(object):
    def __init__(self, screen):
        self.screen = screen
        self.board = np.zeros((3, 3))
        self.mapGrid = {(0, 0): (140, 100), (0, 1): (270, 100), (0, 2): (400, 100),
                        (1, 0): (140, 230), (1, 1): (270, 230), (1, 2): (400, 230),
                        (2, 0): (140, 360), (2, 1): (270, 360), (2, 2): (400, 360)}

        screen.fill((228, 101, 63))
        self.drawGrid()

    def insertMark(self, digit, x, y):
        if not self.spaceIsFree(x, y):
            return False
        self.board[x][y] = digit
        return True

    def spaceIsFree(self, x, y):
        return self.board[x][y] == 0

    def checkForWin(self):
        for digit in [1, 2]:
            if computerLogic.isWinner(self.board, digit):
                return digit
        return 0

    def drawGrid(self):
        pygame.draw.rect(self.screen, color_DARKORANGE, (140, 220, 380, 10))  # horizontal
        pygame.draw.rect(self.screen, color_DARKORANGE, (140, 350, 380, 10))
        pygame.draw.rect(self.screen, color_DARKORANGE, (260, 100, 10, 380))  # vertical
        pygame.draw.rect(self.screen, color_DARKORANGE, (390, 100, 10, 380))

    def drawBoardonGrid(self):
        row, col = self.board.shape
        for i in range(row):
            for j in range(col):
                if self.board[i][j] == 1:
                    self.screen.blit(img_CROSS, (self.mapGrid[(i, j)]))
                elif self.board[i][j] == 2:
                    self.screen.blit(img_CIRCLE, (self.mapGrid[(i, j)]))

    def drawScoreBoard(self):
        bd = 2
        pygame.draw.rect(self.screen, color_DARKORANGE, (640, 180, 270, 150))
        pygame.draw.rect(self.screen, color_BACKGROUND, (640 + bd, 180 + bd, 270 - 2 * bd, 150 - 2 * bd))

        font_TITLE = pygame.font.SysFont("ArialNovaW07-Bold", 48)
        text_SCOREBOARD = font_TITLE.render("Score Board", 1, color_SCOREBOARDTEXT)
        rect_SCOREBOARD = text_SCOREBOARD.get_rect()
        rect_SCOREBOARD.midtop = (640 + 270 / 2, 202)
        self.screen.blit(text_SCOREBOARD, rect_SCOREBOARD)

    def drawHint(self):
        bd = 2
        pygame.draw.rect(self.screen, color_DARKORANGE, (640, 330, 270, 65))
        pygame.draw.rect(self.screen, color_BACKGROUND, (640 + bd, 330 + bd, 270 - 2 * bd, 65 - 2 * bd))

    def updateHint(self, hint):
        self.drawHint()
        font_HINT = pygame.font.SysFont("Comic Sans MS", 24, italic=True)
        text_HINT = font_HINT.render(hint, 1, color_SCOREBOARDTEXT)
        rect_HINT = text_HINT.get_rect()
        rect_HINT.midtop = (640 + 270 / 2, 340)
        self.screen.blit(text_HINT, rect_HINT)

    def resetBoard(self):
        self.board = np.zeros((3, 3))

    def clearScreen(self):
        self.screen = (color_BACKGROUND)

    def countMarks(self):
        return np.count_nonzero(self.board)

    def drawResetButton(self):
        bd = 1
        pygame.draw.rect(self.screen, color_DARKERORANGE, (730, 410, 90, 35))
        font_RESET = pygame.font.SysFont("Comic Sans MS", 24, italic=True)
        text_RESET = font_RESET.render("Retry", 1, color_WHITE)
        rect_RESET = text_RESET.get_rect()
        rect_RESET.midtop = (730 + 90 / 2, 408)
        self.screen.blit(text_RESET, rect_RESET)


# single player gameplay sub-class
class gameVsComp(Gameplay):
    def __init__(self, screen, firstToPlay, score):
        super(gameVsComp, self).__init__(screen)
        self.score = score  # player, computer
        self.firstToPlay = firstToPlay
        self.currentPlayer = firstToPlay

    def makeMove(self, click, mx, my):
        if click and self.currentPlayer == "player":
            if gridClickMapper.getGridLocation(mx, my) is not None:
                (i, j) = gridClickMapper.getGridLocation(mx, my)
                inserted = self.insertMark(1, i, j)
                if inserted:
                    self.currentPlayer = "comp"

        elif self.currentPlayer == "comp":
            (cx, cy) = computerLogic.basicAI(self.board)
            inserted = self.insertMark(2, cx, cy)
            if inserted:
                self.currentPlayer = "player"

        self.updateHint(f"{self.currentPlayer}'s move")

    def hasWinner(self, gameOver, winner, click, mx, my):
        winnerOne = "player" if winner == 1 else "comp"
        if not gameOver:
            self.score[winnerOne] += 1

        self.updateHint(f"{winnerOne} wins")
        self.drawResetButton()

        if click and gridClickMapper.getGridLocation(mx, my) == "reset":
            self.resetGame()
            return False
        return True

    def hasDraw(self, gameOver, click, mx, my):
        self.updateHint("match draw")
        self.drawResetButton()

        if click and gridClickMapper.getGridLocation(mx, my) == "reset":
            self.resetGame()
            return False
        return True

    def updateScoreBoard(self):
        self.drawScoreBoard()
        font_SCORE = pygame.font.SysFont("ArialNovaW07-Bold", 36, italic=True)
        text_SCORE = font_SCORE.render(f"Player : {self.score['player']}   Comp : {self.score['comp']}", 1,
                                       color_SCOREBOARDTEXT)
        rect_SCORE = text_SCORE.get_rect()
        rect_SCORE.midtop = (640 + 270 / 2, 280)
        self.screen.blit(text_SCORE, rect_SCORE)

    def resetGame(self):
        self.firstToPlay = "comp" if self.firstToPlay == "player" else "player"
        self.__init__(self.screen, self.firstToPlay, self.score)


# single player gameplay sub-class
class gameVsHuman(Gameplay):
    def __init__(self, screen, firstToPlay, score):
        super(gameVsHuman, self).__init__(screen)
        self.score = score  # player1, player2
        self.firstToPlay = firstToPlay
        self.currentPlayer = firstToPlay

    def makeMove(self, click, mx, my):
        if click and self.currentPlayer == "player1":
            if gridClickMapper.getGridLocation(mx, my) is not None:
                (i, j) = gridClickMapper.getGridLocation(mx, my)
                inserted = self.insertMark(1, i, j)
                if inserted:
                    self.currentPlayer = "player2"

        elif click and self.currentPlayer == "player2":
            if gridClickMapper.getGridLocation(mx, my) is not None:
                (i, j) = gridClickMapper.getGridLocation(mx, my)
                inserted = self.insertMark(2, i, j)
                if inserted:
                    self.currentPlayer = "player1"

        self.updateHint(f"{self.currentPlayer}'s move")

    def hasWinner(self, gameOver, winner, click, mx, my):
        winnerOne = "player1" if winner == 1 else "player2"
        if not gameOver:
            self.score[winnerOne] += 1

        self.updateHint(f"{winnerOne} wins")
        self.drawResetButton()

        if click and gridClickMapper.getGridLocation(mx, my) == "reset":
            self.resetGame()
            return False
        return True

    def hasDraw(self, gameOver, click, mx, my):
        self.updateHint("match draw")
        self.drawResetButton()

        if click and gridClickMapper.getGridLocation(mx, my) == "reset":
            self.resetGame()
            return False
        return True

    def updateScoreBoard(self):
        self.drawScoreBoard()
        font_SCORE = pygame.font.SysFont("ArialNovaW07-Bold", 32, italic=True)
        text_SCORE = font_SCORE.render(f"Player1 : {self.score['player1']}   Player2 : {self.score['player2']}",
                                       1, color_SCOREBOARDTEXT)
        rect_SCORE = text_SCORE.get_rect()
        rect_SCORE.midtop = (640 + 270 / 2, 280)
        self.screen.blit(text_SCORE, rect_SCORE)

    def resetGame(self):
        self.firstToPlay = "player2" if self.firstToPlay == "player1" else "player1"
        self.__init__(self.screen, self.firstToPlay, self.score)


# gameplay vs computer function
def vsComp(screen, firstToPlay="player", score={"player": 0, "comp": 0}):
    mainClock = pygame.time.Clock()
    game = gameVsComp(screen, firstToPlay, score)

    running = True
    gameOver = False
    while running:
        click = False
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # inserting marks
        if not gameOver:
            click = game.makeMove(click, mx, my)

        # checking for wins
        winner = game.checkForWin()
        if winner != 0:
            gameOver = game.hasWinner(gameOver, winner, click, mx, my)

        # checking for draw
        if game.countMarks() == 9 and winner == 0:
            gameOver = game.hasDraw(gameOver, click, mx, my)

        # update board
        game.drawBoardonGrid()
        game.updateScoreBoard()
        pygame.display.update()
        mainClock.tick(60)


# gameplay vs player function
def vsHuman(screen, firstToPlay="player1", score={"player1": 0, "player2": 0}):
    mainClock = pygame.time.Clock()
    game = gameVsHuman(screen, firstToPlay, score)

    running = True
    gameOver = False
    while running:
        click = False
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # inserting marks
        if not gameOver:
            click = game.makeMove(click, mx, my)

        # checking for wins
        winner = game.checkForWin()
        if winner != 0:
            gameOver = game.hasWinner(gameOver, winner, click, mx, my)

        # checking for draw
        if game.countMarks() == 9 and winner == 0:
            gameOver = game.hasDraw(gameOver, click, mx, my)

        # update board
        game.drawBoardonGrid()
        game.updateScoreBoard()
        pygame.display.update()
        mainClock.tick(60)
