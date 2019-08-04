from src.games.common.utils import Direction
from src.games.common.Vec2 import Vec2

_HORIZONTAL = '─'
_VERTICAL = '│'


class _DirectionsSet:
  """
  Convert a set of Direction to an int value to have the equivalent of a hashable set.

  Attributes:
    directions: set of Direction
    mask: integer value, last 4 bits represent whether each Direction is present in the set
  """
  def __init__(self, arg):
    if type(arg) is list:
      arg = set(arg)
    if type(arg) is set:
      self.directions = arg
      self.mask = 0
      for direction in arg:
        self.mask += 1 << direction.value
    else:
      self.mask = arg
      self.directions = set()
      for i in reversed(range(4)):
        if arg >= (1 << i):
          self.directions.add(Direction(i))
          arg -= 1 << i


_CORNER_TO_DIRECTIONS = {
  '┌': _DirectionsSet({Direction.DOWN, Direction.RIGHT}).mask,
  '┐': _DirectionsSet({Direction.DOWN, Direction.LEFT}).mask,
  '└': _DirectionsSet({Direction.UP, Direction.RIGHT}).mask,
  '┘': _DirectionsSet({Direction.UP, Direction.LEFT}).mask,
  '├': _DirectionsSet({Direction.UP, Direction.DOWN, Direction.RIGHT}).mask,
  '┤': _DirectionsSet({Direction.UP, Direction.DOWN, Direction.LEFT}).mask,
  '┬': _DirectionsSet({Direction.DOWN, Direction.RIGHT, Direction.LEFT}).mask,
  '┴': _DirectionsSet({Direction.UP, Direction.RIGHT, Direction.LEFT}).mask,
  '┼': _DirectionsSet({Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT}).mask
}

_DIRECTIONS_TO_CORNER = {v: k for k, v in _CORNER_TO_DIRECTIONS.items()}


def _is_pos_valid(draw_space, pos):
  return 0 <= pos.y < len(draw_space) and 0 <= pos.x < len(draw_space[pos.y])


def check_draw(draw_space, pos, c, allow_out_of_bounds=False):
  if not _is_pos_valid(draw_space, pos):
    if allow_out_of_bounds:
      return
    else:
      raise RuntimeError(f"Cannot draw '{c}' at {pos}")
  draw_space[pos.y][pos.x] = c


def _draw_corner(draw_space, pos, directions, allow_out_of_bounds):
  """
  Draw a corner in the draw_space
  :param draw_space: list of list of char, where to draw
  :param pos: Vec2
  :param directions: set of Directions, represents how many lines to draw and their direction
  :param allow_out_of_bounds: if True, will not raise any exception if trying to draw outside of draw_space
  """
  if not _is_pos_valid(draw_space, pos):
    if allow_out_of_bounds:
      return
    else:
      raise RuntimeError(f"Cannot draw corner at {pos}")
  existing_directions = _DirectionsSet(_CORNER_TO_DIRECTIONS.get(draw_space[pos.y][pos.x], 0)).directions
  dirs = directions.union(existing_directions)
  draw_space[pos.y][pos.x] = _DIRECTIONS_TO_CORNER[_DirectionsSet(dirs).mask]


def draw_rect(draw_space, pos, size, allow_out_of_bounds=False):
  """
  Draw the contour of a rectangle
  :param draw_space: list of list of char, where to draw
  :param pos: Vec2, upper left origin of the rectangle
  :param size: Vec2
  :param allow_out_of_bounds: if True, will not raise any exception if trying to draw outside of draw_space
  """
  size = size - [1, 1]
  _draw_corner(draw_space, pos, {Direction.DOWN, Direction.RIGHT}, allow_out_of_bounds)
  _draw_corner(draw_space, Vec2(pos.y, pos.x + size.x), {Direction.DOWN, Direction.LEFT}, allow_out_of_bounds)
  _draw_corner(draw_space, pos + size, {Direction.UP, Direction.LEFT}, allow_out_of_bounds)
  _draw_corner(draw_space, Vec2(pos.y + size.y, pos.x), {Direction.UP, Direction.RIGHT}, allow_out_of_bounds)
  for i in range(1, size.x):
    check_draw(draw_space, Vec2(pos.y, pos.x + i), _HORIZONTAL, allow_out_of_bounds)
    check_draw(draw_space, Vec2(pos.y + size.y, pos.x + i), _HORIZONTAL, allow_out_of_bounds)
  for i in range(1, size.y):
    check_draw(draw_space, Vec2(pos.y + i, pos.x), _VERTICAL, allow_out_of_bounds)
    check_draw(draw_space, Vec2(pos.y + i, pos.x + size.x), _VERTICAL, allow_out_of_bounds)


def print_draw_space(draw_space):
  for line in draw_space:
    print(''.join(line))
