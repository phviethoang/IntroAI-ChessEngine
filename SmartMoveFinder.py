import random
import time

moveCounter = 0
moveTime = 0

# Điểm số của từng quân cờ
pieceScore = {"p": 100, "N": 320, "B": 330, "R": 500, "Q": 900, "K": 0}



# Điểm số của từng quân mã
knightScores = [[-66, -53, -75, -75, -10, -55, -58, -70],
                [-3, -6, 100, -36, 4, 62, -4, -14],
                [10, 67, 1, 74, 73, 27, 62, -2],
                [24, 24, 45, 37, 33, 41, 25, 17],
                [-1, 5, 31, 21, 22, 35, 2, 0],
                [-18, 10, 13, 22, 18, 15, 11, -14],
                [-23, -15, 2, 0, 2, 0, -23, -20],
                [-74, -23, -26, -24, -19, -35, -22, -69]]

# Điểm số của từng quân tượng
bishopScores = [[-59, -78, -82, -76, -23, -107, -37, -50],
                [-11, 20, 35, -42, -39, 31, 2, -22],
                [-9, 39, -32, 41, 52, -10, 28, -14],
                [25, 17, 20, 34, 26, 25, 15, 10],
                [13, 10, 17, 23, 17, 16, 0, 7],
                [14, 25, 24, 15, 8, 25, 20, 15],
                [19, 20, 11, 6, 7, 6, 20, 16],
                [-7, 2, -15, -12, -14, -15, -10, -10]]

# Điểm số của từng quân xe
rookScores = [[35, 29, 33, 4, 37, 33, 56, 50],
              [55, 29, 56, 67, 55, 62, 34, 60],
              [19, 35, 28, 33, 45, 27, 25, 15],
              [0, 5, 16, 13, 18, -4, -9, -6],
              [-28, -35, -16, -21, -13, -29, -46, -30],
              [-42, -28, -42, -25, -25, -35, -26, -46],
              [-53, -38, -31, -26, -29, -43, -44, -53],
              [-30, -24, -18, 5, -2, -18, -31, -32]]

# Điểm số của từng quân hậu
queenScores = [[6, 1, -8, -104, 69, 24, 88, 26],
               [14, 32, 60, -10, 20, 76, 57, 24],
               [-2, 43, 32, 60, 72, 63, 43, 2],
               [1, -16, 22, 17, 25, 20, -13, -6],
               [-14, -15, -2, -5, -1, -10, -20, -22],
               [-30, -6, -13, -11, -16, -11, -16, -27],
               [-36, -18, 0, -19, -15, -15, -21, -38],
               [-39, -30, -31, -13, -31, -36, -34, -42]]

# Điểm số của từng quân tốt
pawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
              [50, 50, 50, 50, 50, 50, 50, 50],
              [10, 10, 20, 30, 30, 20, 10, 10],
              [5, 5, 10, 25, 25, 10, 5, 5],
              [0, 0, 0, 20, 20, 0, 0, 0],
              [5, -5, -10, 0, 0, -10, -5, 5],
              [5, 10, 10, -20, -20, 10, 10, 5],
              [0, 0, 0, 0, 0, 0, 0, 0]]

# Điểm số của từng quân vua
kingScores = [[-90, -90, -90, -90, -90, -90, -90, -90],
              [-60, -60, -80, -80, -80, -80, -60, -60],
              [-40, -50, -60, -70, -70, -60, -50, -40],
              [-30, -40, -40, -50, -50, -40, -40, -30],
              [-20, -30, -30, -40, -40, -30, -30, -20],
              [-10, -20, -20, -20, -20, -20, -20, -10],
              [20, 20, 0, 0, 0, 0, 20, 20],
              [20, 30, 10, 0, 0, 10, 30, 20]]

# Điểm số của từng quân cờ tại vị trí cụ thể trên bàn cờ
piecePositionScores = {"wN": knightScores,
                       "bN": knightScores[::-1],
                       "wB": bishopScores,
                       "bB": bishopScores[::-1],
                       "wQ": queenScores,
                       "bQ": queenScores[::-1],
                       "wR": rookScores,
                       "bR": rookScores[::-1],
                       "wp": pawnScores,
                       "bp": pawnScores[::-1],
                       "wK": kingScores,
                       "bK": kingScores[::-1],
                       }

# Điểm số khi chiếu hết
CHECKAMTE = 100000000

# Điểm số khi hòa cờ
STABLEMATE = 0
# Độ sâu tìm kiếm
DEPTH = 3



def findRandomMove(validMoves):
    """
    Hàm tìm một nước đi ngẫu nhiên trong danh sách các nước đi hợp lệ.

    Parameters:
    validMoves (list): Danh sách các nước đi hợp lệ.

    Returns:
    tuple: Tọa độ của quân cờ được di chuyển và tọa độ đích của nước đi.
    """
    return validMoves[random.randint(0, len(validMoves) - 1)]


# Quân đen tìm min
def findBestMove(gs, validMoves):
    """
    Hàm tìm nước đi tốt nhất cho quân đen.

    Parameters:
    gs (GameState): Trạng thái hiện tại của bàn cờ.
    validMoves (list): Danh sách các nước đi hợp lệ.

    Returns:
    tuple: Tọa độ của quân cờ được di chuyển và tọa độ đích của nước đi.
    """
    
    turnMultiplire = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKAMTE
    bestMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentMaxScore = STABLEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKAMTE
        else:
            opponentMaxScore = -CHECKAMTE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                if gs.checkMate:
                    score = CHECKAMTE
                elif gs.staleMate:
                    score = STABLEMATE
                else:
                    score = -turnMultiplire * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestMove = playerMove
        gs.undoMove()
    return bestMove


def findBestMoveMinMax(gs, validMoves):
    """
    Hàm tìm nước đi tốt nhất cho một bên bằng thuật toán Minimax.

    Parameters:
    gs (GameState): Trạng thái hiện tại của bàn cờ.
    validMoves (list): Danh sách các nước đi hợp lệ.

    Returns:
    tuple: Tọa độ của quân cờ được di chuyển và tọa độ đích của nước đi.
    """
    global nextMove, moveCounter, moveTime
    start_time = time.time()
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMax(gs, validMoves, DEPTH, -CHECKAMTE, CHECKAMTE, 1 if gs.whiteToMove else -1)
    end_time = time.time()
    moveTime = (end_time - start_time)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    """
    Hàm tìm điểm số của một nước đi bằng thuật toán Minimax.

    Parameters:
    gs (GameState): Trạng thái hiện tại của bàn cờ.
    validMoves (list): Danh sách các nước đi hợp lệ.
    depth (int): Độ sâu tìm kiếm.
    whiteToMove (bool): True nếu là lượt đi của quân trắng, False nếu là lượt đi của quân đen.

    Returns:
    int: Điểm số của nước đi.
    """
    global nextMove, moveCounter
    moveCounter += 1
    random.shuffle(validMoves)
    if depth == 0:
        return scoreBoard(gs)

    if whiteToMove:
        maxScore = -CHECKAMTE
        for move in validMoves:
            moveCounter += 1
            gs.makeMove(move)
            tmpCheckMate = gs.checkMate
            tmpStaleMate = gs.staleMate
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.checkMate = tmpCheckMate
            gs.staleMate = tmpStaleMate
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKAMTE
        for move in validMoves:
            gs.makeMove(move)
            tmpCheckMate = gs.checkMate
            tmpStaleMate = gs.staleMate
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.checkMate = tmpCheckMate
            gs.staleMate = tmpStaleMate
            gs.undoMove()
        return minScore


def findMoveNegaMax(gs, validMoves, depth, alpha, beta, turnMultiplier):
    """
    Hàm tìm điểm số của một nước đi bằng thuật toán NegaMax.

    Parameters:
    gs (GameState): Trạng thái hiện tại của bàn cờ.
    validMoves (list): Danh sách các nước đi hợp lệ.
    depth (int): Độ sâu tìm kiếm.
    alpha (int): Giá trị alpha.
    beta (int): Giá trị beta.
    turnMultiplier (int): Hệ số nhân cho điểm số.

    Returns:
    int: Điểm số của nước đi.
    """
    global nextMove, moveCounter
    random.shuffle(validMoves)
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = - CHECKAMTE
    for move in validMoves:
        moveCounter += 1
        gs.makeMove(move)
        tmpCheckMate = gs.checkMate
        tmpStaleMate = gs.staleMate
        nextMoves = gs.getValidMoves()
        if len(nextMoves) == 0:
            if gs.checkMate:
                score = turnMultiplier * -CHECKAMTE
            elif gs.staleMate:
                score = STABLEMATE
        else:
            score = -findMoveNegaMax(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.checkMate = tmpCheckMate
        gs.staleMate = tmpStaleMate
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def scoreBoard(gs):
    """
    Hàm tính điểm số của bàn cờ.

    Parameters:
    gs (GameState): Trạng thái hiện tại của bàn cờ.

    Returns:
    int: Điểm số của bàn cờ.
    """
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKAMTE  # Den Win
        else:
            return CHECKAMTE  # Trang win
    elif gs.staleMate:
        return STABLEMATE

    score = 0
    for row in range(0, 8):
        for square in range(0, 8):
            piece = gs.board[row][square]
            if piece != "--":
                if gs.moveNumber <= 10:
                    piece_position_score = 0
                else:
                    piece_position_score = piecePositionScores[piece][row][square]
                if piece[0] == "w":
                    score += pieceScore[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= pieceScore[piece[1]] + piece_position_score
    return score


def scoreMaterial(gs):
    """
    Hàm tính điểm số của bàn cờ dựa trên giá trị của từng quân cờ.

    Parameters:
    gs (GameState): Trạng thái hiện tại của bàn cờ.

    Returns:
    int: Điểm số của bàn cờ.
    """
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKAMTE  # Den Win
        else:
            return CHECKAMTE  # Trang win
    elif gs.staleMate:
        return STABLEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            if square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
