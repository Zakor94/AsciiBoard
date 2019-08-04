from src.games.common.Vec2 import Vec2
from src.games.ur.Player import Player
from src.games.ur.read_board import read_board
from src.games.ur.draw_board import draw_board


class Context:
  def __init__(self, board_filename):
    self.nb_players = 0
    self.nb_pieces_per_player = 0
    self.players = []
    self.board = []
    self.board_size = Vec2(0, 0)
    players_starts, players_finishes = read_board(self, board_filename)
    for i in range(self.nb_players):
      self.players.append(Player(i, self.nb_pieces_per_player, players_starts[i], players_finishes[i]))
    self.draw_tile_size = Vec2(3, 5)
    # The first rectangle is drawn in full but the others share one side
    self.draw_space_size = Vec2(self.draw_tile_size.y + (self.board_size.y - 1) * (self.draw_tile_size.y - 1),
                                self.draw_tile_size.x + (self.board_size.x - 1) * (self.draw_tile_size.x - 1))
    self.draw_space = []
    for i in range(self.draw_space_size.y):
      self.draw_space.append([' '] * self.draw_space_size.x)

  def draw(self):
    draw_board(self)
