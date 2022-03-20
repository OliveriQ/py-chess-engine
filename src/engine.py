import chess
from opening import opening_book
from tablebase import tablebase
from search import root_search, nodes
from timeit import default_timer as timer


board = chess.Board("3r3r/4k3/1pn4p/5pp1/2P1p3/3N4/PPK2PPP/R3R3 w - - 0 29")

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
