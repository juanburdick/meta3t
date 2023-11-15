'''Used for easily initializing widgets, meant to reduce the repeated calls which specify the respective fields of similar widgets'''
# pylint: disable=C0321, no-name-in-module, too-many-arguments
from enum import Enum
from typing import Tuple, Callable, Any, Optional
from PyQt5.QtWidgets import QPushButton, QLabel, QGroupBox, QGridLayout
from game_objects.stylesheets import SELECT, get_btn_style, BTN_STYLE_REF

class TURN(Enum):
    '''Enum for tracking turn player'''
    PL_1 = SELECT.PL_1
    PL_2 = SELECT.PL_2

class MenuButton(QPushButton):
    """A standardized menu button for the game"""
    def __init__(self,
                 text: str,
                 layout_position: Tuple[int,...],
                 ):
        super().__init__(text = text)
        self.setFixedSize(160, 40)
        self.layout_position = layout_position
        self.setStyleSheet(BTN_STYLE_REF)

class GameGroupBox(QGroupBox):
    """A standardized groupbox to contain game elements and serve as an indicator"""
    def __init__(self,
                 style:str,
                 width: int,
                 height: int,
                 ):
        super().__init__()
        self.setFixedSize(width, height)
        self.setStyleSheet(style)
        self.setLayout(QGridLayout())

class GameLabel(QLabel):
    """Label for displaying the number of games won by each player"""
    def __init__(self,
                 text: str,
                 size: int,
                 layout_position: Tuple[int,...],
                 ):
        super().__init__(text = text)
        self.setFixedSize(size, size)
        self.layout_position = layout_position

class GameButton(QPushButton):
    """A standardized square button for the game"""
    def __init__(self,
                 size: int,
                 layout_position: Tuple[int,...],
                 parent_position: Tuple[int,...],
                 get_turn_player: Callable[['GameButton'], TURN],
                 registration: Callable[[Any,Optional[Tuple[int,...]]], None],
                 ):
        super().__init__()
        self.setFixedSize(size, size)
        self.setStyleSheet(get_btn_style(SELECT.DEFAULT_BTN))
        self.layout_position = layout_position
        self.is_claimed: bool = False

        self.take_turn = get_turn_player
        registration(self, parent_position)

    def claim(self):
        '''a user has selected this square, gaining control of it'''
        self.is_claimed = True
        self.setStyleSheet(get_btn_style(self.take_turn(self).value))
        self.setDisabled(True)

    def resetButtonstate(self):
        '''undo button was clicked, reset this square'''
        self.is_claimed = False
        self.setStyleSheet(get_btn_style(SELECT.DEFAULT_BTN))
        self.setEnabled(True)
