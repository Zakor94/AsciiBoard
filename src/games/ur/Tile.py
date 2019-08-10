from typing import List

from src.common.Direction import Direction


class Tile:
  accesses: List[List[int]]
  directions: List[Direction]

  def __init__(self):
    self.accesses = [[]]
    self.directions = []
    self.rethrow = False
    self.safe = False
    self.start = False
    self.finish = False
