from const import *
from square import Square
from piece import *
from move import Move


class Board:
    
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        
    def calc_moves(self, piece, row, col):
        '''
        Calculate all possible (valid) moves of a specific piece at a specific position
        '''
        def pawn_moves():
            # Steps
            steps = 1 if piece.moved else 2

            # Vertical moves
            start = row + piece.dir
            end = row + piece.dir * (1 + steps)
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # Create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # Create new move
                        move = Move(initial, final)
                        # Append new move
                        piece.add_move(move)
                    # Blocked
                    else: break
                # Not in range
                else: break
            
            # Diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # Create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # Create new move
                        move = Move(initial, final)
                        # Append new move
                        piece.add_move(move)
        
        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # Create squares of the possible new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col) #piece=piece
                        # Create new move
                        move = Move(initial, final)
                        # Append new valid move
                        piece.add_move(move)
        
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr
            
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # Create squares of the possible new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # Create a possible new move
                        move = Move(initial, final)
                        
                        # Empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # Append new move
                            piece.add_move(move)
                        
                        # Has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # Append new move
                            piece.add_move(move)
                            break
                        
                        # Has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    # Not in range
                    else: break
                    
                    # Incrementing incrs      
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr
        
        def king_moves():
            adjs = [
                (row-1, col+0),  # up
                (row-1, col+1),  # up-right
                (row+0, col+1),  # right
                (row+1, col+1),  # down-right
                (row+1, col+0),  # down
                (row+1, col-1),  # down-left
                (row+0, col-1),  # left
                (row-1, col-1),  # up-left
            ]
            
            # Normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # Create squares of the possible new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col) #piece=piece
                        # Create new move
                        move = Move(initial, final)
                        # Append new valid move
                        piece.add_move(move)
                        
            # Castling moves
            
            # Queen-side castling
            
            # King-side castling
        
        if isinstance(piece, Pawn): pawn_moves()
        elif isinstance(piece, Knight): knight_moves()
        
        elif isinstance(piece, Bishop): 
            straightline_moves([
                (-1, 1),  # up-right
                (-1, -1), # up-left
                (1, 1),   # down-right
                (1, -1)   # down-left 
            ])
        
        elif isinstance(piece, Rook): 
            straightline_moves([
                (-1, 0),  # up
                (0, 1),   # right
                (1, 0),   # down
                (0, -1)   # left
            ])
        
        elif isinstance(piece, Queen): 
            straightline_moves([
                (-1, 1),  # up-right
                (-1, -1), # up-left
                (1, 1),   # down-right
                (1, -1),  # down-left
                (-1, 0),  # up
                (0, 1),   # right
                (1, 0),   # down
                (0, -1)   # left
            ])
        
        elif isinstance(piece, King): king_moves()
    
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
    
    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
        
        # Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        
        # Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        
        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
                
        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))
