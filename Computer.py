import random
from boards.board import PlayerBoard, TargetBoard, PlanesError


class Computer:
    def __init__(self, target_board, player_board):
        self.__target_board = target_board
        self._player_board = player_board
        self.__targets = list(range(self._player_board.get_size ** 2))
        self.__shoot_randomly = True
        self.__last_hit = None
        self.__adjacent_targets = []

    def place_plane(self, i):
        """
        Places a plane randomly on the board, if the position is valid
        :param i: number used to represent the plane's head
        :return: -
        """
        while True:
            try:
                row = random.randint(0, self.__target_board.get_size - 1)
                column = random.randint(0, self.__target_board.get_size - 1)
                alignment = random.choice(["up", "down", "left", "right"])
                self.__target_board.place_plane(row, column, alignment, i)
                break
            except PlanesError:
                pass
    def get_targets(self):
        return self.__targets

    def hit(self):
        """
        Makes a shot, either randomly or based on the adjacent position of a previous hit if available; updates the available target lists, based on the result of the hit
        :return: -
        """
        if self.__shoot_randomly or not self.__adjacent_targets:
            target = random.choice(self.__targets)
        else:
                adjacent_targets = [ t for t in self.__adjacent_targets if t in self.__targets]
                if not adjacent_targets:
                    target = random.choice(self.__targets)
                else:
                    target = random.choice(adjacent_targets)
                    self.__adjacent_targets.remove(target)
        self.__targets.remove(target)
        result = self._player_board.hit(target // self._player_board.get_size, target % self._player_board.get_size)
        if result == 1:
            self.__shoot_randomly = False
            self.__last_hit = target
            self.__adjacent_targets = self.update_adjacent_targets()
        elif result == 2:
            new_targets = []
            for t in self.__targets:
                if self._player_board.get_board()[t] != 'X':
                    new_targets.append(t)
            self.__targets = new_targets
        elif result == 3 and not self.__adjacent_targets:
            self.__shoot_randomly = True

    def update_adjacent_targets(self):
        """
        Updates the list of adjacent position of previous hits, by adding new positions or removing them if they're not in the main targets lists anymore
        :return: updated list
        """
        new_adjacent_positions = [self.__last_hit+1, self.__last_hit -1, self.__last_hit - self._player_board.get_size,self.__last_hit + self._player_board.get_size]
        for pos in new_adjacent_positions:
            if pos in self.__targets and pos not in self.__adjacent_targets:
                self.__adjacent_targets.append(pos)
        return self.__adjacent_targets




