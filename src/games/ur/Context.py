from src.games.ur.Player import Player
from src.games.ur.read_board import read_board


class Context:
  def __init__(self, board_filename):
    self.nb_players = 0
    self.nb_pieces_per_player = 0
    self.players = []
    self.board = []
    players_starts, players_finishes = read_board(self, board_filename)
    for i in range(self.nb_players):
      self.players.append(Player(i, self.nb_pieces_per_player, players_starts[i], players_finishes[i]))
