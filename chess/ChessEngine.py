# phản hồi các trạng thái của game


class GameState():
    def __init__(self):
        # boards is an 8*8
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveNumber = 0  # số lần di chuyển
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True  # trắng đi trưoc
        self.moveLog = []  # luu tru cac nuoc da di
        self.pins = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False  # check xem có chiếu hết hay không
        self.staleMate = False  # check xem 2 bên có thể chiếu tướng nhau được hay không
        self.enpassantPossible = ()  # ô có thể ăn qua
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    # chuyen quan co den vi tri moi
    def makeMove(self, move):
            """
            Thực hiện di chuyển quân cờ và cập nhật lại bàn cờ và các thuộc tính liên quan.

            Parameters:
                move : Move
                    Đối tượng Move chứa thông tin về di chuyển quân cờ.

            Returns:
            None
            """
            
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)  # để sau này có thể xóa
            self.whiteToMove = not self.whiteToMove  # đổi người chơi
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.endRow, move.endCol)
            if move.pieceMoved == "bK":
                self.blackKingLocation = (move.endRow, move.endCol)

            if move.isPawnPromotion:
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

            if move.isEnpassantMove:
                self.board[move.startRow][move.endCol] = "--"

            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
            else:
                self.enpassantPossible = ()

            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
                else:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                    self.board[move.endRow][move.endCol - 2] = '--'
                    
            
            self.enpassantPossibleLog.append(self.enpassantPossible)
            
            #update castle right
            self.updateCastleRights(move)
            self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                                     self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
            self.moveNumber += 1

    # undo the last move made
    def undoMove(self):
            """
            Hoàn tác nước đi cuối cùng trên bàn cờ.
            """
            if len(self.moveLog) != 0:
                move = self.moveLog.pop()
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured
                self.whiteToMove = not self.whiteToMove
                
                if move.pieceMoved == "wK":
                    self.whiteKingLocation = (move.startRow, move.startCol)
                    
                elif move.pieceMoved == "bK":
                    self.blackKingLocation = (move.startRow, move.startCol)
                    
                if move.isEnpassantMove:
                    self.board[move.endRow][move.endCol] = "--"
                    self.board[move.startRow][move.endCol] = move.pieceCaptured
                    
                self.enpassantPossibleLog.pop()
                self.enpassantPossible = self.enpassantPossibleLog[-1]
                    
                self.castleRightsLog.pop()
                
                newRights = self.castleRightsLog[-1]
                
                self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
                
                if move.isCastleMove:
                    if move.endCol - move.startCol == 2:
                        self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                        self.board[move.endRow][move.endCol - 1] = '--'
                    else:
                        self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                        self.board[move.endRow][move.endCol + 1] = '--'
                self.moveNumber -= 1
                
                self.checkMate = False
                self.staleMate = False

    # all move considering check

    def updateCastleRights(self, move):
            """
            Cập nhật quyền nhập thành của các bên sau mỗi lần di chuyển quân cờ.
            
            Parameters:
            -----------
            move: Move
                Đối tượng di chuyển quân cờ.
            """
            
            if move.pieceMoved == 'wK':
                self.currentCastlingRight.wks = False
                self.currentCastlingRight.wqs = False
            elif move.pieceMoved == 'bK':
                self.currentCastlingRight.bks = False
                self.currentCastlingRight.bqs = False
            elif move.pieceMoved == 'wR':
                if move.startRow == 7:
                    if move.startCol == 0:
                        self.currentCastlingRight.wqs = False
                    elif move.startCol == 7:
                        self.currentCastlingRight.wks = False
            elif move.pieceMoved == 'bR':
                if move.startRow == 0:
                    if move.startCol == 0:
                        self.currentCastlingRight.bqs = False
                    elif move.startCol == 7:
                        self.currentCastlingRight.bks = False


    # get all the moves considering checks
    def getValidMoves(self):
            """
            Trả về danh sách các nước đi hợp lệ của bàn cờ hiện tại.
            """
            
            tmpEnpassantPossible = self.enpassantPossible
            tmpCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                           self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
            moves = self.getAllPossibelMoves()
            if self.whiteToMove:
                self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
            else:
                self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
            for i in range(len(moves) - 1, -1, -1):
                self.makeMove(moves[i])
                self.whiteToMove = not self.whiteToMove
                if self.inCheck():
                    moves.remove(moves[i])
                self.whiteToMove = not self.whiteToMove
                self.undoMove()
            if len(moves) == 0:
                if self.inCheck():
                    self.checkMate = True
                else:
                    self.staleMate = True
            self.enpassantPossible = tmpEnpassantPossible
            self.currentCastlingRight = tmpCastleRights
            return moves

    # all moves without considering checks

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # check if the enemy can attack the square r,c
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibelMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    # tất cả các đường di chuyển có thể của tất cả các quân cờ
    def getAllPossibelMoves(self):
        moves = []
        for r in range(len(self.board)):  # cow
            for c in range(len(self.board[r])):  # row
                turn = self.board[r][c][0]  # while or black
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves


    # nhận tất cả các đường di chuyển của quân tốt tại vị trí row, col
    def getPawnMoves(self, row, col, moves):
            """
            Trả về tất cả các nước đi hợp lệ của quân tốt tại vị trí (row, col) trên bàn cờ hiện tại.
            Nếu quân tốt là quân trắng, hàm sẽ trả về các nước đi hợp lệ của quân tốt trắng.
            Nếu quân tốt là quân đen, hàm sẽ trả về các nước đi hợp lệ của quân tốt đen.
            Các nước đi hợp lệ được lưu trữ trong danh sách 'moves'.
            """
            
            if self.whiteToMove:
                if self.board[row - 1][col] == "--":
                    moves.append(Move((row, col), (row - 1, col), self.board))
                    if row == 6 and self.board[row - 2][col] == "--":
                        moves.append(Move((row, col), (row - 2, col), self.board))
                if col - 1 >= 0:
                    if self.board[row - 1][col - 1][0] == 'b':
                        moves.append(Move((row, col), (row - 1, col - 1), self.board))
                    elif (row - 1, col - 1) == self.enpassantPossible:
                        moves.append(Move((row, col), (row - 1, col - 1), self.board, isEnpassantPossible=True))
                if col + 1 <= 7:
                    if self.board[row - 1][col + 1][0] == 'b':
                        moves.append(Move((row, col), (row - 1, col + 1), self.board))
                    elif (row - 1, col + 1) == self.enpassantPossible:
                        moves.append(Move((row, col), (row - 1, col + 1), self.board, isEnpassantPossible=True))
            else:
                if self.board[row + 1][col] == "--":
                    moves.append(Move((row, col), (row + 1, col), self.board))
                    if row == 1 and self.board[row + 2][col] == "--":
                        moves.append(Move((row, col), (row + 2, col), self.board))
                if col - 1 >= 0:
                    if self.board[row + 1][col - 1][0] == 'w':
                        moves.append(Move((row, col), (row + 1, col - 1), self.board))
                    elif (row + 1, col - 1) == self.enpassantPossible:
                        moves.append(Move((row, col), (row + 1, col - 1), self.board, isEnpassantPossible=True))
                if col + 1 <= 7:
                    if self.board[row + 1][col + 1][0] == 'w':
                        moves.append(Move((row, col), (row + 1, col + 1), self.board))
                    elif (row + 1, col + 1) == self.enpassantPossible:
                        moves.append(Move((row, col), (row + 1, col + 1), self.board, isEnpassantPossible=True))
                    

    # nhận tất cả các đường di chuyển của quân xe tại vị trí row, col
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    # nhận tất cả các đường di chuyển của quân mã tại vị trí row, col
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # nhận tất cả các đường di chuyển của quân tượng tại vị trí row, col
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        emeryColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == emeryColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    # nhận tất cả các đường di chuyển của quân hậu tại vị trí row, col
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    # nhận tất cả các đường di chuyển của quân vua tại vị trí row, col
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # get all the castle moves for the king at (r, c) and add them to the list of moves
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (
                not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (
                not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    # get the kingside castle move for the king at (r, c) and add them to the list of moves
    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == "--" and self.board[r][c + 2]:
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    # get the queenside castle move for the king at (r, c) and add them to the list of moves
    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

# lưu trữ các quyền di chuyển của quân vua
class CastleRights():
    """
    Lớp CastleRights đại diện cho quyền di chuyển của vua trong trường hợp nhập thành.
    """
    
    def __init__(self, wks, bks, wqs, bqs):
        """
        Parameters:
            wks, bks: kingside in black and white
            wqs, bqs: queenside in white and black
        """
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


# lưu trữ các thuộc tính của một nước đi
class Move():
    """
    Lớp Move đại diện cho một nước đi trong trò chơi cờ vua.
    """

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowToRanks = {v: k for k, v in ranksToRows.items()}
    fileToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in fileToCols.items()}

    def __init__(self, startsq, endsq, board, isEnpassantPossible=False, isCastleMove=False):
        """
        Khởi tạo một đối tượng Move với các thông tin cần thiết.

        Parameters:
            startsq (tuple): Tọa độ hàng và cột của ô bắt đầu.
            endsq (tuple): Tọa độ hàng và cột của ô kết thúc.
            board (list): Bảng cờ hiện tại.
            isEnpassantPossible (bool): Cho biết có thể thực hiện nước đi En passant hay không.
            isCastleMove (bool): Cho biết có thể thực hiện nước đi Castle hay không.
        """
        self.startRow = startsq[0]
        self.endRow = endsq[0]
        self.startCol = startsq[1]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (
                    self.pieceMoved == "bp" and self.endRow == 7)

        self.isEnpassantMove = isEnpassantPossible
        if self.isEnpassantMove:
            if self.pieceMoved == "bp":
                self.pieceCaptured = "wp"
            else:
                self.pieceCaptured = "bp"
        self.castle = isCastleMove
        self.isCapture = self.pieceCaptured != "--"

        self.isCastleMove = isCastleMove
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    # Overriding the equals method
    def __eq__(self, other):
        """
        So sánh hai đối tượng Move với nhau.

        Parameters:
            other (Move): Đối tượng Move cần so sánh.

        Returns:
            bool: True nếu hai đối tượng Move giống nhau, False nếu không giống nhau.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    # Overriding the hash method
    def getChessNotation(self):
        """
        Trả về chuỗi biểu diễn nước đi theo định dạng của cờ vua.

        Returns:
            str: Chuỗi biểu diễn nước đi theo định dạng của cờ vua.
        """
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        """
        Trả về tọa độ của ô cờ theo định dạng của cờ vua.

        Parameters:
            r (int): Hàng của ô cờ.
            c (int): Cột của ô cờ.

        Returns:
            str: Chuỗi biểu diễn tọa độ của ô cờ theo định dạng của cờ vua.
        """
        return self.colsToFiles[c] + self.rowToRanks[r]

    def __str__(self):
        #castle move
        if self.castle:
            return "O-O" if self.endCol == 6 else "O-O-O"

        endSquare = self.getRankFile(self.endRow, self.endCol)

        #pawn moves
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

        #two of the same type of piece moving to a square, Nbd2 if both knights can move to d2
        if self.pieceMoved[1] == 'N':
            if self.isCapture:
                return "N" + self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return "N" + endSquare
        #also adding + for check move, and # for checkmate move
        if self.isCapture:
            if self.pieceMoved[1] == 'K':
                return "K" + self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return self.pieceMoved[1] + "x" + endSquare

        #piece moves
        moveString = self.pieceMoved[1]
        if self.pieceCaptured != "--":
            moveString += "x"
        return moveString + endSquare
        
        
        


