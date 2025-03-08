
from boards.board import GameOver, PlanesError
class Ui:
    def __init__(self, player_board, target_board, computer):
        self.__player_board = player_board
        self.__target_board = target_board
        self.__computer = computer

    def placing_phase(self, i):
        print(self.__player_board)
        while True:
            print("Where do you want to place the head of the plane?")
            column = input("Enter column(A to J): ").upper()
            if len(column) == 1 and 'A' <= column <='J':
                column = ord(column) - ord('A')
                break
            else:
                print("Invalid column!")
        while True:
            row = input("Enter row (1,10): ")
            if (row.isdigit() or row=='10') and 0 < int(row) < 11:
                row = int(row) - 1
                break
            else:
                print("Invalid row!")
        print("Do you want the plane to be facing up (w), down (s), left (a) or right (d)?")
        while True:
            alignment = input("enter w, a, s, or d: ").lower()
            corespondents = {'w': "up", 's': "down", 'd': "right", 'a': "left"}
            if alignment not in corespondents.keys():
                    print("Invalid alignment!")
            else:
                alignment = corespondents[alignment]
                break
        self.__player_board.place_plane(row,column, alignment,i)

    def start_game(self):
        i = 1
        while i <= 5:
            try:
                self.placing_phase(i)
                self.__computer.place_plane(i)
                print("Computer placed its plane!")
                i += 2
            except PlanesError as e:
                print(e)

        print("Starting the game!")
        while True:
            print("Player's board")
            print(self.__player_board)
            print("Computer's board")
            print(self.__target_board)
            try:
                print("Where do you want to shoot?")
                while True:
                    column = input("column: ").upper()
                    row = input("row: ")
                    if len(column) == 1 and 'A' <= column <='J' and (row.isdigit() or row=='10') and 0 < int(row) < 11:
                        column = ord(column) - ord('A')
                        row = int(row) - 1
                        break
                    else:
                        print("Invalid input!")
                self.__target_board.hit(row, column)
            except GameOver:
                print("You win!!!!")
                break
            except ValueError:
                print("Invalid input!")
            except PlanesError as e:
                print(e)
                continue
            try:
               self.__computer.hit()
            except GameOver:
                print("You lost!")
                break







