'''Standardized style sheets for the game windows.'''

P1_BTN_STYLE = ('''
                QPushButton {
                    color: rgb(0,0,0);\n
                    background-color: rgb(150,105,25);\n
                    font: bold 24pt
                }''')

P2_BTN_STYLE = ('''
                QPushButton {
                    color: rgb(0,0,0);\n
                    background-color: rgb(67,97,117);\n
                    font: bold 24pt
                }''')

P1_TURN_INDICATOR = ('''
                    QGroupBox {
                        background-color: rgb(150,105,25);\n
                        border-width: 4px;\n
                        border-style: ridge;
                    }''')

P2_TURN_INDICATOR = ('''
                    QGroupBox {
                        background-color: rgb(67,97,117);\n
                        border-width: 4px;\n
                        border-style: ridge;
                    }''')

# Applied to QGroupBoxes
GROUPBOX_STYLE = ('''
                    QGroupBox {
                        background-color: rgb(160, 160, 160);\n
                        border-width: 4px;\n
                        border-style: ridge;
                    }''')

DISABLED_GROUPBOX_STYLE = ('''
                           QGroupBox {
                                background-color: rgb(50, 50, 50);\n
                                border-width: 4px;\n
                                border-style: ridge;
                            }''')

BTN_STYLE = ('''
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
