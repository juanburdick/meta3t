'''Create the startup window.'''
# pylint: disable=no-name-in-module, import-error, fixme
import sys
from typing import List, Dict, Tuple, Optional
from itertools import product
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QMainWindow, QPushButton
from tools.ui_widgets import GameGroupBox, MenuButton
from tools.stylesheets import get_style,BTN_STYLE,BOX_STYLE

class GameButton(QPushButton):
    """A standardized button for the game"""
    def __init__(self, parent: 'SubGameBoard', text: str, size: int, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(text = text)
        self.ancestor = parent
        self.setFixedSize(size, size)
        self.layout_position = layout_position
        self.setStyleSheet(get_style(BTN_STYLE.DEFAULT))
        self.is_claimed: bool = False

    def getButtonPosition(self):
        return self.layout_position

    def claim(self):
        '''a user has selected this square, gaining control of it'''
        self.is_claimed = True
        is_player_one_turn = self.ancestor.ancestor.ancestor.who_is_taking_turn(self)

        if is_player_one_turn:
            self.setStyleSheet(get_style(BTN_STYLE.PL_1))
            self.setText('x')
        else:
            self.setStyleSheet(get_style(BTN_STYLE.PL_2))
            self.setText('o')
        self.setDisabled(True)

    def resetButtonstate(self):
        '''undo button was clicked, reset this square'''
        self.is_claimed = False
        self.setStyleSheet(get_style(BTN_STYLE.DEFAULT))
        self.setText('')
        self.setEnabled(True)

class MetaBoard(QWidget):
    '''Contain and track the main game/game board'''
    GRID = [(0,0), (0,1), (0,2),
            (1,0), (1,1), (1,2),
            (2,0), (2,1), (2,2)]

    def __init__(self, parent: 'GameController', size: int, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(parent)
        self.ancestor = parent
        self.groupbox = GameGroupBox(get_style(BOX_STYLE.PL_1), size, size)
        self.layout_position = layout_position

        for position in self.GRID:
            subgame = SubGameBoard(self, 220, position)
            self.groupbox.layout().addWidget(subgame.groupbox, *subgame.layout_position) # type: ignore

    def update_turn_indicator(self, is_player_one: bool):
        '''update the color of the groupbox to indicate which player's turn it is'''
        self.groupbox.setStyleSheet(get_style(BOX_STYLE.PL_1 if is_player_one else BOX_STYLE.PL_2))

class SubGameBoard(QWidget):
    '''Contains a subgame of tic tac toe'''
    def __init__(self, parent: MetaBoard, size: int, layout_position : Tuple[int,...] = (0,0)):
        super().__init__(parent)
        self.ancestor = parent
        self.groupbox = GameGroupBox(get_style(BOX_STYLE.DEFAULT), size, size)
        self.layout_position = layout_position
        self.ancestor.ancestor.boards[layout_position] = self

        self.buttons: List[GameButton] = []

        for position in product((0,1,2), repeat = 2):
            button = GameButton(self, '', 60, position)
            button.clicked.connect(button.claim)
            self.groupbox.layout().addWidget(button, *position) # type: ignore
            self.buttons.append(button)

    def set_active_board(self):
        '''this is the board the current player will be forced to play in, set all buttons in it active'''
        self.groupbox.setStyleSheet(get_style(BOX_STYLE.DEFAULT))
        for button in self.buttons:
            if not button.is_claimed:
                button.resetButtonstate()

    def disable_board(self):
        '''this board is not available to the player this turn, disable all buttons in it'''
        self.groupbox.setStyleSheet(get_style(BOX_STYLE.DISABLED))
        for button in self.buttons:
            button.setDisabled(True)
            if not button.is_claimed:
                button.setStyleSheet(get_style(BTN_STYLE.DISABLED))

class GameController(QWidget):
    '''Used to implement a tabbed system of splitting widgets'''
    def __init__(self, parent: 'HostWindow'):
        super().__init__(parent)
        self.ancestor = parent
        self.setLayout(QGridLayout())

        self.is_player_one_turn: bool = True
        self.turn_history: List[GameButton] = []
        self.boards: Dict[Tuple[int,int], SubGameBoard] = {}

        self.meta = MetaBoard(self, 700, (0,0,1,1))
        self.menu = MenuBox(self, (1,0,1,1))

        self.layout().addWidget(self.meta.groupbox, *self.meta.layout_position)
        self.layout().addWidget(self.menu.groupbox, *self.menu.layout_position)

    def update_boards(self, target: Tuple[int,int]):
        '''Set boards active or inactive based on the last move'''
        for layout_position, board in self.boards.items():
            if layout_position == target:
                board.set_active_board()
            else:
                board.disable_board()

    def switch_turn(self, source_button: Optional[GameButton] = None):
        if source_button is not None:
            self.update_boards(source_button.layout_position)
        self.is_player_one_turn = False if self.is_player_one_turn else True
        self.menu.update_turn_indicator(self.is_player_one_turn)
        self.meta.update_turn_indicator(self.is_player_one_turn)

    def who_is_taking_turn(self, button: GameButton) -> bool:
        '''method that returns active player's turn, stores turn history, and updates turn player'''
        ret = self.is_player_one_turn
        self.switch_turn(button)
        self.turn_history.append(button)
        return ret

    def undo_last_move(self):
        '''undo the most recent move'''
        if len(self.turn_history) > 1:
            self.turn_history.pop().resetButtonstate()
            self.switch_turn(self.turn_history[-1])
        else:
            self.reset_new_game()

    def reset_new_game(self):
        '''reset the board for a new game'''
        for board in self.boards.values():
            for button in board.buttons:
                button.resetButtonstate()
            board.set_active_board()
        if not self.is_player_one_turn:
            self.switch_turn()

class MenuBox(QWidget):
    '''Parent class for GroupBoxes for jogging buttons'''
    def __init__(self, parent: 'GameController', layout_position: Tuple[int,...] = (0,0)):
        super().__init__(parent)
        self.ancestor = parent
        self.layout_position = layout_position
        self.groupbox = GameGroupBox(get_style(BOX_STYLE.PL_1), width = 700, height = 80)

        reset_button = MenuButton("New Game", (0,0,1,1))
        reset_button.clicked.connect(self.ancestor.reset_new_game)
        self.groupbox.layout().addWidget(reset_button, *reset_button.layout_position)

        undo_button = MenuButton("Undo", (0,1,1,1))
        undo_button.clicked.connect(self.ancestor.undo_last_move)
        self.groupbox.layout().addWidget(undo_button, *undo_button.layout_position)

        exit_button = MenuButton("Exit Game", (0,2,1,1))
        exit_button.clicked.connect(self.ancestor.ancestor.close)
        self.groupbox.layout().addWidget(exit_button, *exit_button.layout_position)

    def update_turn_indicator(self, is_player_one: bool):
        '''update the color of the groupbox to indicate which player's turn it is'''
        self.groupbox.setStyleSheet(get_style(BOX_STYLE.PL_1 if is_player_one else BOX_STYLE.PL_2))

class HostWindow(QMainWindow):
    '''The main game window'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Meta Tic-Tac-Toe')
        self.setCentralWidget(GameController(parent = self))
        self.setStyleSheet('background-color: rgb(22,25,37)')
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    game = HostWindow()
    game.setFixedSize(718,804)
    sys.exit(app.exec_())
