'''Create the startup window.'''
# pylint: disable=no-name-in-module, import-error, fixme
import sys
from enum import Enum
from typing import List, Dict, Tuple, Optional, Callable, Protocol, Any
from itertools import product, cycle
import numpy as np
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QMainWindow, QPushButton
from tools.ui_widgets import MenuButton, GameButton, GameGroupBox, TURN, TURN_CYCLER
from tools.stylesheets import get_btn_style, get_box_style,SELECT

_GAME_SIZE = 700
_MENU_SIZE = 80
_BOX_SIZE = 220
_BTN_SIZE = 60
_CLAIMED_SIZE = 195

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

class MetaBoard(QWidget):
    '''Contain and track the main game/game board'''
    def __init__(self,
                 size: int,
                 layout_position: Tuple[int,...],
                 get_turn_player: Callable[[GameButton], TURN],
                 registration: Callable[[Any,Optional[Tuple[int,...]]], None],
                 ):
        super().__init__()
        self.groupbox = GameGroupBox(get_box_style(SELECT.PL_1), size, size)
        self.layout_position = layout_position

        for position in product((0,1,2), repeat = 2):
            subgame = SubGameBoard(_BOX_SIZE, position, get_turn_player, registration)
            self.groupbox.layout().addWidget(subgame.groupbox, *subgame.layout_position) # type: ignore

        registration(self, None)

    def update_turn_indicator(self, is_player_one: bool):
        '''update the color of the groupbox to indicate which player's turn it is'''
        self.groupbox.setStyleSheet(get_box_style(SELECT.PL_1 if is_player_one else SELECT.PL_2))

class SubGameBoard(QWidget):
    '''Contains a subgame of tic tac toe'''
    def __init__(self,
                 size: int,
                 layout_position : Tuple[int,...],
                 get_turn_player: Callable[[GameButton], TURN],
                 registration: Callable[[Any,Optional[Tuple[int,...]]], None],
                ):
        super().__init__()

        self.groupbox = GameGroupBox(get_box_style(SELECT.DEFAULT_BOX), size, size)
        self.layout_position = layout_position
        self.is_claimed: bool = False

        self.buttons: List[GameButton] = []
        self.claimed_button = GameButton('x', _CLAIMED_SIZE, (0,0), self.layout_position, get_turn_player, registration)

        for position in product((0,1,2), repeat = 2):
            button = GameButton('', _BTN_SIZE, position, self.layout_position, get_turn_player, registration)
            button.clicked.connect(button.claim)
            self.groupbox.layout().addWidget(button, *position) # type: ignore
            self.buttons.append(button)

        if self.layout_position == (0,0):
            self.claim_board()

        registration(self, None)

    def set_active_board(self):
        '''this is the board the current player will be forced to play in, set all buttons in it active'''
        self.groupbox.setStyleSheet(get_box_style(SELECT.DEFAULT_BOX))
        for button in self.buttons:
            if not button.is_claimed:
                button.resetButtonstate()

    def disable_board(self):
        '''this board is not available to the player this turn, disable all buttons in it'''
        self.groupbox.setStyleSheet(get_box_style(SELECT.DISABLED_BOX))
        for button in self.buttons:
            button.setDisabled(True)
            if not button.is_claimed:
                button.setStyleSheet(get_btn_style(SELECT.DISABLED_BTN))

    def claim_board(self):
        '''a player has won this board, display that player's symbol and lock the board'''
        self.is_claimed = True
        for button in self.buttons:
            button.setParent(None)

        self.groupbox.layout().addWidget(self.claimed_button, *self.claimed_button.layout_position)
        self.claimed_button.setStyleSheet(get_btn_style(SELECT.PL_1))
        # claimed_button.setDisabled(True)
        self.claimed_button.clicked.connect(self.reset_board)

    def reset_board(self):
        '''reset the board'''
        self.is_claimed = False
        self.claimed_button.setParent(None)
        for button in self.buttons:
            button.setParent(self)
            self.groupbox.layout().addWidget(button, *button.layout_position)

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

class MenuBox(QWidget):
    '''Parent class for GroupBoxes for jogging buttons'''
    def __init__(self,
                 layout_position: Tuple[int,...],
                 registration: Callable[[TurnIndicator], None],
                 new_game_method: Callable,
                 undo_method: Callable,
                 exit_method: Callable,
                 ):
        super().__init__()
        self.layout_position = layout_position
        self.groupbox = GameGroupBox(get_box_style(SELECT.PL_1), width = _GAME_SIZE, height = _MENU_SIZE)

        reset_button = MenuButton("New Game", (0,0,1,1))
        reset_button.clicked.connect(new_game_method)
        self.groupbox.layout().addWidget(reset_button, *reset_button.layout_position)

        undo_button = MenuButton("Undo", (0,1,1,1))
        undo_button.clicked.connect(undo_method)
        self.groupbox.layout().addWidget(undo_button, *undo_button.layout_position)

        exit_button = MenuButton("Exit Game", (0,2,1,1))
        exit_button.clicked.connect(exit_method)
        self.groupbox.layout().addWidget(exit_button, *exit_button.layout_position)

        registration(self)

    def update_turn_indicator(self, is_player_one: bool):
        '''update the color of the groupbox to indicate which player's turn it is'''
        self.groupbox.setStyleSheet(get_box_style(SELECT.PL_1 if is_player_one else SELECT.PL_2))

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
