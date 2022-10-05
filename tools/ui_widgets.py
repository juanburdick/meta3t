'''Used for easily initializing widgets, meant to reduce the repeated calls which specify the respective fields of similar widgets'''
# pylint: disable=C0321, no-name-in-module, too-many-arguments
from enum import Enum
from typing import List, Tuple, Optional, Union
from PyQt5.QtWidgets import QPushButton, QLabel, QGroupBox, QGridLayout, QVBoxLayout, QToolButton, QLineEdit, QTextEdit, QRadioButton
from PyQt5.QtGui import QValidator
from PyQt5.QtCore import Qt

class SquareState(Enum):
    '''Store the available jog intervals'''
    PLAYER_A = 1
    PLAYER_B = -1
    PLAYER_NONE = 0

class GameButton(QPushButton):
    """A standardized button for the game"""
    def __init__(self, text: str = '', style: str = '', width: Optional[int] = None, height: Optional[int] = None, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(text = text)
        self.setStyleSheet(style)
        if width: self.setFixedWidth(width)
        if height: self.setFixedHeight(height)
        self.layout_position = layout_position

class WAAMToolButton(QToolButton):
    """A standardized button for the WAAM GUI"""
    def __init__(self, increment_key: str, continuous_key: str, text: str = '', style: str = '', width: Optional[int] = None, height: Optional[int] = None,
                       layout_position: Tuple[int,...] = (0,0), arrow: Optional[Qt.ArrowType] = None, multiplier: int = 1, is_rotation: bool = False):
        super().__init__()
        self.setText(text)
        self.increment_key = increment_key
        self.continuous_key = continuous_key
        self.setStyleSheet(style)
        if width: self.setFixedWidth(width)
        if height: self.setFixedHeight(height)
        if arrow: self. setArrowType(arrow)
        self.layout_position = layout_position
        self.multiplier = multiplier
        self.is_rotation = is_rotation

class GameLabel(QLabel):
    """A standardized label for the game"""
    def __init__(self, text: str, style: str = '', width: Optional[int] = None, height: Optional[int] = None, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(text = text)
        self.setStyleSheet(style)
        if width: self.setFixedWidth(width)
        if height: self.setFixedHeight(height)
        self.layout_position = layout_position

class WAAMLineEdit(QLineEdit):
    """A standard line edit widget for the WAAM GUI"""
    def __init__(self, text: str = '', style: str = '', width: Optional[int] = None, height: Optional[int] = None, layout_position: Tuple[int,...] = (0,0), validator: Optional[QValidator] = None):
        super().__init__(text)
        self.setStyleSheet(style)
        if width: self.setFixedWidth(width)
        if height: self.setFixedHeight(height)
        if validator: self.setValidator(validator)
        self.layout_position = layout_position

class WAAMTextEdit(QTextEdit):
    """A standard line edit widget for the WAAM GUI"""
    def __init__(self, text: str = '', style: str = '', width: Optional[int] = None, height: Optional[int] = None, layout_position: Tuple[int,...] = (0,0)):
        super().__init__(text)
        self.setStyleSheet(style)
        if width: self.setFixedWidth(width)
        if height: self.setFixedHeight(height)
        self.layout_position = layout_position

class WAAMGroupBox(QGroupBox):
    """A standard groub box widget for the WAAM GUI"""
    def __init__(self, style:str, layout: Union[QGridLayout, QVBoxLayout], width: Optional[int] = None, height: Optional[int] = None):
        super().__init__()
        self.setStyleSheet(style)
        self.setLayout(layout)
        if width: self.setFixedWidth(width)
        if height: self.setFixedHeight(height)

class WAAMRadioButton(QRadioButton):
    """A standard radio button for the WAAM GUI"""
    def __init__(self, text: str, style: str = ''):
        super().__init__()
        self.setText(text)
        self.setStyleSheet(style)
        self.interval = None
