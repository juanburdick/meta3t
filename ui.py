'''Create the startup window.'''
# pylint: disable=no-name-in-module, import-error, fixme
import sys
from enum import Enum
from typing import List, Dict, Tuple, Optional
from itertools import product, cycle
import numpy as np
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QMainWindow, QPushButton
from tools.ui_widgets import GameGroupBox, MenuButton
from tools.stylesheets import get_btn_style, get_box_style,SELECT

_GAME_SIZE = 700
_MENU_SIZE = 80
_BOX_SIZE = 220
_BTN_SIZE = 60
_CLAIMED_SIZE = 195

class TURN(Enum):
    '''Enum for tracking turn player'''
    PL_1 = 1
    PL_2 = 2

TURN_CYCLER = cycle((TURN.PL_1, TURN.PL_2))

class GameController:
    '''class for mainting the game data'''
    def __init__(self, parent: 'GameWidget') -> None:
        self.parent = parent
        self.turn = next(TURN_CYCLER)
        self.turn_history: List[GameButton] = []
        self.boards: Dict[Tuple[int,int], SubGameBoard] = {}
        self.buttons: np.ndarray[GameButton] = np.empty((3,3,3,3), dtype = GameButton)

    def register(self, board: 'SubGameBoard', button: Optional['GameButton'] = None):
        '''allows game pieces to register themself with the game controller'''
        if button is None:
            self.boards[board.layout_position] = board
            return None

        self.buttons[board.layout_position][button.layout_position] = button
        return None

    def update_boards(self, target: Tuple[int,int]):
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

    def take_turn(self, button: 'GameButton') -> TURN:
        '''method that returns active player's turn, stores turn history, and updates turn player'''
        self.update_boards(target = button.layout_position)
        self.turn_history.append(button)

        player = self.turn
        self.turn = next(TURN_CYCLER)
        self.parent.update_turn_indicators()
        return player

    def undo_last_move(self):
        '''undo the most recent move'''
        if len(self.turn_history) > 1:
            square_played = self.turn_history.pop() # remove the last play from the history to discard it
            square_played.resetButtonstate() # reset the button before discarding the play

            prev_square = self.turn_history[-1] # to reset the board, we need to act as if the prev turn was just taken
            self.update_boards(target = prev_square.layout_position)

            self.turn = next(TURN_CYCLER) # since the game is binary, we can simply progress the turn cycler
            self.parent.update_turn_indicators() # and update the turn indicators appropriately

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
            self.parent.update_turn_indicators()
        self.turn_history.clear()

class GameButton(QPushButton):
    """A standardized button for the game"""
    def __init__(self, parent: 'SubGameBoard', game_controller: GameController, text: str, size: int, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(text = text)
        self.ancestor = parent
        self.gc = game_controller
        self.setFixedSize(size, size)
        self.setStyleSheet(get_btn_style(SELECT.DEFAULT_BTN))
        self.layout_position = layout_position
        self.is_claimed: bool = False

        self.gc.register(self.ancestor, self)

    def getButtonPosition(self):
        return self.layout_position

    def claim(self):
        '''a user has selected this square, gaining control of it'''
        self.is_claimed = True
        turn = self.gc.take_turn(self)
        ref = SELECT.PL_1 if turn is TURN.PL_1 else SELECT.PL_2
        self.setStyleSheet(get_btn_style(ref))
        self.setDisabled(True)

    def resetButtonstate(self):
        '''undo button was clicked, reset this square'''
        self.is_claimed = False
        self.setStyleSheet(get_btn_style(SELECT.DEFAULT_BTN))
        self.setEnabled(True)

class MetaBoard(QWidget):
    '''Contain and track the main game/game board'''
    GRID = [(0,0), (0,1), (0,2),
            (1,0), (1,1), (1,2),
            (2,0), (2,1), (2,2)]

    def __init__(self, parent: 'GameWidget', game_controller: GameController, size: int, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(parent)
        self.ancestor = parent
        self.gc = game_controller
        self.groupbox = GameGroupBox(get_box_style(SELECT.PL_1), size, size)
        self.layout_position = layout_position

        for position in self.GRID:
            subgame = SubGameBoard(self, self.gc, _BOX_SIZE, position)
            self.groupbox.layout().addWidget(subgame.groupbox, *subgame.layout_position) # type: ignore

    def update_turn_indicator(self, is_player_one: bool):
        '''update the color of the groupbox to indicate which player's turn it is'''
        self.groupbox.setStyleSheet(get_box_style(SELECT.PL_1 if is_player_one else SELECT.PL_2))

class SubGameBoard(QWidget):
    '''Contains a subgame of tic tac toe'''
    def __init__(self, parent: MetaBoard, game_controller: GameController, size: int, layout_position : Tuple[int,...] = (0,0)):
        super().__init__(parent)
        self.ancestor = parent
        self.gc = game_controller
        self.groupbox = GameGroupBox(get_box_style(SELECT.DEFAULT_BOX), size, size)
        self.layout_position = layout_position
        self.is_claimed: bool = False

        self.buttons: List[GameButton] = []
        self.claimed_button = GameButton(self, self.gc, 'x', _CLAIMED_SIZE, (0,0))

        for position in product((0,1,2), repeat = 2):
            button = GameButton(self, self.gc, '', _BTN_SIZE, position)
            button.clicked.connect(button.claim)
            self.groupbox.layout().addWidget(button, *position) # type: ignore
            self.buttons.append(button)

        if self.layout_position == (0,0):
            self.claim_board()

        self.gc.register(self)

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
        self.ancestor = parent
        self.setLayout(QGridLayout())

        self.gc = GameController(self)

        self.meta = MetaBoard(self, self.gc, _GAME_SIZE, (0,0,1,1))
        self.menu = MenuBox(self, self.gc, (1,0,1,1))

        self.layout().addWidget(self.meta.groupbox, *self.meta.layout_position)
        self.layout().addWidget(self.menu.groupbox, *self.menu.layout_position)

    def update_turn_indicators(self):
        '''update menu and board turn indicators'''
        self.menu.update_turn_indicator(self.gc.turn is TURN.PL_1)
        self.meta.update_turn_indicator(self.gc.turn is TURN.PL_1)

class MenuBox(QWidget):
    '''Parent class for GroupBoxes for jogging buttons'''
    def __init__(self, parent: 'GameWidget', game_controller: GameController, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(parent)
        self.ancestor = parent
        self.gc = game_controller
        self.layout_position = layout_position
        self.groupbox = GameGroupBox(get_box_style(SELECT.PL_1), width = _GAME_SIZE, height = _MENU_SIZE)

        reset_button = MenuButton("New Game", (0,0,1,1))
        reset_button.clicked.connect(self.gc.reset_new_game)
        self.groupbox.layout().addWidget(reset_button, *reset_button.layout_position)

        undo_button = MenuButton("Undo", (0,1,1,1))
        undo_button.clicked.connect(self.gc.undo_last_move)
        self.groupbox.layout().addWidget(undo_button, *undo_button.layout_position)

        exit_button = MenuButton("Exit Game", (0,2,1,1))
        exit_button.clicked.connect(self.ancestor.ancestor.close)
        self.groupbox.layout().addWidget(exit_button, *exit_button.layout_position)

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
