'''Create the startup window.'''
# pylint: disable=no-name-in-module, import-error, fixme
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QTabWidget, QMainWindow

class TabsWidget(QWidget):
    '''Used to implement a tabbed system of splitting widgets'''
    def __init__(self, parent: 'Game'):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0,0,0,0)

        # Initialize the tabs with related widgets. The string arg is the displayed name of the tab
        tabs = QTabWidget()
        tabs.setStyleSheet('QTabBar::tab { height: 40px; width: 250px; font: 16pt }')
        tabs.addTab(QWidget(), "Visualization") # TODO: replace this with Jonah's visualization widget
        self.layout().addWidget(tabs, stretch = 98) #type: ignore  # when layout is QBoxLayout, stretch is a keyword

class Game(QMainWindow):
    '''The main game window'''
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Game')

        self.tabs_widg = TabsWidget(parent = self)
        self.setCentralWidget(self.tabs_widg)

        self.setStyleSheet('background-color: rgb(136, 136, 136)')
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    game = Game()
    game.resize(1200, 800)
    game.show()
    sys.exit(app.exec_())
