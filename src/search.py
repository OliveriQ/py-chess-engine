from moves import make_move, unmake_move, sort_moves
from evaluation import evaluate

nodes = 0

def quiescence(board, alpha, beta, depth):
    global nodes

    pos_eval = evaluate(board, depth)

    if (pos_eval >= beta):
        return beta

    if (alpha < pos_eval):
        alpha = pos_eval

    capture_moves = list(board.generate_legal_captures())

    sort_moves(board, capture_moves)

    for move in capture_moves:
        nodes += 1
        make_move(board, move)
        score = -quiescence(board, -beta, -alpha, depth)
        unmake_move(board)

        if score >= beta:
            return beta
        
        if score > alpha:
            alpha = score
    
    return alpha

def negamax(board, alpha, beta, depth):
    global nodes

    if depth == 0 or board.is_game_over() or board.is_repetition():
        return quiescence(board, alpha, beta, depth)

    max = -99999
    moveList = list(board.legal_moves)

    sort_moves(board, moveList)

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

    sort_moves(board, moveList)

    for move in moveList:
        nodes += 1
        print("Move: ", move)
        make_move(board, move)
        score = -negamax(board, -99999, 99999, depth - 1)
        unmake_move(board)
        print("Score: ", score)
        print("\n")
        if (score > max):
            max = score
            best_move = move

    return best_move