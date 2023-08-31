'''Create the startup window.'''
# pylint: disable=no-name-in-module, import-error, fixme
import sys
from typing import Tuple
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QMainWindow, QPushButton
from tools.ui_widgets import GameGroupBox, MenuButton
from tools.stylesheets import MAIN_WINDOW_STYLE, GROUPBOX_STYLE, PLAYER_1_STYLE, PLAYER_2_STYLE

class GameButton(QPushButton):
    """A standardized button for the game"""
    def __init__(self, parent: 'SubGameBoard', text: str, size: int, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(text = text)
        self.ancestor = parent
        self.setFixedSize(size, size)
        self.layout_position = layout_position

    def setButtonState(self, is_player_one_turn: bool):
        '''a user has selected this square, gaining control of it'''
        if is_player_one_turn:
            self.setStyleSheet(PLAYER_1_STYLE)
            self.setText('x')
        else:
            self.setStyleSheet(PLAYER_2_STYLE)
            self.setText('o')
        self.setDisabled(True)

class MetaBoard(QWidget):
    '''Contain and track the main game/game board'''
    GRID = [(0,0), (0,1), (0,2),
            (1,0), (1,1), (1,2),
            (2,0), (2,1), (2,2)]

    def __init__(self, parent: 'GameController', size: int, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(parent)
        self.ancestor = parent
        self.groupbox = GameGroupBox(GROUPBOX_STYLE, size, size)
        self.layout_position = layout_position

        for position in self.GRID:
            subgame = SubGameBoard(self, 220, position)
            self.groupbox.layout().addWidget(subgame.groupbox, *subgame.layout_position) # type: ignore

class SubGameBoard(QWidget):
    '''Contains a subgame of tic tac toe'''
    GRID = [(0,0), (0,1), (0,2),
            (1,0), (1,1), (1,2),
            (2,0), (2,1), (2,2)]

    def __init__(self, parent: MetaBoard, size: int, layout_position : Tuple[int,...] = (0,0)):
        super().__init__(parent)
        self.ancestor = parent
        self.groupbox = GameGroupBox(GROUPBOX_STYLE, size, size)
        self.layout_position = layout_position

        for position in self.GRID:
            button = GameButton(self, f'{position}', 60, position)
            button.clicked.connect(lambda: self.take_turn(button))
            self.groupbox.layout().addWidget(button, *button.layout_position) # type: ignore

    def take_turn(self, button: GameButton):
        '''set button state based on turn player and switch turn'''
        button.setButtonState(self.ancestor.ancestor.is_player_one_turn)
        self.ancestor.ancestor.switch_turn()

class GameController(QWidget):
    '''Used to implement a tabbed system of splitting widgets'''
    def __init__(self, parent: 'HostWindow'):
        super().__init__(parent)
        self.ancestor = parent
        self.is_player_one_turn = True
        self.setLayout(QGridLayout())

        meta = MetaBoard(self, 700, (0,0,1,1))
        menu = MenuBox(self, (1,0,1,1))

        self.layout().addWidget(meta.groupbox, *meta.layout_position)
        self.layout().addWidget(menu.groupbox, *menu.layout_position)

    def switch_turn(self):
        self.is_player_one_turn = False if self.is_player_one_turn else True

class MenuBox(QWidget):
    '''Parent class for GroupBoxes for jogging buttons'''
    def __init__(self, parent: 'GameController', layout_position: Tuple[int,...] = (0,0)):
        super().__init__(parent)
        self.ancestor = parent
        self.layout_position = layout_position
        self.groupbox = GameGroupBox(GROUPBOX_STYLE, width = 700, height = 80)

        start_button = MenuButton("New Game", (0,0,1,1))
        undo_button = MenuButton("Undo", (0,1,1,1))
        exit_button = MenuButton("Exit Game", (0,2,1,1))
        exit_button.clicked.connect(self.ancestor.ancestor.close)

        self.groupbox.layout().addWidget(start_button, *start_button.layout_position)
        self.groupbox.layout().addWidget(undo_button, *undo_button.layout_position)
        self.groupbox.layout().addWidget(exit_button, *exit_button.layout_position)

class HostWindow(QMainWindow):
    '''The main game window'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Meta Tic-Tac-Toe')
        self.setCentralWidget(GameController(parent = self))
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    game = HostWindow()
    game.resize(700, 720)
    sys.exit(app.exec_())
