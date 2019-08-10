from typing import List

from src.common import Vec2
from src.common.ColoredChar import ColoredChar


class Context:
  draw_space: List[List[ColoredChar]]

  def __init__(self, draw_space_size: Vec2):
    self.draw_space_size = draw_space_size
    self.draw_space = []
    for y in range(self.draw_space_size.y):
      line = []
      for x in range(self.draw_space_size.x):
        line.append(ColoredChar())
      self.draw_space.append(line)

  def clr(self):
    for line in self.draw_space:
      for x in range(self.draw_space_size.x):
        line[x] = ColoredChar()
