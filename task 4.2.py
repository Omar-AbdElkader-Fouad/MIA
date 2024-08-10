import tkinter as tk
from tkinter import messagebox

WHITE = "white"
BLACK = "black"

class Game:
    def __init__(self):
        self.playersturn = BLACK
        self.message = "This is where prompts will go"
        self.gameboard = {}
        self.place_pieces()
        self.init_gui()

    def place_pieces(self):
        for i in range(8):
            self.gameboard[(i, 1)] = Pawn(WHITE, uniDict[WHITE][Pawn], 1)
            self.gameboard[(i, 6)] = Pawn(BLACK, uniDict[BLACK][Pawn], -1)
        
        placers = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        
        for i in range(8):
            self.gameboard[(i, 0)] = placers[i](WHITE, uniDict[WHITE][placers[i]])
            self.gameboard[(7 - i, 7)] = placers[i](BLACK, uniDict[BLACK][placers[i]])
        placers.reverse()

    def init_gui(self):
        self.root = tk.Tk()
        self.root.title("Chess Game")
        self.canvas = tk.Canvas(self.root, width=640, height=640)
        self.canvas.pack()
        self.draw_board()
        self.root.mainloop()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(i*80, j*80, (i+1)*80, (j+1)*80, fill=color)
                piece = self.gameboard.get((i, j), None)
                if piece:
                    self.canvas.create_text(i*80+40, j*80+40, text=piece.name, font=("Arial", 36))
        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        x, y = event.x // 80, event.y // 80
        if hasattr(self, 'start_pos'):
            self.end_pos = (x, y)
            self.make_move(self.start_pos, self.end_pos)
            del self.start_pos
        else:
            self.start_pos = (x, y)

    def make_move(self, startpos, endpos):
        try:
            target = self.gameboard[startpos]
        except KeyError:
            self.message = "Could not find piece; index probably out of range"
            target = None

        if target:
            if target.Color != self.playersturn:
                self.message = "You aren't allowed to move that piece this turn"
                return
            if target.isValid(startpos, endpos, target.Color, self.gameboard):
                self.message = "That is a valid move"
                self.gameboard[endpos] = self.gameboard[startpos]
                del self.gameboard[startpos]
                self.is_check()
                self.playersturn = WHITE if self.playersturn == BLACK else BLACK
            else:
                self.message = "Invalid move"
        else:
            self.message = "There is no piece in that space"

        self.draw_board()
        if "check" in self.message:
            messagebox.showinfo("Check", self.message)

    def is_check(self):
        kingDict = {}
        pieceDict = {BLACK: [], WHITE: []}
        for position, piece in self.gameboard.items():
            if isinstance(piece, King):
                kingDict[piece.Color] = position
            pieceDict[piece.Color].append((piece, position))
        if self.can_see_king(kingDict[WHITE], pieceDict[BLACK]):
            self.message = "White player is in check"
        if self.can_see_king(kingDict[BLACK], pieceDict[WHITE]):
            self.message = "Black player is in check"

    def can_see_king(self, kingpos, piecelist):
        for piece, position in piecelist:
            if piece.isValid(position, kingpos, piece.Color, self.gameboard):
                return True
        return False

class Piece:
    def __init__(self, color, name):
        self.name = name
        self.Color = color

    def isValid(self, startpos, endpos, Color, gameboard):
        if endpos in self.available_moves(startpos[0], startpos[1], gameboard, Color):
            return True
        return False

    def available_moves(self, x, y, gameboard, Color=None):
        pass

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def ad_nauseum(self, x, y, gameboard, Color, intervals):
        answers = []
        for xint, yint in intervals:
            xtemp, ytemp = x + xint, y + yint
            while self.is_in_bounds(xtemp, ytemp):
                target = gameboard.get((xtemp, ytemp), None)
                if target is None:
                    answers.append((xtemp, ytemp))
                elif target.Color != Color:
                    answers.append((xtemp, ytemp))
                    break
                else:
                    break
                xtemp, ytemp = xtemp + xint, ytemp + yint
        return answers

    def is_in_bounds(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def no_conflict(self, gameboard, initialColor, x, y):
        if self.is_in_bounds(x, y) and (((x, y) not in gameboard) or gameboard[(x, y)].Color != initialColor):
            return True
        return False

chessCardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
chessDiagonals = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

def knightList(x, y, int1, int2):
    return [(x + int1, y + int2), (x - int1, y + int2), (x + int1, y - int2), (x - int1, y - int2),
            (x + int2, y + int1), (x - int2, y + int1), (x + int2, y - int1), (x - int2, y - int1)]

def kingList(x, y):
    return [(x + 1, y), (x + 1, y + 1), (x + 1, y - 1), (x, y + 1), (x, y - 1), (x - 1, y), (x - 1, y + 1), (x - 1, y - 1)]

class Knight(Piece):
    def available_moves(self, x, y, gameboard, Color=None):
        if Color is None:
            Color = self.Color
        return [(xx, yy) for xx, yy in knightList(x, y, 2, 1) if self.no_conflict(gameboard, Color, xx, yy)]

class Rook(Piece):
    def available_moves(self, x, y, gameboard, Color=None):
        if Color is None:
            Color = self.Color
        return self.ad_nauseum(x, y, gameboard, Color, chessCardinals)

class Bishop(Piece):
    def available_moves(self, x, y, gameboard, Color=None):
        if Color is None:
            Color = self.Color
        return self.ad_nauseum(x, y, gameboard, Color, chessDiagonals)

class Queen(Piece):
    def available_moves(self, x, y, gameboard, Color=None):
        if Color is None:
            Color = self.Color
        return self.ad_nauseum(x, y, gameboard, Color, chessCardinals + chessDiagonals)

class King(Piece):
    def available_moves(self, x, y, gameboard, Color=None):
        if Color is None:
            Color = self.Color
        return [(xx, yy) for xx, yy in kingList(x, y) if self.no_conflict(gameboard, Color, xx, yy)]

class Pawn(Piece):
    def __init__(self, color, name, direction):
        super().__init__(color, name)
        self.direction = direction

    def available_moves(self, x, y, gameboard, Color=None):
        if Color is None:
            Color = self.Color
        answers = []
        if (x + 1, y + self.direction) in gameboard and self.no_conflict(gameboard, Color, x + 1, y + self.direction):
            answers.append((x + 1, y + self.direction))
        if (x - 1, y + self.direction) in gameboard and self.no_conflict(gameboard, Color, x - 1, y + self.direction):
            answers.append((x - 1, y + self.direction))
        if (x, y + self.direction) not in gameboard and Color == self.Color:
            answers.append((x, y + self.direction))
        return answers

uniDict = {
    WHITE: {Pawn: "♙", Rook: "♖", Knight: "♘", Bishop: "♗", King: "♔", Queen: "♕"},
    BLACK: {Pawn: "♟", Rook: "♜", Knight: "♞", Bishop: "♝", King: "♚", Queen: "♛"}
}

if __name__ == "__main__":
    Game()
