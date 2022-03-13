import chess
from timeit import default_timer as timer


board = chess.Board("r3k2r/p1ppqpb1/Bn2p1p1/3PN3/1p2P3/2N2Q1p/PPPB1PPP/4K2R b Kkq - 0 1")

# Constant piece values
PAWN_VALUE = 1
BISHOP_VALUE = 3
KNIGHT_VALUE = 3
ROOK_VALUE = 5
QUEEN_VALUE = 9

nodes = 0


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

def count_material(board, color):
    material = 0

    material += chess.popcount(board.pieces(chess.PAWN, color)) * PAWN_VALUE
    material += chess.popcount(board.pieces(chess.KNIGHT, color)) * KNIGHT_VALUE
    material += chess.popcount(board.pieces(chess.BISHOP, color)) * BISHOP_VALUE
    material += chess.popcount(board.pieces(chess.ROOK, color)) * ROOK_VALUE
    material += chess.popcount(board.pieces(chess.QUEEN, color)) * QUEEN_VALUE

    return material

def evaluate(board):
    evaluation = count_material(board, chess.WHITE) - count_material(board, chess.BLACK)
    if (board.turn == chess.WHITE):
        return evaluation * 1

    return evaluation * -1

def sort_moves(moveList):
    move_scores = []

    # score each move and add to move_scores
    for move in moveList:
        move_scores.append(score_move(move))

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

    

def score_move(move):
    # assign score to move
    move_score = 0
    if (board.is_capture(move)):
        if board.is_en_passant(move):
            op_color = chess.BLACK if board.turn==chess.WHITE else chess.WHITE
            move_score = mvv_lva[PT[chess.Piece(chess.PAWN, board.turn)]][PT[chess.Piece(chess.PAWN, op_color)]] + 1000
        else:
            move_score = mvv_lva[PT[board.piece_at(move.from_square)]][PT[board.piece_at(move.to_square)]] + 1000

    return move_score


def negamax(board, alpha, beta, depth):
    global nodes

    if depth == 0:
        return evaluate(board)

    max = -99999
    moveList = list(board.legal_moves)

    if len(list(moveList)) == 0:
        if board.is_check():
            return -99999
        return 0

    sort_moves(moveList)

    for move in moveList:
        nodes += 1
        
        make_move(board, move)
        score = -negamax(board, -beta, -alpha, depth-1)
        unmake_move(board)

        if (score > max):
            max = score

        if max > alpha:
            alpha = max

        if (alpha >= beta):
            break

    return max

def root_search(board, depth):
    global nodes

    nodes += 1

    best_move = None

    max = -99999
    moveList = list(board.legal_moves)

    if len(list(moveList)) == 0:
        if board.is_check():
            return -99999     
        return 0

    sort_moves(moveList)

    for move in moveList:
        nodes += 1

        make_move(board, move)
        score = -negamax(board, -99999, 99999, depth - 1)
        unmake_move(board)
        if (score > max):
            max = score
            best_move = move

    return best_move

def search(board):
    return root_search(board, 4)

print(board)

start = timer()
best_move = search(board)
end = timer()

print("Depth: ", 4)
print("Best move: ", best_move) 
print("Nodes: ", nodes)
print("Time: ", end - start)
