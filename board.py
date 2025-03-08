import texttable
class PlanesError(Exception):
    pass

class GameOver(PlanesError):
    pass
class Board:
    def __init__ (self, size):
        self._size = size
        self._board = [' '] * size * size
        self._head_hits = 3

    @property
    def get_size(self):
        return self._size

    def get_board(self):
        return self._board

    def is_empty(self, row, column):
        """
        checks if a space is empty
        :param row: int
        :param column: int
        :return: true or false
        """
        return self._board[row* self._size + column] == ' '


    def place_plane(self, row, column, alignment, symbol):
        """
        Places a plane based on the coordinates of its head, its alignment, and symbol, if all the spaces needed  are valid

        :param row: int
        :param column: int
        :param alignment: string
        :param symbol: int (1,3,5)
        :return: -
        :raises: PlaneErrors if the row or column values won't allow the placement, or if the position overlaps an existing plane
        """
        if alignment == "up":
            if not (0 <= row <= self._size - 4) or not (2 <= column <= self._size - 3):
                raise PlanesError("Invalid placement!")
            if not self.is_empty(row, column):
                raise PlanesError("Invalid placement!")
            positions = [(row + i, column + j) for i, j in [ (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (2, 0), (3, -1), (3, 0), (3, 1)]]
            if any(not self.is_empty(r,c) for r,c in positions):
                raise PlanesError("Invalid placement! Planes shouldn't overlap!")
            self._board[row * self._size + column] = symbol
            for r,c in positions:
                self._board[r*self._size +c] = symbol +1
        if alignment == "down":
            if not (3 <= row <= self._size-1) or not (2 <= column <= self._size - 3):
                raise PlanesError("Invalid placement!")
            if not self.is_empty(row, column):
                raise PlanesError("Invalid placement!")
            positions = [(row - i, column + j) for i, j in [(1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (2, 0), (3, -1), (3, 0), (3, 1)]]
            if any(not self.is_empty(r, c) for r, c in positions):
                raise PlanesError("Invalid placement! Planes shouldn't overlap!")
            self._board[row * self._size + column] = symbol
            for r, c in positions:
                self._board[r * self._size + c] = symbol + 1

        elif alignment == "left":
            if not (2 <= row <= self._size - 3) or not (0 <= column <= self._size - 4):
                raise PlanesError("Invalid placement!")
            if not self.is_empty(row, column):
                raise PlanesError("Invalid placement!")
            positions = [(row + i, column + j) for i, j in [(-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (0, 2), (-1, 3), (0, 3), (1, 3)]]
            if any(not self.is_empty(r, c) for r, c in positions):
                raise PlanesError("Invalid placement! Planes shouldn't overlap!")
            self._board[row * self._size + column] = symbol
            for r, c in positions:
                self._board[r * self._size + c] = symbol + 1

        elif alignment == "right":
            if not (2 <= row <= self._size - 3) or not (3 <= column <= self._size - 1):
                raise PlanesError("Invalid placement!")
            if not self.is_empty(row, column):
                raise PlanesError("Invalid placement!")
            positions = [(row + i, column - j) for i, j in [(-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (0, 2), (-1, 3), (0, 3), (1, 3)]]
            if any(not self.is_empty(r, c) for r, c in positions):
                raise PlanesError("Invalid placement! Planes shouldn't overlap!")
            self._board[row * self._size + column] = symbol
            for r, c in positions:
                self._board[r * self._size + c] = symbol + 1

    def __str__(self):
      raise NotImplementedError()

    def hit(self, row, column):
        """
        Places a shot on the board, if possible, based on row and column
        "-" miss
        "X" non-head hit
        "!" head hit - the entire plane is revealed as shot down
        :param row: int
        :param column: int
        :return: 1, if a part of a plane (except its head) is hit
                2, for a head hit
                3, for a miss
                raises GameOver if all heads of the planes were hit
        """
        if not(0 <= row < self._size) or not(0 <= column < self._size):
            raise PlanesError("Invalid square coordinates!")
        if self._board[row*self._size + column] in ('-', 'X', '!'):
            raise PlanesError("Square already attacked!")
        if self._board[row* self._size + column] in (2,4,6):
            self._board[row*self._size + column] = 'X'
            return 1
        elif self._board[row* self._size + column] in (1,3,5):
            self._head_hits -= 1
            for i in range(self._size*self._size):
                if self._board[i] == self._board[row * self._size + column] + 1:
                    self._board[i] = 'X'
            self._board[row*self._size + column] = '!'
            if self._head_hits == 0:
                raise GameOver()
            return 2
        else:
            self._board[row * self._size + column] = '-'
            return 3

class PlayerBoard(Board):
    def __str__(self):
        t = texttable.Texttable()
        header = ['/']
        for i in range (self._size):
            header.append(chr(ord('A') + i))
        t.header(header)
        for i in range(0, self._size ** 2, self._size):
            t.add_row([ i // self._size + 1] + self._board[i:i + self._size])
        return t.draw()



class TargetBoard(Board):
    def __str__(self):
        t = texttable.Texttable()
        t_board = [' ' if p in (1,2,3,4,5,6) else p for p in self._board]
        header = ['/']
        for i in range (self._size):
            header.append(chr(ord('A') + i))
        t.header(header)
        for i in range(0, self._size ** 2, self._size):
            t.add_row([ i // 10 + 1] + t_board[i:i + self._size])

        return t.draw()




