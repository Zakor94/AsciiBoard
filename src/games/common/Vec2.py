class Vec2:
  def __init__(self, y, x):
    self.y = y
    self.x = x

  def __add__(self, val):
    return Vec2(self.y + val[0], self.x + val[1])

  def __sub__(self, val):
    return Vec2(self.y - val[0], self.x - val[1])

  def __iadd__(self, val):
    self.y = val[0] + self.y
    self.x = val[1] + self.x
    return self

  def __isub__(self, val):
    self.y = self.y - val[0]
    self.x = self.x - val[1]
    return self

  def __truediv__(self, val):
    return Vec2(self.y / val, self.x / val)

  def __floordiv__(self, val):
    return Vec2(self.y // val, self.x // val)

  def __mul__(self, val):
    return Vec2(self.y * val, self.x * val)

  def __itruediv__(self, val):
    self.y /= val
    self.x /= val
    return self

  def __ifloordiv__(self, val):
    self.y //= val
    self.x //= val
    return self

  def __imul__(self, val):
    self.y *= val
    self.x *= val
    return self

  def __getitem__(self, key):
    if key == 0:
      return self.y
    elif key == 1:
      return self.x
    else:
      raise Exception("Invalid key to Vec2")

  def __setitem__(self, key, val):
    if key == 0:
      self.y = val
    elif key == 1:
      self.x = val
    else:
      raise Exception("Invalid key to Vec2")

  def __str__(self):
    return f"({self.y}, {self.x})"

  def e_wise_truediv(self, val):
    return Vec2(self.y / val[0], self.x / val[1])

  def e_wise_floordiv(self, val):
    return Vec2(self.y // val[0], self.x // val[1])

  def e_wise_mul(self, val):
    return Vec2(self.y * val[0], self.x * val[1])
