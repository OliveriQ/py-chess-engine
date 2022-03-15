import chess
from opening import opening_book
from tablebase import tablebase
from search import root_search, nodes
from timeit import default_timer as timer


board = chess.Board("n4rk1/5pp1/1q6/6NQ/8/8/5PPP/5RK1 b - - 0 1")

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
