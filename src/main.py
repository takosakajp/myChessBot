import chess
from search import find_best_move


board = chess.Board()

while not board.is_game_over():
    print(board)
    if board.turn:
        move = find_best_move(board, depth=3)
        print(f"Bot plays: {move}")
    else:
        move = input("Your move: ")
        move = chess.Move.from_uci(move)

    if move in board.legal_moves:
        board.push(move)
    else:
        print("Illegal move. Try again.")
