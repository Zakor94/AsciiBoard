from src.common.Direction import Direction
from src.common.Vec2 import Vec2
from src.games.ur.Tile import Tile

DIRECTIONS = {
  'u': Direction.UP,
  'd': Direction.DOWN,
  'l': Direction.LEFT,
  'r': Direction.RIGHT
}


def read_board(ctx, board_filename):
  with open(board_filename) as f:
    lines = f.readlines()
  err_str = f"Error when loading board '{board_filename}'"
  if len(lines) < 3:
    raise RuntimeError(f"{err_str}: Not enough lines.")
  header_lines_idx = 0

  def read_value(name, value_type):
    nonlocal header_lines_idx
    split = lines[header_lines_idx].split('=')
    header_lines_idx += 1
    if split[0] != name:
      raise RuntimeError(f"{err_str}: : Expected attribute '{name}' but got '{split[0]}'.")
    try:
      return value_type(split[1])
    except ValueError:
      raise RuntimeError(f"{err_str}: : Could not convert attribute '{name}' '{split[1]}' to type {value_type}.")

  ctx.nb_players = read_value("nb_players", int)
  ctx.nb_tokens_per_player = read_value("nb_tokens_per_player", int)

  def read_access(_attr, _loc_attr_str):
    try:
      _access = int(_attr)
      if _access >= ctx.nb_players:
        raise RuntimeError(f"{err_str}: Player id {_access} is greater than maximum number of player {ctx.nb_players} "
                           f"at {_loc_attr_str}")
    except ValueError:
      _access = None
    return _access

  def append_start_finish(_tile, dic, pos, _loc_attr_str):
    if _tile.rethrow or _tile.safe or (_tile.finish and _tile.start):
      raise RuntimeError(f"{err_str}: Tile cannot have other attributes than start or finish at {_loc_attr_str}")
    for a in _tile.accesses:
      for player_id in a:
        if player_id in dic:
          dic[player_id].append(pos)
        else:
          dic[player_id] = [pos]

  players_starts = {}
  players_finishes = {}
  ctx.board = []
  ctx.board_size.y = len(lines) - header_lines_idx
  for row in range(ctx.board_size.y):
    line_idx = row + header_lines_idx
    line = lines[line_idx]
    line_split = line.split(';')
    ctx.board.append([])
    ctx.board_size.x = max(ctx.board_size.x, len(line_split))
    for col in range(len(line_split)):
      if not line_split[col]:
        ctx.board[row].append(None)
      tile_split = line_split[col].split(',')
      loc_str = f"row={line_idx}, col={col}"
      tile = Tile()
      # Read first direction and access
      attr = tile_split[0].strip()
      direction = DIRECTIONS.get(attr)
      loc_attr_str = f"{loc_str}, attr=0"
      if not direction:
        raise RuntimeError(f"{err_str}: Expected direction but got '{attr}' at {loc_attr_str}")
      tile.directions.append(direction)
      attr = tile_split[1].strip()
      loc_attr_str = f"{loc_str}, attr=1"
      access = read_access(attr, loc_attr_str)
      if access is None:
        raise RuntimeError(f"{err_str}: Expected player id but got '{attr}' at {loc_attr_str}")
      tile.accesses[0].append(access)
      # Read more attributes
      for attr_idx in range(2, len(tile_split)):
        loc_attr_str = f"{loc_str}, attr={attr_idx}"
        attr = tile_split[attr_idx].strip()
        direction = DIRECTIONS.get(attr)
        if direction:
          if not tile.accesses[len(tile.directions) - 1]:
            raise RuntimeError(f"{err_str}: Expected player id but got '{attr}' at {loc_attr_str}")
          tile.directions.append(direction)
          tile.accesses.append([])
          continue
        access = read_access(attr, loc_attr_str)
        if access is not None:
          tile.accesses[len(tile.directions) - 1].append(access)
          continue
        if not tile.accesses[len(tile.directions) - 1]:
          raise RuntimeError(f"{err_str}: Expected player id but got '{attr}' at {loc_attr_str}")
        if attr == "rethrow":
          tile.rethrow = True
          continue
        if attr == "safe":
          tile.safe = True
          continue
        if attr == "start":
          tile.start = True
          append_start_finish(tile, players_starts, Vec2(row, col), loc_attr_str)
          continue
        if attr == "finish":
          tile.finish = True
          append_start_finish(tile, players_finishes, Vec2(row, col), loc_attr_str)
          continue
        raise RuntimeError(f"{err_str}: Unknown attribute '{attr}' at {loc_attr_str}")
      ctx.board[row].append(tile)
  # Add None to make each row the same length
  for row in range(ctx.board_size.y):
    while len(ctx.board[row]) < ctx.board_size.x:
      ctx.board[row].append(None)
  return players_starts, players_finishes
