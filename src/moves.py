import chess

PT = {
    chess.Piece(chess.PAWN, chess.WHITE) : 0,
    chess.Piece(chess.KNIGHT, chess.WHITE) : 1,
    chess.Piece(chess.BISHOP, chess.WHITE) : 2,
    chess.Piece(chess.ROOK, chess.WHITE) : 3,
    chess.Piece(chess.QUEEN, chess.WHITE) : 4,
    chess.Piece(chess.KING, chess.WHITE) : 5,

    chess.Piece(chess.PAWN, chess.BLACK) : 6,
    chess.Piece(chess.KNIGHT, chess.BLACK) : 7,
    chess.Piece(chess.BISHOP, chess.BLACK) : 8,
    chess.Piece(chess.ROOK, chess.BLACK) : 9,
    chess.Piece(chess.QUEEN, chess.BLACK) : 10,
    chess.Piece(chess.KING, chess.BLACK) : 11,
}

# MVV LVA [attacker][victim]
mvv_lva = [
 	[105, 205, 305, 405, 505, 605,  105, 205, 305, 405, 505, 605],
	[104, 204, 304, 404, 504, 604,  104, 204, 304, 404, 504, 604],
	[103, 203, 303, 403, 503, 603,  103, 203, 303, 403, 503, 603],
	[102, 202, 302, 402, 502, 602,  102, 202, 302, 402, 502, 602],
	[101, 201, 301, 401, 501, 601,  101, 201, 301, 401, 501, 601],
	[100, 200, 300, 400, 500, 600,  100, 200, 300, 400, 500, 600],

	[105, 205, 305, 405, 505, 605,  105, 205, 305, 405, 505, 605],
	[104, 204, 304, 404, 504, 604,  104, 204, 304, 404, 504, 604],
	[103, 203, 303, 403, 503, 603,  103, 203, 303, 403, 503, 603],
	[102, 202, 302, 402, 502, 602,  102, 202, 302, 402, 502, 602],
	[101, 201, 301, 401, 501, 601,  101, 201, 301, 401, 501, 601],
	[100, 200, 300, 400, 500, 600,  100, 200, 300, 400, 500, 600]
]

class Move:
    def __init__(self, move, score):
        self.move = move
        self.score = score

def make_move(board, move):
    board.push(chess.Move.from_uci(move.uci()))
    
def unmake_move(board):
    board.pop()

def sort_moves(board, moveList):
    move_scores = []

    # score each move and add to move_scores
    for move in moveList:
        move_scores.append(score_move(board, move))

    # sort moves based on score
    for move in range(0, len(moveList)):
        for next_move in range(move + 1, len(moveList)):
            if move_scores[move] < move_scores[next_move]:
                # swap scores
                temp_score = move_scores[move]
                move_scores[move] = move_scores[next_move]
                move_scores[next_move] = temp_score

                # swap moves
                temp_move = moveList[move]
                moveList[move] = moveList[next_move]
                moveList[next_move] = temp_move


    

def score_move(board, move):
    # assign score to move
    move_score = 0
    if (board.is_capture(move)):
        if board.is_en_passant(move):
            op_color = chess.BLACK if board.turn==chess.WHITE else chess.WHITE
            move_score = mvv_lva[PT[chess.Piece(chess.PAWN, board.turn)]][PT[chess.Piece(chess.PAWN, op_color)]] + 1000
        else:
            move_score = mvv_lva[PT[board.piece_at(move.from_square)]][PT[board.piece_at(move.to_square)]] + 1000

    return move_score