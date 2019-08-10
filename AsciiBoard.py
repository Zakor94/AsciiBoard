#!/usr/bin/python3
import colorama

from src.games.ur import ur


def main():
  # Colorama is needed for Windows to support color ANSI codes
  colorama.init()
  ur.run()


if __name__ == "__main__":
  main()
