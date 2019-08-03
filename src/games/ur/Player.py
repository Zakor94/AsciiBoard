class Player:
  def __init__(self, id_, nb_pieces, starts, finishes):
    self.id = id_
    self.pieces = [None] * nb_pieces
    self.starts = starts
    self.finishes = finishes
