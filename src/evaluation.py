import chess


PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0
}

def evaluate_board(board: chess.Board) -> int:
    """Evaluates the board from the perspective of the side to move."""
    if board.is_checkmate():
        return -99999 if board.turn else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for piece_type in PIECE_VALUES:
        score += (
            len(board.pieces(piece_type, chess.WHITE)) * PIECE_VALUES[piece_type]
        )
        score -= (
            len(board.pieces(piece_type, chess.BLACK)) * PIECE_VALUES[piece_type]
        )
    
    return score if board.turn else -score
