import chess
from search import find_best_move


def get_player_color() -> chess.Color:
    """Prompt the user to choose white or black."""
    while True:
        choice = input("Choose your color (white/black): ").strip().lower()
        if choice == "white" or choice == "w":
            return chess.WHITE
        elif choice == "black" or choice == "b":
            return chess.BLACK
        else:
            print("Invalid choice. Please type 'white' or 'black'.")


def get_human_move(board: chess.Board) -> chess.Move:
    """Get a valid move from the human player using either UCI or SAN."""
    while True:
        move_input = input("Your move (UCI or SAN): ").strip()
        try:
            # Try UCI format first
            move = chess.Move.from_uci(move_input)
            if move in board.legal_moves:
                return move
        except:
            pass

        try:
            # Try SAN (Standard Algebraic Notation)
            move = board.parse_san(move_input)
            return move
        except:
            print("Invalid move format or illegal move. Try again.")


def play_game():
    board = chess.Board()
    player_color = get_player_color()

    while not board.is_game_over():
        # print(board, "\n")
        if board.turn == player_color:
            move = get_human_move(board)
        else:
            move = find_best_move(board, depth=3)
            print(f"Bot plays: {move.uci()}")

        board.push(move)

    print("\nGame Over:", board.result())
    print(board)


if __name__ == "__main__":
    play_game()
