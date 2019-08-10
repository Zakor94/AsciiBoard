from typing import List
from termcolor import cprint


class ColoredChar:
  def __init__(self, char: str = ' ', color: str = None, attrs: List[str] = None):
    self.char = char
    self.color = color
    self.attrs = list(attrs) if attrs else []

  def print(self):
    cprint(self.char, self.color, attrs=self.attrs, end='')
