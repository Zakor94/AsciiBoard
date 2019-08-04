from src.games.common.Vec2 import Vec2
from src.games.common.draw_utils import *


_TILE_START = 'S'
_TILE_FINISH = 'F'
_TILE_SAFE = 'X'
_TILE_RETHROW = 'R'
_TILE_SAFE_RETHROW = 'O'


def draw_board(ctx):
  tile_size_m1 = ctx.draw_tile_size - [1, 1]
  tile_center_offset = ctx.draw_tile_size // 2
  for row in range(ctx.board_size.y):
    pos_y = tile_size_m1.y * row
    tile_row = ctx.board[row]
    for col in range(ctx.board_size.x):
      tile = tile_row[col]
      if tile is not None:
        tile_pos = Vec2(pos_y, tile_size_m1.x * col)
        draw_rect(ctx.draw_space, tile_pos, ctx.draw_tile_size)
        tile_center = tile_pos + tile_center_offset
        if tile.start:
          check_draw(ctx.draw_space, tile_center, _TILE_START)
        elif tile.finish:
          check_draw(ctx.draw_space, tile_center, _TILE_FINISH)
        elif tile.safe and tile.rethrow:
          check_draw(ctx.draw_space, tile_center, _TILE_SAFE_RETHROW)
        elif tile.safe:
          check_draw(ctx.draw_space, tile_center, _TILE_SAFE)
        elif tile.rethrow:
          check_draw(ctx.draw_space, tile_center, _TILE_RETHROW)
