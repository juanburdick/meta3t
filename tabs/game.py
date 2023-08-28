'''Groupboxes containing the manual jog buttons'''
# pylint: disable=no-name-in-module, import-error
from typing import Tuple, Union, TYPE_CHECKING
from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QPushButton
from tools.stylesheets import GROUPBOX_STYLE
if TYPE_CHECKING:
    from ui import Tabs

class GameGroupBox(QGroupBox):
    """A standard groub box widget for the WAAM GUI"""
    def __init__(self, style:str, size: int):
        super().__init__()
        self.setLayout(QGridLayout())
        self.setStyleSheet(style)
        self.setFixedSize(size, size)

class GameButton(QPushButton):
    """A standardized button for the game"""
    def __init__(self, text: str, size: int, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(text = text)
        self.setFixedSize(size, size)
        self.layout_position = layout_position

class GameTab(QWidget):
    '''Contains instances of user_ctrl_widgets submodules'''
    def __init__(self, parent: 'Tabs'):
        super().__init__(parent)
        self.setLayout(QGridLayout())

        meta = MetaBoard(self, 700, (0,0,1,1))
        self.layout().addWidget(meta.groupbox, *meta.layout_position) # type: ignore

class Board(QWidget):
    GRID = [(0,0,1,1), (0,1,1,1), (0,2,1,1),
            (1,0,1,1), (1,1,1,1), (1,2,1,1),
            (2,0,1,1), (2,1,1,1), (2,2,1,1)]

    '''Format for a tic tac toe game, meta or subgame'''
    def __init__(self, parent: Union[GameTab, 'MetaBoard'], size: int, layout_position : Tuple[int,...] = (0,0)):
        super().__init__(parent)
        self.groupbox = GameGroupBox(GROUPBOX_STYLE, size)
        self.layout_position = layout_position

class MetaBoard(Board):
    '''Contain and track the main game/game board'''
    def __init__(self, parent: GameTab, size: int, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(parent, size, layout_position)

        for position in self.GRID:
            subgame = SubGameBoard(self, 220, position)
            self.groupbox.layout().addWidget(subgame.groupbox, *subgame.layout_position) # type: ignore

class SubGameBoard(Board):
    '''Contains a subgame of tic tac toe'''
    def __init__(self, parent: MetaBoard, size: int, layout_position : Tuple[int,...] = (0,0)):
        super().__init__(parent, size, layout_position)

        for position in self.GRID:
            button = GameButton(f'{position[:2]}', 60, position)
            self.groupbox.layout().addWidget(button, *button.layout_position) # type: ignore
