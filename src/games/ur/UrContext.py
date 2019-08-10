from src.common.Context import Context
from src.games.ur.Options import Options
from src.games.ur.Player import Player
from src.games.ur.read_board import read_board
from src.games.ur.draw_board import *


class UrContext(Context):
  options: Options
  players: List[Player]
  board: List[List[Tile]]

  def __init__(self, options):
    self.options = options
    self.nb_players = 0
    self.nb_tokens_per_player = 0
    self.players = []
    self.board = []
    self.board_size = Vec2(0, 0)
    players_starts, players_finishes = read_board(self, options.board_filename)
    for i in range(self.nb_players):
      self.players.append(Player(i, self.nb_tokens_per_player, players_starts[i], players_finishes[i]))

    self.draw_tile_size = Vec2(5, 9)
    # The first rectangle is drawn in full but the others share one side
    draw_space_size = Vec2(self.draw_tile_size.y + (self.board_size.y - 1) * (self.draw_tile_size.y - 1),
                           self.draw_tile_size.x + (self.board_size.x - 1) * (self.draw_tile_size.x - 1))
    super().__init__(draw_space_size)

  def draw(self):
    draw_board(self, True, [Vec2(2, 1)])
    draw_tile_properties(self)
    print_ctx(self)
    self.clr()

    draw_board(self, False, [])
    draw_players_directions(self, [0, 1])
    print_ctx(self)
    self.clr()

    draw_board(self, True, [])
    draw_players_tokens(self, [0, 1])
    print_ctx(self)
    self.clr()
