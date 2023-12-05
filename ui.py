'''Entry point for the game, containing launching method and top-level game objects for maintaining the state'''
# pylint: disable=no-name-in-module, import-error, fixme
import sys
from itertools import cycle, product
from typing import List, Dict, Tuple, Protocol
import numpy as np
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QMainWindow
from game_objects.boards import MetaBoard, SubGameBoard, MenuBox
from game_objects.buttons import GameButton, TURN

TURN_CYCLER = cycle((TURN.PL_1, TURN.PL_2))

class TurnIndicator(Protocol):
    def update_turn_indicator(self, _: TURN) -> None:
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
        if isinstance(to_reg, SubGameBoard): self.boards[to_reg.layout_position] = to_reg
        elif isinstance(to_reg, GameButton) and key is not None: self.buttons[key][to_reg.layout_position] = to_reg
        elif hasattr(to_reg, 'update_turn_indicator') and callable(to_reg.update_turn_indicator): self.turn_indicators.append(to_reg)

    def check_win(self):
        '''check to see if a player has won this subgame board, claiming it'''
        pl1_eval = np.vectorize(lambda button: button.owned_by_player is TURN.PL_1)(self.buttons)
        pl2_eval = np.vectorize(lambda button: button.owned_by_player is TURN.PL_2)(self.buttons)
        for target in product((0,1,2), repeat = 2):

            pl1_buttons = pl1_eval[target]
            pl1_diag1 = np.expand_dims(pl1_buttons.diagonal(),1)
            pl1_diag2 = np.expand_dims(np.fliplr(pl1_buttons).diagonal(),1)
            pl1_stacked = np.hstack((pl1_buttons, pl1_buttons.T, pl1_diag1, pl1_diag2))

            pl2_buttons = pl2_eval[target]
            pl2_diag1 = np.expand_dims(pl2_buttons.diagonal(),1)
            pl2_diag2 = np.expand_dims(np.fliplr(pl2_buttons).diagonal(),1)
            pl2_stacked = np.hstack((pl2_buttons, pl2_buttons.T, pl2_diag1, pl2_diag2))

            target_board = self.boards[target]

            if np.any(np.all(pl1_stacked, axis = 0)):
                if target_board.is_claimed:
                    continue
                target_board.claim_board(TURN.PL_1)

            if np.any(np.all(pl2_stacked, axis = 0)):
                if target_board.is_claimed:
                    continue
                target_board.claim_board(TURN.PL_2)

            if not np.any(np.all(pl1_stacked, axis = 0)) and not np.any(np.all(pl2_stacked, axis = 0)):
                target_board.reset_board()

    def show_next_turn(self):
        '''Call all registered turn indicators to update their displays'''
        self.turn = next(TURN_CYCLER)
        for indicator in self.turn_indicators:
            indicator.update_turn_indicator(self.turn)

    def update_boards(self, target: Tuple[int,...]):
        '''Try to activate a board (if it's already claimed, activate all unclaimed boards instead)'''
        self.check_win()
        target_board = self.boards[target]

        for _, board in self.boards.items():
            board.disable_board() # disable all boards
            if target_board.is_claimed and not board.is_claimed: # if target board is claimed, we'll enable all other NOT claimed boards
                board.set_active_board()

        if not target_board.is_claimed: # if target board isn't claimed, we just disabled every board including target
            target_board.set_active_board() # so enable just the target board

    def take_turn(self, button: GameButton) -> None:
        '''method that returns active player's turn, stores turn history, and updates turn player'''
        button.claim_button(self.turn)
        self.turn_history.append(button)
        self.update_boards(target = button.layout_position)
        self.show_next_turn()

    def undo_last_move(self):
        '''undo the most recent move'''
        if len(self.turn_history) < 2: self.reset_new_game(); return # if there's only one turn, just reset

        self.turn_history.pop().resetButtonstate() # remove the last play and reset the button before discarding
        previous = self.turn_history[-1] # to reset the board, we need to act as if the prev turn was just taken
        self.update_boards(target = previous.layout_position)
        self.show_next_turn()

    def reset_new_game(self):
        '''reset the board for a new game'''
        self.turn_history.clear()
        if self.turn is TURN.PL_2: self.show_next_turn()
        for board in self.boards.values():
            board.reset_board(new_game = True)
            board.set_active_board()

class GameWidget(QWidget):
    '''Class for maintaining and visualizing the game state'''
    def __init__(self, parent: 'HostWindow'):
        super().__init__(parent)

        self.gc = GameController()
        self.meta = MetaBoard((0,0,1,1), self.gc.take_turn, self.gc.register)
        self.menu = MenuBox((1,0,1,1), parent.close, self.gc.undo_last_move, self.gc.reset_new_game, self.gc.register)

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
