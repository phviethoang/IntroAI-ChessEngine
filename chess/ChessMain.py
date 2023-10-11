# biểu diễn trạng thái của game và sự kiện người dùng

import pygame as p
from chess import ChessEngine

WIDTH = HEIGHT = 512  # kich thuoc ban co
DIMENSION = 8         # số ô mỗi chiều
SQ_SIZE = HEIGHT // DIMENSION  # kich thuoc 1 ô
MAX_FPS = 15  # FOR ANIMATIONS LATER ON
IMAGES = {}


#load ảnh các quaan cờ vào mảng Image
def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

#ham thực thi
def main():
    #khoi tao man hinh choi cờ
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()              #khoi tao trang thai ban dau
    loadImages()                  #tao mang chua anh cac quan cờ
    running = True
    sqSelected=()                   #cac ô cờ được click
    playerClicks=[]                 #lưu trư thong tin click cua nguoi choi
    while running:                    #neu dang thuc thi chuong trinh
        for e in p.event.get():       #sử lý  kiện clicked chuột
            if e.type == p.QUIT:
                running = False
            elif e.type==p.MOUSEBUTTONDOWN:
                location=p.mouse.get_pos()
                col=location[0]//SQ_SIZE
                row=location[1]//SQ_SIZE
                if sqSelected==(row,col):
                    sqSelected=()
                    playerClicks=[]
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks)==2:
                    move=ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())    #in ra vi tri bat dau va ket thuc cua quan co
                    gs.makeMove(move)                 #chuyen quan co den vi tri moi
                    sqSelected=()  #khởi tạo lại trạng thái click
                    playerClicks=[]
        drawGameState(screen, gs)           #ve ban co
        clock.tick(MAX_FPS)                 #gioi han so khung hinh moi giay
        p.display.flip()              #không co che do full man hinh


# goc phía trên bên trái luôn là màu trắng
#vẽ 2 màu trắng v xám cho bàn cờ
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

#dua cac quan co vao ban co
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

#vẽ ban co va quan co
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


if __name__ == "__main__":
    main()



