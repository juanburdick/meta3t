'''Create the startup window.'''
# pylint: disable=no-name-in-module, import-error, fixme
import sys
for path in sys.path:
    print(path)
    print("test")
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QTabWidget, QMainWindow
from tools.stylesheets import MAIN_WINDOW_STYLE, TAB_STYLE
from tabs.menu import MenuTab
from tabs.game import GameTab

class Tabs(QWidget):
    '''Used to implement a tabbed system of splitting widgets'''
    def __init__(self, parent: 'HostWindow'):
        super().__init__(parent)
        self.ancestor = parent

        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0,0,0,0)

        # Initialize the tabs with related widgets. The string arg is the displayed name of the tab
        tabs = QTabWidget()
        # tabs.setStyleSheet(TAB_STYLE)
        tabs.addTab(MenuTab(self), "Menu")
        tabs.addTab(GameTab(self), "Game")
        self.layout().addWidget(tabs) #type: ignore  # when layout is QBoxLayout, stretch is a keyword

class HostWindow(QMainWindow):
    '''The main game window'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Meta Tic-Tac-Toe')
        self.setCentralWidget(Tabs(parent = self))
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    game = HostWindow()
    game.resize(700, 720)
    sys.exit(app.exec_())
