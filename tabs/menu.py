'''Groupboxes containing the manual jog buttons'''
# pylint: disable=no-name-in-module, import-error
from typing import Tuple, TYPE_CHECKING
from PyQt5.QtWidgets import QWidget, QGridLayout
from tools.ui_widgets import WAAMGroupBox, QPushButton
from tools.stylesheets import GROUPBOX_STYLE, MACRO_BTN_STYLE
if TYPE_CHECKING:
    from ui import Tabs

class MenuButton(QPushButton):
    """A standardized button for the game"""
    def __init__(self, text: str = '', layout_position: Tuple[int,...] = (0,0)):
        super().__init__(text = text)
        self.setStyleSheet(MACRO_BTN_STYLE)
        self.setFixedSize(160, 40)
        self.layout_position = layout_position

class MenuTab(QWidget):
    '''Contains instances of user_ctrl_widgets submodules'''
    def __init__(self, parent: 'Tabs'):
        super().__init__(parent)
        self.ancestor = parent
        self.setLayout(QGridLayout())

        group_box = MenuBox(parent = self)
        self.layout().addWidget(group_box.groupbox) # type: ignore

class MenuBox(QWidget):
    '''Parent class for GroupBoxes for jogging buttons'''
    def __init__(self, parent: MenuTab):
        super().__init__(parent)
        self.ancestor = parent
        self.groupbox = WAAMGroupBox(GROUPBOX_STYLE, QGridLayout(), width = 700, height = 80)

        start_button = MenuButton("New Game", (0,0,1,1))
        exit_button = MenuButton("Exit Game", (0,1,1,1))
        exit_button.clicked.connect(self.ancestor.ancestor.ancestor.close)

        self.groupbox.layout().addWidget(start_button, *start_button.layout_position)
        self.groupbox.layout().addWidget(exit_button, *exit_button.layout_position)
