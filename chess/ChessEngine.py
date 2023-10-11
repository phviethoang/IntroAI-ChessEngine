# phản hồi các trạng thái của game
class GameState():
    def __init__(self):
        #boards is an 8*8
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--", "--", "--", "--", "--", "--","--","--"],
            ["--", "--", "--", "--", "--", "--","--","--"],
            ["--", "--", "--", "--", "--", "--","--","--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
            ]
        self.whiteToMove=True                   #trắng đi trưoc
        self.moveLog=[]                          #luu tru cac nuoc da di

     #chuyen quan co den vi tri moi
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # để sau này có thể xóa
        self.whiteToMove = not self.whiteToMove  # đổi người chơi

class Move():

    #chuyen doi qua lai giua thu tu o co va vi tri tren ban co
    ranksToRows={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowToRanks={v:k for k,v in ranksToRows.items()}
    fileToCols={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles={v:k for k,v in fileToCols.items()}

    def __init__(self,startsq,endsq,board):
        self.startRow=startsq[0]
        self.endRow=endsq[0]
        self.startCol=startsq[1]
        self.endCol=endsq[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)
    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowToRanks[r]

