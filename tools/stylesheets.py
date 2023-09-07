'''Standardized style sheets for the game windows.'''
from enum import Enum

_PLAYER_1_COLOR = (150,105,25,255)
_PLAYER_2_COLOR = (67,97,117,255)

class BTN_STYLE(Enum):
    '''enum for button colors'''
    PL_1 = _PLAYER_1_COLOR
    PL_2 = _PLAYER_2_COLOR
    DEFAULT = (136,136,136,255)
    DISABLED = (130,130,130,100)

class BOX_STYLE(Enum):
    '''enum for box colors'''
    PL_1 = _PLAYER_1_COLOR
    PL_2 = _PLAYER_2_COLOR
    DEFAULT = (160,160,160,255)
    DISABLED = (50,50,50,255)

def get_style(select: BTN_STYLE | BOX_STYLE) -> str:
    '''get button style for selected player'''
    if isinstance(select, BTN_STYLE):
        return (f'''QPushButton {{
                        color: rgb(0,0,0);
                        background-color: rgba{select.value};
                        font: bold 24pt
                    }}''')
    if isinstance(select, BOX_STYLE):
        return (f'''QGroupBox {{
                        background-color: rgba{select.value};
                        border-width: 4px;
                        border-style: ridge;
                    }}''')
    else:
        return ''

BTN_STYLE_REF = ('''
            QPushButton {
                background-color: rgb(150, 150, 150);\n

                font: bold 11.5pt;\n
                color: rgb(0, 0, 0);\n

                padding: 8px;\n

                border-style: ridge;\n
                border-width: 4px;\n
                border-radius: 20px;\n
                border-color: rgb(78, 78, 78);\n
            }
            QPushButton:pressed {
                background-color: rgb(150, 150, 150);\n

                font: 11.5pt;\n
                color: rgb(0, 0, 0);\n

                padding: 4px;\n

                border-style: ridge;\n
                border-width: 0px;\n
                border-radius: 20px;\n
                border-color: rgb(78, 78, 78);\n
            }''')
