from typing import Set

from src.common.Direction import Direction
from src.common.Vec2 import Vec2
from src.common.ColoredChar import *

_HORIZONTAL = '─'
_VERTICAL = '│'


class _DirectionsSet:
  """
  Convert a set of Direction to an int value to have the equivalent of a hashable set.

  Attributes:
    directions: set of Direction
    mask: integer value, last 4 bits represent whether each Direction is present in the set
  """
  mask: int
  directions: Set[Direction]

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


def _is_pos_valid(ctx, pos: Vec2, allow_out_of_bounds: bool):
  if not 0 <= pos.y < ctx.draw_space_size.y and 0 <= pos.x < ctx.draw_space_size.x:
    if allow_out_of_bounds:
      return False
    else:
      raise RuntimeError(f"Cannot draw at {pos}")
  return True


def unchecked_draw(ctx, pos: Vec2, cc: ColoredChar):
  ctx.draw_space[pos.y][pos.x] = cc


def unchecked_draw_merge_color_and_attrs(ctx, pos: Vec2, cc: ColoredChar):
  act_cc = ctx.draw_space[pos.y][pos.x]
  act_cc.char = cc.char
  act_cc.attrs.extend(cc.attrs)
  if cc.color:
    if not act_cc.color:
      act_cc.color = cc.color
    elif act_cc.color != cc.color:
      act_cc.color = None


def checked_draw(ctx, pos: Vec2, cc: ColoredChar, allow_out_of_bounds=False):
  if _is_pos_valid(ctx, pos, allow_out_of_bounds):
    unchecked_draw(ctx, pos, cc)


def checked_draw_merge_color_and_attrs(ctx, pos: Vec2, cc: ColoredChar, allow_out_of_bounds=False):
  if _is_pos_valid(ctx, pos, allow_out_of_bounds):
    unchecked_draw_merge_color_and_attrs(ctx, pos, cc)


def _draw_corner(ctx, pos: Vec2, directions: Set[Direction], color: str, attrs: List[str], allow_out_of_bounds: bool):
  """
  Draw a corner in the Context's draw_space
  :param ctx: list of list of char, where to draw
  :param pos: Vec2
  :param directions: set of Directions, represents how many lines to draw and their direction
  :param color: overwrite any previous color
  :param allow_out_of_bounds: if True, will not raise any exception if trying to draw outside of draw_space
  """
  if _is_pos_valid(ctx, pos, allow_out_of_bounds):
    existing_directions = _DirectionsSet(_CORNER_TO_DIRECTIONS.get(ctx.draw_space[pos.y][pos.x].char, 0)).directions
    dirs = directions.union(existing_directions)
    cc = ColoredChar(_DIRECTIONS_TO_CORNER[_DirectionsSet(dirs).mask], color, attrs)
    unchecked_draw_merge_color_and_attrs(ctx, pos, cc)


def draw_rect(ctx, pos: Vec2, size: Vec2, *, edge_color: str = None, edge_attrs: List[str] = None,
              corner_color: str = None, corner_attrs: List[str] = None, allow_out_of_bounds: bool = False):
  """
  Draw the contour of a rectangle
  :param ctx:
  :param pos: Vec2, upper left origin of the rectangle
  :param size: Vec2
  :param edge_color: merge with previous color
  :param edge_attrs: append to previous attrs
  :param corner_color: merge with previous color
  :param corner_attrs: merge with previous color
  :param allow_out_of_bounds: if True, will not raise any exception if trying to draw outside of draw_space
  """
  size = size - [1, 1]
  _draw_corner(ctx, pos, {Direction.DOWN, Direction.RIGHT}, corner_color, corner_attrs, allow_out_of_bounds)
  _draw_corner(ctx, Vec2(pos.y, pos.x + size.x), {Direction.DOWN, Direction.LEFT}, corner_color, corner_attrs,
               allow_out_of_bounds)
  _draw_corner(ctx, pos + size, {Direction.UP, Direction.LEFT}, corner_color, corner_attrs, allow_out_of_bounds)
  _draw_corner(ctx, Vec2(pos.y + size.y, pos.x), {Direction.UP, Direction.RIGHT}, corner_color, corner_attrs,
               allow_out_of_bounds)
  for i in range(1, size.x):
    checked_draw_merge_color_and_attrs(ctx, Vec2(pos.y, pos.x + i),
                                       ColoredChar(_HORIZONTAL, edge_color, edge_attrs),
                                       allow_out_of_bounds)
    checked_draw_merge_color_and_attrs(ctx, Vec2(pos.y + size.y, pos.x + i),
                                       ColoredChar(_HORIZONTAL, edge_color, edge_attrs),
                                       allow_out_of_bounds)
  for i in range(1, size.y):
    checked_draw_merge_color_and_attrs(ctx, Vec2(pos.y + i, pos.x),
                                       ColoredChar(_VERTICAL, edge_color, edge_attrs),
                                       allow_out_of_bounds)
    checked_draw_merge_color_and_attrs(ctx, Vec2(pos.y + i, pos.x + size.x),
                                       ColoredChar(_VERTICAL, edge_color, edge_attrs),
                                       allow_out_of_bounds)


def print_ctx(ctx):
  for line in ctx.draw_space:
    for cc in line:
      cc.print()
    print()
