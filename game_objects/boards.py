'''Contains the game board and menu objects, which function as containers and represent the game state'''
from typing import List, Tuple, Optional, Callable, Any
from itertools import product
from PyQt5.QtWidgets import QWidget
from game_objects.buttons import MenuButton, GameButton, GameGroupBox, TURN
from game_objects.stylesheets import get_btn_style, get_box_style,SELECT

_GAME_SIZE = 700
_MENU_SIZE = 80
_BOX_SIZE = 220
_BTN_SIZE = 60
_CLAIMED_SIZE = 195

class MenuBox(QWidget):
    '''Parent class for GroupBoxes for jogging buttons'''
    def __init__(self,
                 layout_position: Tuple[int,...],
                 registration: Callable[[Any,Optional[Tuple[int,...]]], None],
                 new_game_method: Callable,
                 undo_method: Callable,
                 exit_method: Callable,
                 ):
        super().__init__()
        self.layout_position = layout_position
        self.groupbox = GameGroupBox(get_box_style(SELECT.PL_1), width = _GAME_SIZE, height = _MENU_SIZE)

        reset_button = MenuButton("New Game", (0,0,1,1))
        reset_button.clicked.connect(new_game_method)
        self.groupbox.layout().addWidget(reset_button, *reset_button.layout_position)

        undo_button = MenuButton("Undo", (0,1,1,1))
        undo_button.clicked.connect(undo_method)
        self.groupbox.layout().addWidget(undo_button, *undo_button.layout_position)

        exit_button = MenuButton("Exit Game", (0,2,1,1))
        exit_button.clicked.connect(exit_method)
        self.groupbox.layout().addWidget(exit_button, *exit_button.layout_position)

        registration(self, None)

    def update_turn_indicator(self, is_player_one: bool):
        '''update the color of the groupbox to indicate which player's turn it is'''
        self.groupbox.setStyleSheet(get_box_style(SELECT.PL_1 if is_player_one else SELECT.PL_2))

class MetaBoard(QWidget):
    '''Contain and track the main game/game board'''
    def __init__(self,
                 size: int,
                 layout_position: Tuple[int,...],
                 get_turn_player: Callable[[GameButton], TURN],
                 registration: Callable[[Any,Optional[Tuple[int,...]]], None],
                 ):
        super().__init__()
        self.groupbox = GameGroupBox(get_box_style(SELECT.PL_1), size, size)
        self.layout_position = layout_position

        for position in product((0,1,2), repeat = 2):
            subgame = SubGameBoard(_BOX_SIZE, position, get_turn_player, registration)
            self.groupbox.layout().addWidget(subgame.groupbox, *subgame.layout_position) # type: ignore

        registration(self, None)

    def update_turn_indicator(self, is_player_one: bool):
        '''update the color of the groupbox to indicate which player's turn it is'''
        self.groupbox.setStyleSheet(get_box_style(SELECT.PL_1 if is_player_one else SELECT.PL_2))

class SubGameBoard(QWidget):
    '''Contains a subgame of tic tac toe'''
    def __init__(self,
                 size: int,
                 layout_position : Tuple[int,...],
                 get_turn_player: Callable[[GameButton], TURN],
                 registration: Callable[[Any,Optional[Tuple[int,...]]], None],
                ):
        super().__init__()

        self.groupbox = GameGroupBox(get_box_style(SELECT.DEFAULT_BOX), size, size)
        self.layout_position = layout_position
        self.is_claimed: bool = False

        self.buttons: List[GameButton] = []
        self.claimed_button = GameButton('x', _CLAIMED_SIZE, (0,0), self.layout_position, get_turn_player, registration)

        for position in product((0,1,2), repeat = 2):
            button = GameButton('', _BTN_SIZE, position, self.layout_position, get_turn_player, registration)
            button.clicked.connect(button.claim)
            self.groupbox.layout().addWidget(button, *position) # type: ignore
            self.buttons.append(button)

        if self.layout_position == (0,0):
            self.claim_board()

        registration(self, None)

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
