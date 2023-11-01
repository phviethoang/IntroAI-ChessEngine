import  random

pieceScore = {"K": 0, "Q": 10, "R" : 5, "B": 3, "N":3, "p":1}
CHECKAMTE=1000 # Nếu chiếu hiết thì dc 1000 điểm
STABLEMATE = 0 # Hòa cờ thì trả về -
DEPTH = 3

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

#Quân đen tìm min 
def findBestMove(gs, validMoves):
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
                    score =  STABLEMATE
                else:
                    score = -turnMultiplire * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestMove=playerMove
        gs.undoMove()
    return bestMove

def findBestMoveMinMax(gs, validMoves):
    global nextMove
    random.shuffle(validMoves)
    findMoveNegaMax(gs, validMoves, DEPTH, -CHECKAMTE, CHECKAMTE,1 if gs.whiteToMove else -1)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    random.shuffle(validMoves)
    if depth == 0:
        return scoreBoard(gs) 
    
    if whiteToMove:
        maxScore = -CHECKAMTE
        for move in validMoves:
            gs.makeMove(move)
            tmpCheckMate=gs.checkMate
            tmpStaleMate= gs.staleMate
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs,nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            s.checkMate=tmpCheckMate
            gs.staleMate=tmpStaleMate
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKAMTE
        for move in validMoves:
            gs.makeMove(move)
            tmpCheckMate=gs.checkMate
            tmpStaleMate= gs.staleMate
            nextMoves= gs.getValidMoves()
            score= findMoveMinMax(gs, nextMoves, depth-1, True)
            if score<minScore:
                minScore=score
                if depth==DEPTH:
                    nextMove=move
            gs.checkMate=tmpCheckMate
            gs.staleMate=tmpStaleMate
            gs.undoMove()
        return minScore
    
def findMoveNegaMax(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    random.shuffle(validMoves)
    if depth==0:
        return turnMultiplier*scoreBoard(gs)
    
    maxScore= - CHECKAMTE
    for move in validMoves:
        gs.makeMove(move)
        tmpCheckMate=gs.checkMate
        tmpStaleMate= gs.staleMate
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.checkMate=tmpCheckMate
        gs.staleMate=tmpStaleMate
        gs.undoMove()
        if maxScore >alpha:
            alpha=maxScore
        if alpha>=beta:
            break
    return maxScore
    

def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKAMTE #Den Win
        else:   
            return CHECKAMTE #Trang win
    elif gs.staleMate:
        return STABLEMATE
    
    score=0
    for row in gs.board:
        for square in row:
            if square[0]=='w':
                score+=pieceScore[square[1]]
            if square[0]=='b':
                score-=pieceScore[square[1]]
    return score


def scoreMaterial(board):
    score=0
    for row in board:
        for square in row:
            if square[0]=='w':
                score+=pieceScore[square[1]]
            if square[0]=='b':
                score-=pieceScore[square[1]]
    return score