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
def draw_mode_selection_screen(screen):
    """
    Vẽ màn hình chọn chế độ.
    
    :param screen: pygame.Surface object, màn hình hiển thị.
    :return: Chế độ chơi (True cho "Chơi với người", False cho "Chơi với máy").
    """
    screen.fill(p.Color("gray"))
    font = p.font.Font(None, 60)
    title_text = font.render("CHESS ARENA", True, p.Color("black"))
    title_rect = title_text.get_rect(center=(BOARD_WIDTH // 2 + 150, 200))
    screen.blit(title_text, title_rect)

    # Tạo các nút chọn chế độ
    button_font = p.font.Font(None, 36)
    button_text1 = button_font.render("Play With Human", True, p.Color("black"))
    button_text2 = button_font.render("Play With AI", True, p.Color("black"))

    button1_rect = p.Rect(BOARD_WIDTH // 2, 300, 300, 50)
    button2_rect = p.Rect(BOARD_WIDTH // 2, 400, 300, 50)

    # Vẽ lại các nút
    p.draw.rect(screen, p.Color("lightgray"), button1_rect)  # Nút Play With Human
    p.draw.rect(screen, p.Color("lightgray"), button2_rect)  # Nút Play With AI


    screen.blit(button_text1, button1_rect.move(50, 15))
    screen.blit(button_text2, button2_rect.move(80, 15))
    # Hiển thị hướng dẫn ở góc dưới trái
    instructions_font = p.font.SysFont("Arial", 22, False, False)
    instructions_text = "R: Restart the game | Z: Undo the previous move | Home: Return to the main menu"
    instructions_surface = instructions_font.render(instructions_text, True, p.Color("black"))
    # Vẽ hướng dẫn lên màn hình tại vị trí góc dưới bên trái
    screen.blit(instructions_surface, (10, BOARD_HEIGHT - 30))  
    instructions_font_name = p.font.SysFont("Arial", 26, False, False)
    instructions_name="Instructions:"
    instructions_surface_name=instructions_font_name.render(instructions_name, True, p.Color("black"))
    screen.blit(instructions_surface_name,(10, BOARD_HEIGHT - 60))
    p.display.flip()

    # Chờ người chơi chọn chế độ
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button1_rect.collidepoint(x, y):
                    return True  # Chọn chơi với người
                elif button2_rect.collidepoint(x, y):
                    return False  # Chọn chơi với máy
                
def draw_game_screen(screen, gs, validMoves, sqSelected, moveLogFont):
    """
    Vẽ giao diện chơi cờ và nút Home.
    
    :param screen: pygame.Surface object, màn hình hiển thị.
    :param gs: ChessEngine.GameState object, trạng thái trò chơi.
    :param validMoves: list, các nước đi hợp lệ.
    :param sqSelected: tuple, tọa độ ô cờ đang chọn.
    :param moveLogFont: font cho log các nước đi.
    """
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)
    
    # Tạo nút "Home" ở góc dưới bên phải
    home_button_font = p.font.Font(None, 30)
    home_button_text = home_button_font.render("Home", True, p.Color("black"))
    home_button_rect = p.Rect(BOARD_WIDTH + 190, BOARD_HEIGHT - 50, 80, 40)  # Vị trí góc dưới phải

    # Tạo nút Home với màu nền
    p.draw.rect(screen, p.Color("lightblue"), home_button_rect)
    screen.blit(home_button_text, home_button_rect.move(15, 10))

    # Cập nhật màn hình
    p.display.flip()
    return home_button_rect

def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    running = True

    while running:
        # Vẽ màn hình chọn chế độ
        mode = draw_mode_selection_screen(screen)
        
        if mode is None:
            # Quay lại màn hình chọn chế độ khi nhấn "Home"
            continue
        elif mode:
            # Bắt đầu trò chơi với người chơi (Play with Another Player)
            result = play_game(playerTwo=True)
        else:
            # Bắt đầu trò chơi với AI (Play with AI)
            result = play_game(playerTwo=False)
        
        if result == "home":
            continue  # Quay lại màn hình chọn chế độ nếu nhấn Home
        elif result == "quit":
            running = False 
    clock.tick(MAX_FPS)
def play_game(playerTwo):
    """
    Hàm chạy game, kiểm tra các nước đi và sự kiện game.
    
    :param playerTwo: Boolean, nếu là True là chơi với AI, False là chơi với người.
    """
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 16, False, False)
    gs = ChessEngine.GameState()
    animate = False
    moveMade = False
    loadImages()  # Tải ảnh quân cờ
    running = True
    sqSelected = ()  # Ô cờ đang được chọn
    playerClicks = []
    validMoves = gs.getValidMoves()
    gameOver = False
    playerOne = True
    while running:
        # Kiểm tra lượt người chơi
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        for e in p.event.get():  # Sử lý sự kiện
            if e.type == p.QUIT:
                return "quit"

            # Xử lý click chuột
            elif not gameOver and e.type == p.MOUSEBUTTONDOWN:
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
                                    gs.board[validMoves[i].endRow][validMoves[i].endCol] = validMoves[i].pieceMoved[0] + promotion_choice
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
            # AI xử lý nếu không phải lượt người chơi
        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMoveNegaMax(gs, validMoves)
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

        # Vẽ giao diện trò chơi và kiểm tra nút "Home"
        home_button_rect = draw_game_screen(screen, gs, validMoves, sqSelected, moveLogFont)

        # Kiểm tra sự kiện nhấn nút "Home"
        if p.mouse.get_pressed()[0]:  # Kiểm tra nếu người chơi nhấn chuột
            x, y = p.mouse.get_pos()
            if home_button_rect.collidepoint(x, y):
                return "home"  # Quay lại trang chủ

        # Kiểm tra kết thúc trò chơi và hiển thị thông báo
        if gs.checkMate:
            gameOver = True
            winner = "Black" if gs.whiteToMove else "White"
            draw_end_game_message(screen, f"{winner} wins by checkmate")
        elif gs.staleMate:
            gameOver = True
            draw_end_game_message(screen, "Stalemate")
        # Nếu trò chơi đã kết thúc, không cập nhật màn hình thêm nữa
        if gameOver:
            p.display.flip()  # Chỉ cập nhật khi có thay đổi (vẽ thông báo kết thúc)
            continue  # Đợi người chơi nhấn "Home" để thoát

        clock.tick(MAX_FPS)  # gioi han so khung hinh moi giay
        p.display.flip()  # không co che do full man hinh


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

def draw_end_game_message(screen, message):
    """
    Hàm vẽ thông báo kết quả khi trò chơi kết thúc (checkmate, stalemate, v.v.)
    
    :param screen: màn hình hiển thị.
    :param message: thông báo kết quả, ví dụ "White wins", "Black wins".
    """
    font = p.font.SysFont("Arial", 40, True, False)
    text = font.render(message, True, p.Color("black"))
    text_rect = text.get_rect(center=(BOARD_WIDTH // 2, BOARD_HEIGHT // 2))
    
    # Vẽ nền mờ phía sau thông báo
    overlay = p.Surface((BOARD_WIDTH, BOARD_HEIGHT))
    overlay.set_alpha(128)  # Mức độ mờ
    overlay.fill(p.Color("gray"))
    screen.blit(overlay, (0, 0))
    
    # Vẽ thông báo lên màn hình
    screen.blit(text, text_rect)
    p.display.flip()


if __name__ == "__main__":
    main()
