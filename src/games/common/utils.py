from enum import Enum


class Position:
  def __init__(self, y, x):
    self.y = y
    self.x = x


class Direction(Enum):
  UP = 0
  DOWN = 1
  RIGHT = 2
  LEFT = 3


DIRECTIONS = {
  'u': Direction.UP,
  'd': Direction.DOWN,
  'r': Direction.RIGHT,
  'l': Direction.LEFT,
}
