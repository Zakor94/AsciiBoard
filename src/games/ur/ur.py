from src.games.ur.Context import *
from src.games.common.draw_utils import print_draw_space


def run():
  ctx = Context("src/games/ur/boards/default_board.txt")
  ctx.draw()
  print_draw_space(ctx.draw_space)
  input("")
