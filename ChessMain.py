import sys

import pygame as p
import ChessEngine, SmartMoveFinder
from SmartMoveFinder import moveCounter, moveTime

BOARD_WIDTH = BOARD_HEIGHT = 720 # kich thuoc ban co
MOVE_LOG_PANEL_WIDTH = 280
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8  # số ô mỗi chiều
SQ_SIZE = BOARD_HEIGHT // DIMENSION  # kich thuoc 1 ô
MAX_FPS = 15  # FOR ANIMATIONS LATER ON
IMAGES = {}


def loadImages():
    """
    Tải ảnh các quân cờ từ thư mục images và lưu vào biến IMAGES.
    """
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def draw_promotion_popup(screen):
    popup_rect = p.Rect(250, 180, 500, 360)
    p.draw.rect(screen, (255, 255, 255), popup_rect)

    font = p.font.Font(None, 36)
    text = font.render("Choose the piece:", True, (0, 0, 0))
    text_rect = text.get_rect(center=(popup_rect.centerx, popup_rect.top + 30))
    screen.blit(text, text_rect)

    options = ["Q", "R", "B", "N"]
    button_rects = []
    for i, option in enumerate(options):
        button_rect = p.Rect(
            popup_rect.left + 30 + i * 120, popup_rect.top + 80, 100, 40
        )
        p.draw.rect(screen, (200, 200, 200), button_rect)
        button_text = font.render(option, True, (0, 0, 0))
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)
        button_rects.append((button_rect, option))

    p.display.flip()

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                x, y = event.pos
                for button_rect, option in button_rects:
                    if button_rect.collidepoint(x, y):
                        return option

def promote_pawn_popup():
    option = None
    popup_screen = p.display.set_mode((1000, 720))
    p.display.set_caption("Chess Game - Promotion Popup")

    while option is None:
        option = draw_promotion_popup(popup_screen)

    return option

# ham thực thi
def main():
    """
    Hàm chính của chương trình, thực hiện khởi tạo trạng thái ban đầu của bàn cờ, lấy thông tin click chuột của người chơi, 
    xử lý các sự kiện, thực hiện các nước đi hợp lệ, vẽ bàn cờ và kiểm tra kết thúc trò chơi.
    """

    # move_Times = []
    # move_counts = []
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 16, False, False)
    gs = ChessEngine.GameState()  # khoi tao trang thai ban dau
    animate = False
    moveMade = False  # flag varible for when a move is made
    loadImages()  # tao mang chua anh cac quan cờ
    running = True
    sqSelected = ()  # cac ô cờ được click
    playerClicks = []
    # lưu trư thong tin click cua nguoi choi
    validMoves = gs.getValidMoves()
    gameOver = False
    playerOne = True
    playerTwo = False
    while running:  # neu dang thuc thi chuong trinh
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        for e in p.event.get():  # sử lý  kiện clicked chuột
            if e.type == p.QUIT:
                running = False

            # mouse handle
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8:
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())  # in ra vi tri bat dau va ket thuc cua quan co
                        validMoves = gs.getValidMoves()
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])  # chuyen quan co den vi tri moi
                                if (validMoves[i].isPawnPromotion):
                                    promotion_choice = promote_pawn_popup()
                                    gs.board[validMoves[i].endRow][validMoves[i].endCol] = validMoves[i].pieceMoved[
                                                                                               0] + promotion_choice
                                # if moveMade:
                                #     move_Times.append(moveTime)
                                #     move_counts.append(moveCounter)
                                moveMade = True
                                animate = True
                                sqSelected = ()  # khởi tạo lại trạng thái click
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # nhan z để quay trở lại
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    validMoves = gs.getValidMoves()
                if e.key == p.K_r:  # nhan r để reset game
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMoveMinMax(gs, validMoves)
            if (AIMove is None):
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            if AIMove.isPawnPromotion:
                AIMove.pieceMoved = AIMove.pieceMoved[0] + "Q"
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

            # Cập nhật dữ liệu mỗi nước đi
            # move_Times.append(SmartMoveFinder.moveTime)
            # move_Times.append(SmartMoveFinder.moveCounter)

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)  # ve ban co

        if gs.checkMate or gs.staleMate:
            gameOver = True
            drawEndGameText(screen,
                            "Stalemate" if gs.staleMate else "Black wins by checkmate" if gs.whiteToMove else "White wins by checkmate")

        clock.tick(MAX_FPS)  # gioi han so khung hinh moi giay
        p.display.flip()  # không co che do full man hinh


# vẽ ban co va quan co
def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    """
    Vẽ trạng thái hiện tại của bàn cờ.

    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param gs: GameState object, trạng thái hiện tại của trò chơi
    :param validMoves: list, danh sách các nước đi hợp lệ
    :param sqSelected: tuple, tọa độ ô cờ đang được chọn
    """
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)


def drawBoard(screen):
    """
    Vẽ bàn cờ với 2 màu trắng và xám.

    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    """
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlightSquares(screen, gs, validMoves, sqSelected):
    """
    Tô màu các ô cờ trên bàn cờ để thể hiện các nước đi hợp lệ và ô cờ đang được chọn.
    
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param gs: GameState object, trạng thái hiện tại của trò chơi
    :param validMoves: list, danh sách các nước đi hợp lệ
    :param sqSelected: tuple, tọa độ ô cờ đang được chọn
    """

    if sqSelected != ():
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


# dua cac quan co vao ban co
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


def drawMoveLog(screen, game_state, font):
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = game_state.moveLog

    # Định dạng mỗi nước đi để có cùng chiều dài
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = f"{i // 2 + 1}. {str(move_log[i]).ljust(15)}"  # Căn chỉnh nước đi thứ nhất
        if i + 1 < len(move_log):
            move_string += f"{str(move_log[i + 1]).ljust(15)}"  # Căn chỉnh nước đi thứ hai
        move_texts.append(move_string)

    moves_per_row = 1
    padding = 5
    line_spacing = 2
    text_y = padding
    for move_text in move_texts:
        text_object = font.render(move_text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def animateMove(move, screen, board, clock):
    """
    Thực hiện animation cho một nước đi trên bàn cờ.
    
    :param move: Move object, nước đi cần thực hiện animation
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param board: list, danh sách các quân cờ trên bàn cờ
    :param clock: pygame.time.Clock object, đồng hồ đếm thời gian
    """
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        if move.pieceMoved != '--':
            screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        p.display.flip()
        clock.tick(60)


def drawEndGameText(screen, text):
    """
    Vẽ text trên màn hình.
    
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param text: str, text cần vẽ
    """
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == "__main__":
    main()
