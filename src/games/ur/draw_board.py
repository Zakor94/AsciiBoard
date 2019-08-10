from typing import Callable
from src.common.draw_utils import *
from src.common.Direction import *
from src.games.ur.Tile import Tile

_TILE_START = 'S'
_TILE_FINISH = 'F'
_TILE_SAFE = 'X'
_TILE_RETHROW = 'R'
_TILE_SAFE_RETHROW = 'O'
_TILE_TOO_MANY_PLAYERS = '?'

_DIRECTION_TO_ASCII = {
  Direction.UP: '^',
  Direction.DOWN: '˅',
  Direction.LEFT: '<',
  Direction.RIGHT: '>'
}


def _gen_draw_board(ctx, func: Callable[[Tile, Vec2, Vec2, Vec2], None]):
  tile_size_m1 = ctx.draw_tile_size - [1, 1]
  tile_draw_center_offset = ctx.draw_tile_size // 2
  for row in range(ctx.board_size.y):
    pos_y = tile_size_m1.y * row
    tile_row = ctx.board[row]
    for col in range(ctx.board_size.x):
      tile = tile_row[col]
      if tile is not None:
        tile_draw_pos = Vec2(pos_y, tile_size_m1.x * col)
        tile_draw_center = tile_draw_pos + tile_draw_center_offset
        func(tile, Vec2(row, col), tile_draw_pos, tile_draw_center)


def _tile_to_cc(tile: Tile) -> ColoredChar:
  if tile.start:
    return ColoredChar(_TILE_START, 'green')
  if tile.finish:
    return ColoredChar(_TILE_FINISH, 'red')
  if tile.safe and tile.rethrow:
    return ColoredChar(_TILE_SAFE_RETHROW, 'cyan')
  if tile.safe:
    return ColoredChar(_TILE_SAFE, 'blue')
  if tile.rethrow:
    return ColoredChar(_TILE_RETHROW, 'yellow')
  return ColoredChar()


def draw_board(ctx, color_tile_properties: bool, possible_moves: List[Vec2]):
  """
  Draw the board.
  :param ctx:
  :param color_tile_properties: whether to draw the tile properties as colors on the vertical and horizontal bars of the
                                tile.
  :param possible_moves: list of tile's position which corners will be drawn in color.
  """

  def draw_func(tile, tile_pos, tile_draw_pos, _tile_draw_center):
    edge_color = None
    corner_color = None
    corner_attrs = []
    if color_tile_properties:
      edge_color = _tile_to_cc(tile).color
      if tile_pos in possible_moves:
        corner_color = 'magenta'
        corner_attrs = ['bold']
    draw_rect(ctx, tile_draw_pos, ctx.draw_tile_size, edge_color=edge_color, corner_color=corner_color,
              corner_attrs=corner_attrs)

  _gen_draw_board(ctx, draw_func)


def draw_tile_properties(ctx):
  """
  Draw the tile properties as a symbol in the center of the tile.
  :param ctx:
  """

  def draw_func(tile, _tile_pos, _tile_draw_pos, tile_draw_center):
    unchecked_draw(ctx, tile_draw_center, _tile_to_cc(tile))

  _gen_draw_board(ctx, draw_func)


def draw_players_directions(ctx, players_id: List[int]):
  """
  Draw up to 4 directions in a tile that at list one player in the given list can take.
  :param ctx:
  :param players_id: list of players id to draw directions for.
  """

  def draw_func(tile, _tile_pos, _tile_draw_pos, tile_draw_center):
    directions = []
    for d in tile.directions:
      d_idx = tile.directions.index(d)
      for p_id in players_id:
        if p_id in tile.accesses[d_idx]:
          directions.append(d)
          break
    if len(directions) == 1:
      d = directions[0]
      accesses = tile.accesses[tile.directions.index(d)]
      color = ctx.options.get_player_color(accesses[0]) if len(accesses) == 1 else None
      unchecked_draw(ctx, tile_draw_center, ColoredChar(_DIRECTION_TO_ASCII.get(d), color))
    else:
      for d in directions:
        accesses = tile.accesses[tile.directions.index(d)]
        color = ctx.options.get_player_color(accesses[0]) if len(accesses) == 1 else None
        unchecked_draw(ctx, tile_draw_center + DIRECTION_TO_VEC.get(d), ColoredChar(_DIRECTION_TO_ASCII.get(d), color))

  _gen_draw_board(ctx, draw_func)


def draw_players_tokens(ctx, players_id: List[int]):
  """
  Draw position of all given players' tokens
  :param ctx:
  :param players_id: list of players id whose tokens to draw
  """

  def draw_func(_tile, tile_pos, _tile_draw_pos, tile_draw_center):
    player_nb_token_pairs = []
    for p_id in players_id:
      p = ctx.players[p_id]
      nb_tokens = p.tokens.count(tile_pos)
      if nb_tokens > 0:
        player_nb_token_pairs.append((p_id, nb_tokens))
    pair_count = len(player_nb_token_pairs)
    if pair_count > 2:
      unchecked_draw(ctx, tile_draw_center, ColoredChar(_TILE_TOO_MANY_PLAYERS))
    else:
      offsets = [Vec2(0, 0)] if pair_count == 1 else [Vec2(0, -1), Vec2(0, 1)]
      for i in range(pair_count):
        player_id = player_nb_token_pairs[i][0]
        nb_token = player_nb_token_pairs[i][1]
        unchecked_draw(ctx, tile_draw_center + offsets[i],
                       ColoredChar(str(nb_token), ctx.options.get_player_color(player_id)))

  _gen_draw_board(ctx, draw_func)
