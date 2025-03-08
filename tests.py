import unittest
from boards.board import Board, TargetBoard, PlayerBoard, PlanesError, GameOver
from Computer_player.Computer import Computer

class TestBoard(unittest.TestCase):
    def setUp(self):
        self._board = Board(10)

    def test_size(self):
        self.assertEqual(self._board.get_size, 10)


    def test_place_plane(self):
        self._board.place_plane(7, 8, "right", 3)
        self.assertEqual(self._board.is_empty(7,7), False)
        self.assertEqual(self._board.is_empty(7,8), False)
        self.assertRaises(PlanesError, self._board.place_plane, 7, 7, "down", 5)
        self.assertRaises(PlanesError, self._board.place_plane,10, 3, "left", 7)

    def test_is_empty(self):
        self.assertEqual(self._board.is_empty(2, 2), True)
        self._board.place_plane(2, 2, "up", 1)
        self.assertEqual(self._board.is_empty(2, 2), False)

    def test_hit(self):
        self._board.place_plane(7,8, "right", 3)
        result = self._board.hit(7,7)
        self.assertEqual(result,1)
        self.assertEqual(self._board.hit(0,1), 3)
        self.assertEqual(self._board.hit(7,8),2)
        self.assertRaises(PlanesError, self._board.hit,0,1 )

    def test_Game_over(self):
        self._board.place_plane(7,8, "right", 3)
        self._board.place_plane(2, 2, "up", 1)
        self._board.place_plane(1, 7, "up", 1)
        self._board.hit(7,8)
        self._board.hit(2,2)
        self.assertRaises(GameOver, self._board.hit, 1,7)

class TestComputer(unittest.TestCase):
    def setUp(self):
        self.__tb = TargetBoard(10)
        self.__pb = PlayerBoard(10)
        self.__ai = Computer(self.__tb, self.__pb)

    def test_place_plane(self):
        self.__ai.place_plane(1)
        occupied_spaces = 0
        for i in range (10):
            for j in range(10):
                if self.__tb.is_empty(i,j) == False:
                        occupied_spaces +=1
        self.assertEqual(occupied_spaces,10)

    def test_hit(self):
        targets = self.__ai.get_targets()
        self.__ai.hit()
        self.__ai.hit()
        self.assertEqual(len(targets), 98)


if __name__ == "__main__":
    unittest.main()



