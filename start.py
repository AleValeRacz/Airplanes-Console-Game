from boards.board import PlayerBoard, TargetBoard
from Computer_player.Computer import Computer
from Ui.ui import Ui

t_board = TargetBoard(10)
p_board = PlayerBoard(10)
ai = Computer(t_board, p_board)
ui = Ui(p_board, t_board, ai)
ui.start_game()
