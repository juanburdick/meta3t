'''Create the startup window.'''
# pylint: disable=fixme
import sys
from PyQ5.QtWidgets import QApplication, QMainWindow

class Game(QMainWindow):
    '''The main game window'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Game')
        self.setCentralWidget(self.window())

if __name__ == '__main__':
    print('ssh tested')
    app = QApplication([])
    game = Game()
    game.show()
    sys.exit(app.exec_())
