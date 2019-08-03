class Tile:
  def __init__(self):
    self.directions = []
    self.accesses = [[]]  # List of player id for each direction
    self.rethrow = False
    self.safe = False
    self.start = False
    self.finish = False
