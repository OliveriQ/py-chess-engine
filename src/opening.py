import chess.polyglot

def opening_book(board, book):
  best_move = (None, 0)
  with chess.polyglot.open_reader(book) as reader:
    for entry in reader.find_all(board):
      if (entry.weight > best_move[1]):
        best_move = (entry.move, entry.weight)
  
  return best_move