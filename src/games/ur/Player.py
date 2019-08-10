from typing import List

from src.common.Vec2 import Vec2


class Player:
  tokens: List[Vec2]

  def __init__(self, idx: int, nb_tokens: int, starts: List[Vec2], finishes: List[Vec2]):
    self.idx = idx
    self.tokens = [starts[0]] * nb_tokens
    self.starts = starts
    self.finishes = finishes
