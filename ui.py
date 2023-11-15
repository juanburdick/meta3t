'''Entry point for the game, contains:
    Launching methods
    Top-level game objects for maintaining the state
        GameController maintains the game state
        GameWidget runs the game and connects visual elements with the GameController'''
# pylint: disable=no-name-in-module, import-error, fixme
import sys
from typing import List, Dict, Tuple, Protocol
import numpy as np
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QMainWindow
from game_objects.boards import MetaBoard, SubGameBoard, MenuBox
from game_objects.buttons import GameButton, TURN, TURN_CYCLER

_GAME_SIZE = 700

class TurnIndicator(Protocol):
    def update_turn_indicator(self, _: bool) -> None:
        return

class GameController:
    '''class for mainting the game data'''
    def __init__(self) -> None:
        self.turn = next(TURN_CYCLER)
        self.turn_history: List[GameButton] = []
        self.turn_indicators: List[TurnIndicator] = []
        self.boards: Dict[Tuple[int,...], SubGameBoard] = {}
        self.buttons: np.ndarray[GameButton] = np.empty((3,3,3,3), dtype = GameButton) # type: ignore

    def register(self, to_reg, key: Tuple[int,...] | None = None):
        '''allows game pieces to register themself with the game controller'''
        if isinstance(to_reg, SubGameBoard):
            self.boards[to_reg.layout_position] = to_reg

        elif isinstance(to_reg, GameButton):
            if not key:
                raise KeyError('Key is required when GameButton is registering!')
            self.buttons[key][to_reg.layout_position] = to_reg

        elif hasattr(to_reg, 'update_turn_indicator') and callable(to_reg.update_turn_indicator):
            self.turn_indicators.append(to_reg)

    def update_turn_indicators(self):
        '''Call all registered turn indicators to update their displays'''
        for indicator in self.turn_indicators:
            indicator.update_turn_indicator(self.turn is TURN.PL_1)

    def update_boards(self, target: Tuple[int,...]):
        '''Try to activate a board (if it's already claimed, activate all unclaimed boards instead)'''
        target_board = self.boards[target]

        if target_board.is_claimed: # if target board is claimed, enable all other unclaimed boards
            for board in self.boards.values():
                if not board.is_claimed:
                    board.set_active_board()

        else: # if target board isn't claimed, enable target and disable all other unclaimed boards
            target_board.set_active_board()
            for board in self.boards.values():
                if not board.is_claimed and board is not target_board:
                    board.disable_board()

    def take_turn(self, button: GameButton) -> TURN:
        '''method that returns active player's turn, stores turn history, and updates turn player'''
        self.update_boards(target = button.layout_position)
        self.turn_history.append(button)

        player = self.turn
        self.turn = next(TURN_CYCLER)
        self.update_turn_indicators()
        return player

    def undo_last_move(self):
        '''undo the most recent move'''
        if len(self.turn_history) > 1:
            square_played = self.turn_history.pop() # remove the last play from the history to discard it
            square_played.resetButtonstate() # reset the button before discarding the play

            prev_square = self.turn_history[-1] # to reset the board, we need to act as if the prev turn was just taken
            self.update_boards(target = prev_square.layout_position)

            self.turn = next(TURN_CYCLER) # since the game is binary, we can simply progress the turn cycler
            self.update_turn_indicators() # and update the turn indicators appropriately

        else: # since undoing carries a backref to the prev turn, if the turn to be undone was the first one
            self.reset_new_game() # just reset

    def reset_new_game(self):
        '''reset the board for a new game'''
        for board in self.boards.values():
            for button in board.buttons:
                button.resetButtonstate()
            board.set_active_board()
        if self.turn is TURN.PL_2:
            self.turn = next(TURN_CYCLER)
            self.update_turn_indicators()
        self.turn_history.clear()

class GameWidget(QWidget):
    '''Used to implement a tabbed system of splitting widgets'''
    def __init__(self, parent: 'HostWindow'):
        super().__init__(parent)

        self.gc = GameController()

        self.meta = MetaBoard(size = _GAME_SIZE,
                              layout_position = (0,0,1,1),
                              get_turn_player = self.gc.take_turn,
                              registration = self.gc.register)

        self.menu = MenuBox(layout_position = (1,0,1,1),
                            registration = self.gc.register,
                            new_game_method = self.gc.reset_new_game,
                            undo_method = self.gc.undo_last_move,
                            exit_method = parent.close)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.meta.groupbox, *self.meta.layout_position)
        self.layout().addWidget(self.menu.groupbox, *self.menu.layout_position)

class HostWindow(QMainWindow):
    '''The main game window'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Meta Tic-Tac-Toe')
        self.setCentralWidget(GameWidget(parent = self))
        self.setStyleSheet('background-color: rgb(22,25,37)')
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    game = HostWindow()
    game.setFixedSize(718,804)
    sys.exit(app.exec_())
