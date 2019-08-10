from src.games.ur.Options import Options
from src.games.ur.UrContext import UrContext


def run():
  opt = Options()
  opt.board_filename = "src/games/ur/boards/default_board.txt"
  ctx = UrContext(opt)
  ctx.draw()
  input("")
