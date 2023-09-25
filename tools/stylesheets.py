'''Standardized style sheets for the game windows.'''
from enum import Enum

_PLAYER_1_COLOR = (150,105,25,255)
_PLAYER_2_COLOR = (67,97,117,255)
# _DEFAULT = (160,160,160,255)
# _DEFAULT = (136,136,136,255)
# _DISABLED = (50,50,50,255)

class SELECT(Enum):
    '''enum for colors'''
    PL_1 = _PLAYER_1_COLOR, 'image: url(tic_tac_toe_X.png)'
    PL_2 = _PLAYER_2_COLOR, 'image: url(tic_tac_toe_O.png)'
    DEFAULT_BTN = (128,131,135,255), ''
    DISABLED_BTN = (130,130,130,100), ''
    DEFAULT_BOX = (22,25,37,255), ''
    DISABLED_BOX = (22,25,25,255), ''

def get_btn_style(select: SELECT) -> str:
    '''get button style for selected player'''
    color, image = select.value
    return f'''QPushButton {{
                    color: rgb(0,0,0);
                    background-color: rgba{color};
                    font: bold 24pt;
                    {image}}}'''

def get_box_style(select: SELECT) -> str:
    '''get button style for selected player'''
    color, _ = select.value
    return f'''QGroupBox {{
                    background-color: rgba{color};
                    border-width: 4px;
                    border-style: ridge;
                }}'''

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
