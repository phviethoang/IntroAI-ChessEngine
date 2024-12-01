import pygame as p
import ChessEngine, SmartMoveFinder, performance

# kích thước bàn cờ
WIDTH = HEIGHT = 512
# số ô mỗi chiều
DIMENSION = 8
# kích thước một ô
SQ_SIZE = HEIGHT // DIMENSION
# cho animations
MAX_FPS = 15
IMAGES = {}


def loadImages():
    """
    Load hình ảnh các quân cờ.
    """
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    """
    Hàm chính của trò chơi.
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    loadImages()

    # Khởi tạo biến để lưu dữ liệu hiệu suất
    white_move_times = []
    black_move_times = []
    white_move_counts = []
    black_move_counts = []

    while not (gs.checkMate or gs.staleMate):
        AIMove = SmartMoveFinder.findBestMoveMinMax(gs, validMoves)
        if AIMove is None:
            AIMove = SmartMoveFinder.findRandomMove(validMoves)
        gs.makeMove(AIMove)

        # Thu thập dữ liệu hiệu suất
        if gs.whiteToMove:
            # Nếu bây giờ là lượt của quân trắng, ghi nhận nước đi cuối cùng của quân đen
            black_move_times.append(SmartMoveFinder.moveTime)
            black_move_counts.append(SmartMoveFinder.moveCounter)
        else:
            # Nếu bây giờ là lượt của quân đen, ghi nhận nước đi cuối cùng của quân trắng
            white_move_times.append(SmartMoveFinder.moveTime)
            white_move_counts.append(SmartMoveFinder.moveCounter)

        validMoves = gs.getValidMoves()
        drawGameState(screen, gs, validMoves)
        clock.tick(MAX_FPS)
        p.display.flip()

    # Vẽ biểu đồ hiệu suất
    performance.plot_performance(white_move_times, white_move_counts, "white_performance.png")
    performance.plot_performance(black_move_times, black_move_counts, "black_performance.png")


def drawGameState(screen, gs, validMoves):
    """
    Vẽ trạng thái hiện tại của trò chơi.
    
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param gs: GameState object, trạng thái hiện tại của trò chơi
    :param validMoves: list, danh sách các nước đi hợp lệ
    """
    drawBoard(screen)  # vẽ bàn cờ
    highlightSquares(screen, gs, validMoves, ())  # tô màu các ô hợp lệ, không có ô nào được chọn
    drawPieces(screen, gs.board)  # vẽ quân cờ


def drawBoard(screen):
    """
    Vẽ bàn cờ.
    
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    """
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    """
    Vẽ các quân cờ trên bàn cờ.
    
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param board: list, danh sách các quân cờ trên bàn cờ
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlightSquares(screen, gs, validMoves, sqSelected):
    """
    Tô màu các ô cờ trên bàn cờ để thể hiện các nước đi hợp lệ và ô cờ đang được chọn.
    
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param gs: GameState object, trạng thái hiện tại của trò chơi
    :param validMoves: list, danh sách các nước đi hợp lệ
    :param sqSelected: tuple, tọa độ ô cờ đang được chọn
    """
    if sqSelected:
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


if __name__ == "__main__":
    main()
