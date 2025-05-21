import chess
from evaluation import evaluate_board


def minimax(board: chess.Board, depth: int, alpha: int, beta: int, maximizing: bool, perspective: chess.Color) -> int:
    if depth == 0 or board.is_game_over():
        return evaluate_board(board, perspective)

    legal_moves = list(board.legal_moves)
    if maximizing:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False, perspective)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True, perspective)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def find_best_move(board: chess.Board, depth: int = 3) -> chess.Move:
    """Returns the best move found using minimax search."""
    best_move = None
    best_value = float('-inf')
    perspective = board.turn  # Keep this constant

    for move in board.legal_moves:
        board.push(move)
        value = minimax(board, depth - 1, float('-inf'), float('inf'), False, perspective)
        board.pop()

        if value > best_value:
            best_value = value
            best_move = move

    return best_move
