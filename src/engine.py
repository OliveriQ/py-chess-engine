import chess
from opening import opening_book
from tablebase import tablebase
from search import root_search, nodes
from timeit import default_timer as timer


board = chess.Board("6k1/5R2/3N4/3B4/6P1/P5P1/P1P2K2/4R3 w - - 9 44")

def search(board):
    book_move = opening_book(board, "openings.bin")
    if (book_move[0] == None):
        if (tablebase(board) == None):
            return root_search(board, 4)
        else: 
            return tablebase(board)
    else:
        return book_move[0]

print(board)

start = timer()
best_move = search(board)
end = timer()

print("Best move: ", best_move) 
print("Nodes: ", nodes)
print("Time: ", end - start)
