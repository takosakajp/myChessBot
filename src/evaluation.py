import chess

# --- Heuristic weights ---
WEIGHTS = {
    "piece_values": {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 320,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0  # King is invaluable but excluded from scoring
    },
    "center_control": 20,
    "development": 30,
    "check_bonus": 50
}

CENTER_SQUARES = [chess.D4, chess.D5, chess.E4, chess.E5]


def material_score(board: chess.Board) -> int:
    score = 0
    for piece_type, value in WEIGHTS["piece_values"].items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value
    return score


def center_control_score(board: chess.Board) -> int:
    weight = WEIGHTS["center_control"]
    score = 0
    for square in CENTER_SQUARES:
        attackers_white = board.attackers(chess.WHITE, square)
        attackers_black = board.attackers(chess.BLACK, square)
        score += len(attackers_white) * weight
        score -= len(attackers_black) * weight
    return score


def development_score(board: chess.Board) -> int:
    weight = WEIGHTS["development"]
    undeveloped_white = sum(
        board.piece_at(sq) is not None and board.piece_at(sq).piece_type in [chess.KNIGHT, chess.BISHOP]
        for sq in [chess.B1, chess.G1, chess.C1, chess.F1]
    )
    undeveloped_black = sum(
        board.piece_at(sq) is not None and board.piece_at(sq).piece_type in [chess.KNIGHT, chess.BISHOP]
        for sq in [chess.B8, chess.G8, chess.C8, chess.F8]
    )
    return (2 - undeveloped_white) * weight - (2 - undeveloped_black) * weight


def check_bonus(board: chess.Board) -> int:
    weight = WEIGHTS["check_bonus"]
    if board.is_check():
        return weight if board.turn == chess.BLACK else -weight
    return 0


def evaluate_board(board: chess.Board, perspective: chess.Color) -> int:
    """Combines all heuristics into one score, modularly weighted."""
    if board.is_checkmate():
        return -99999 if board.turn else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    score += material_score(board)
    score += center_control_score(board)
    score += development_score(board)
    score += check_bonus(board)

    return score if perspective == chess.WHITE else -score
