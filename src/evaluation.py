import chess

# Constant piece values
PAWN_VALUE = 100
BISHOP_VALUE = 300
KNIGHT_VALUE = 300
ROOK_VALUE = 500
QUEEN_VALUE = 900

# Piece square tables
pawns_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

knights_table = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

bishops_table = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

rooks_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

queens_table = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

king_middle_table = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

king_end_table = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

def evaluate(board):
    if board.is_checkmate():
        return -99999

    elif board.is_stalemate():
        return 0

    else:
        turn = board.turn

        white_eval = 0
        black_eval = 0

        white_material = count_material(board, chess.WHITE)
        black_material = count_material(board, chess.BLACK)

        white_eval += white_material
        black_eval += black_material

        white_eval += count_piece_square_tables(board, chess.WHITE)
        black_eval += count_piece_square_tables(board, chess.BLACK)

        evaluation = white_eval - black_eval
        
        return (evaluation * 1) if turn == chess.WHITE else (evaluation * -1)
        

def count_piece_square_tables(board, turn):
    value = 0
    is_white = True

    if (turn == chess.BLACK): 
        is_white = False
    
    value += evaluate_piece_square_table(pawns_table, board.pieces(chess.PAWN, turn), is_white)
    value += evaluate_piece_square_table(pawns_table, board.pieces(chess.KNIGHT, turn), is_white)
    value += evaluate_piece_square_table(pawns_table, board.pieces(chess.BISHOP, turn), is_white)
    value += evaluate_piece_square_table(pawns_table, board.pieces(chess.ROOK, turn), is_white)
    value += evaluate_piece_square_table(pawns_table, board.pieces(chess.QUEEN, turn), is_white)
    value += evaluate_piece_square_table(pawns_table, board.pieces(chess.KING, turn), is_white)

    return value
    

def evaluate_piece_square_table(table, piece_squares, is_white):
    value = 0
    for square in piece_squares:
        value += read_piece_square_table(table, square, is_white)

    return value

def read_piece_square_table(table, square, is_white):
    if is_white:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        rank = 7 - rank
        square = rank * 8 + file
    
    return table[square]



def count_material(board, color):
    material = 0

    material += chess.popcount(board.pieces(chess.PAWN, color)) * PAWN_VALUE
    material += chess.popcount(board.pieces(chess.KNIGHT, color)) * KNIGHT_VALUE
    material += chess.popcount(board.pieces(chess.BISHOP, color)) * BISHOP_VALUE
    material += chess.popcount(board.pieces(chess.ROOK, color)) * ROOK_VALUE
    material += chess.popcount(board.pieces(chess.QUEEN, color)) * QUEEN_VALUE

    return material