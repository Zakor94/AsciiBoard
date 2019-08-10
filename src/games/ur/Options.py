class Options:
  def __init__(self):
    self.board_filename = ''
    self.host_player_color = 'blue'
    self.other_players_color = 'red'
    self.selected_player_id = 0

  def get_player_color(self, player_id: int):
    if self.selected_player_id == player_id:
      return self.host_player_color
    return self.other_players_color
