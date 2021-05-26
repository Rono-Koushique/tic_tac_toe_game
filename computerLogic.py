import random

def basicAI(board):
    row, col = board.shape
    possibleMoves = []

    for i in range(row):
        for j in range(col):
            if board[i][j] == 0:
                possibleMoves.append((i,j))

    for char in [2, 1]:
        for choice in possibleMoves:
            i, j = choice
            boardCopy = board.copy()
            boardCopy[i][j] = char
            if isWinner(boardCopy, char):
                move = choice
                return move

    cornersOpen = []
    for choice in possibleMoves:
        if choice in [(0,0), (0,2), (2,0), (2,2)]:
            cornersOpen.append(choice)
    if len(cornersOpen) > 0:
        move = selectRandom(cornersOpen)
        return move

    if (1,1) in possibleMoves:
        return (1,1)

    edgesOpen = []
    for choice in possibleMoves:
        if choice in [(0,1), (1,0), (1,2), (2,1)]:
            edgesOpen.append(choice)
    if len(edgesOpen) > 0:
        move = selectRandom(edgesOpen)
        return move

def selectRandom(array):
    randomIdx = random.randint(0, len(array)-1)
    return array[randomIdx]

def isWinner(board, player):
    return (board[0][0] == player and board[0][1] == player and board[0][2] == player) or \
           (board[1][0] == player and board[1][1] == player and board[1][2] == player) or \
           (board[2][0] == player and board[2][1] == player and board[2][2] == player) or \
           (board[0][0] == player and board[1][0] == player and board[2][0] == player) or \
           (board[0][1] == player and board[1][1] == player and board[2][1] == player) or \
           (board[0][2] == player and board[1][2] == player and board[2][2] == player) or \
           (board[0][0] == player and board[1][1] == player and board[2][2] == player) or \
           (board[0][2] == player and board[1][1] == player and board[2][0] == player)
