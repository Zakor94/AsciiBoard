from enum import Enum
from src.common.Vec2 import Vec2


class Direction(Enum):
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3


DIRECTION_TO_VEC = {
  Direction.UP: Vec2(-1, 0),
  Direction.DOWN: Vec2(1, 0),
  Direction.LEFT: Vec2(0, -1),
  Direction.RIGHT: Vec2(0, 1)
}
