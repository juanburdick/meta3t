'''Create the startup window.'''
# pylint: disable=no-name-in-module, import-error, fixme
import sys
from typing import List, Dict, Tuple
from itertools import product
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QMainWindow, QPushButton
from tools.ui_widgets import GameGroupBox, MenuButton
from tools.stylesheets import GROUPBOX_STYLE,DISABLED_GROUPBOX_STYLE,P1_BTN_STYLE,P2_BTN_STYLE,P1_TURN_INDICATOR,P2_TURN_INDICATOR

class GameButton(QPushButton):
    """A standardized button for the game"""
    def __init__(self, parent: 'SubGameBoard', text: str, size: int, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(text = text)
        self.ancestor = parent
        self.setFixedSize(size, size)
        self.layout_position = layout_position

    def getButtonPosition(self):
        return self.layout_position

    def setButtonState(self):
        '''a user has selected this square, gaining control of it'''
        is_player_one_turn = self.ancestor.ancestor.ancestor.who_is_taking_turn(self)

        if is_player_one_turn:
            self.setStyleSheet(P1_BTN_STYLE)
            self.setText('x')
        else:
            self.setStyleSheet(P2_BTN_STYLE)
            self.setText('o')
        self.setDisabled(True)

    def resetButtonstate(self):
        '''undo button was clicked, reset this square'''
        self.setStyleSheet('')
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
        self.groupbox = GameGroupBox(P1_TURN_INDICATOR, size, size)
        self.layout_position = layout_position

        for position in self.GRID:
            subgame = SubGameBoard(self, 220, position)
            self.groupbox.layout().addWidget(subgame.groupbox, *subgame.layout_position) # type: ignore

    def update_turn_indicator(self, is_player_one: bool):
        '''update the color of the groupbox to indicate which player's turn it is'''
        self.groupbox.setStyleSheet(P1_TURN_INDICATOR if is_player_one else P2_TURN_INDICATOR)


class SubGameBoard(QWidget):
    '''Contains a subgame of tic tac toe'''
    def __init__(self, parent: MetaBoard, size: int, layout_position : Tuple[int,...] = (0,0)):
        super().__init__(parent)
        self.ancestor = parent
        self.groupbox = GameGroupBox(GROUPBOX_STYLE, size, size)
        self.layout_position = layout_position
        self.buttons: List[GameButton] = []

        for position in product((0,1,2), repeat = 2):
            button = GameButton(self, '', 60, position)
            button.clicked.connect(button.setButtonState)
            self.groupbox.layout().addWidget(button, *position) # type: ignore
            self.buttons.append(button)

        self.disable_board()

    def set_active_board(self):
        '''this is the board the current player will be forced to play in, set all buttons in it active'''

    def disable_board(self):
        '''this board is not available to the player this turn, disable all buttons in it'''
        if self.layout_position == (2,2):
            self.groupbox.setStyleSheet(DISABLED_GROUPBOX_STYLE)
            for button in self.buttons:
                button.setDisabled(True)
                button.setStyleSheet('background-color: rgba(130,130,130,100)')

class GameController(QWidget):
    '''Used to implement a tabbed system of splitting widgets'''
    def __init__(self, parent: 'HostWindow'):
        super().__init__(parent)
        self.ancestor = parent
        self.setLayout(QGridLayout())

        meta = MetaBoard(self, 700, (0,0,1,1))
        self.meta = meta
        menu = MenuBox(self, (1,0,1,1))
        self.menu = menu

        self.layout().addWidget(meta.groupbox, *meta.layout_position)
        self.layout().addWidget(menu.groupbox, *menu.layout_position)

        self.is_player_one_turn: bool = True
        self.turn_history: List[GameButton] = []

    def switch_turn(self):
        self.is_player_one_turn = False if self.is_player_one_turn else True
        self.menu.update_turn_indicator(self.is_player_one_turn)
        self.meta.update_turn_indicator(self.is_player_one_turn)

    def who_is_taking_turn(self, button: GameButton) -> bool:
        '''method that returns active player's turn, stores turn history, and updates turn player'''
        ret = self.is_player_one_turn
        self.switch_turn()
        self.turn_history.append(button)
        return ret

    def undo_last_move(self):
        '''undo the most recent move'''
        if self.turn_history:
            self.turn_history.pop().resetButtonstate()
            self.switch_turn()

    def reset_new_game(self):
        '''reset the board for a new game'''
        while self.turn_history:
            self.undo_last_move()

class MenuBox(QWidget):
    '''Parent class for GroupBoxes for jogging buttons'''
    def __init__(self, parent: 'GameController', layout_position: Tuple[int,...] = (0,0)):
        super().__init__(parent)
        self.ancestor = parent
        self.layout_position = layout_position
        self.groupbox = GameGroupBox(P1_TURN_INDICATOR, width = 700, height = 80)

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
        self.groupbox.setStyleSheet(P1_TURN_INDICATOR if is_player_one else P2_TURN_INDICATOR)

class HostWindow(QMainWindow):
    '''The main game window'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Meta Tic-Tac-Toe')
        self.setCentralWidget(GameController(parent = self))
        self.setStyleSheet('background-color: rgb(136, 136, 136)')
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    game = HostWindow()
    game.resize(700, 720)
    sys.exit(app.exec_())
