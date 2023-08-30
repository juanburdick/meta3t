'''Standardized style sheets for the game windows.'''

MAIN_WINDOW_STYLE = 'background-color: rgb(136, 136, 136)'

TAB_STYLE = 'QTabBar::tab { height: 40px; width: 360px; font: 16pt }'

PLAYER_1_STYLE = ('''
                QPushButton {
                    color: rgb(0,0,0);\n
                    background-color: rgb(150,105,25);\n
                    font: bold 24pt
                  }''')

PLAYER_2_STYLE = ('''
                QPushButton {
                    color: rgb(0,0,0);\n
                    background-color: rgb(67,97,117);\n
                    font: bold 24pt
                  }''')

'''Widget styles to import and apply across the UI'''
# Applied to many of the UI buttons
BTN_STYLE = ('''
            QPushButton {
                color: rgb(0, 0, 0);\nbackground-color: rgb(150, 150, 150);\n
                border-style: ridge;\nborder-width: 4px;\nborder-radius: 20px;\n
                padding: 8px;\nborder-color: rgb(78, 78, 78);\nfont: bold 11.5pt\n
            }
            QPushButton:pressed {
                color: rgb(0, 0, 0);\nbackground-color: rgb(150, 150, 150);\n
                border-style: ridge;\nborder-width: 0px;\nborder-radius: 20px;\n
                padding: 4px;\nborder-color: rgb(78, 78, 78);\nfont: 11.5pt\n
            }''')

# Applied to textboxes
TEXT_STYLE = ('border-style: ridge;\nbackground-color: white;\nborder-color: black;\nborder-width: 4px')

# Applied to QGroupBoxes
GROUPBOX_STYLE = ('''
                QGroupBox {
                    background-color: rgb(160, 160, 160);\nborder-width: 4px;\nborder-style: ridge;
                }''')

# Style used for labels so they blend in with the background of their groupbox widget
BLEND_BACKGROUND_STYLE = ('background-color: rgb(160, 160, 160);\nfont: bold 12pt;')

# Smaller font version of BLEND_BACKGROUND_STYLE
SMALL_BLEND_BACKGROUND_STYLE = ('background-color: rgb(160, 160, 160);\nfont: bold 9pt;')

# Styles for the coordinate system labels, switched when coordinate system is changed
COORD_SYS_ON = ('background-color: rgb(160, 160, 160);\nfont: bold 11pt;\ntext-decoration: underline;')
COORD_SYS_OFF = ('background-color: rgb(160, 160, 160);\nfont: 11pt;')

# Style for the slider bars used for selecting jog and rotation speeds
SLIDER_STYLE = ('''
                    QSlider::groove:horizontal {
                        border-radius: 1px;
                        height: 3px;
                        margin: 0px;
                        background-color: rgb(52, 59, 72);
                    }
                    QSlider::groove:horizontal:hover {
                        background-color: rgb(55, 62, 76);
                    }
                    QSlider::handle:horizontal {
                        background-color: rgb(85, 170, 255);
                        border: none;
                        height: 40px;
                        width: 20px;
                        margin: -20px 0;
                        border-radius: 20px;
                        padding: -20px 0px;
                    }
                    QSlider::handle:horizontal:hover {
                        background-color: rgb(155, 180, 255);
                    }
                    QSlider::handle:horizontal:pressed {
                        background-color: rgb(65, 255, 195);
                    }''')

# Applied to the button that opens the macro menu
MACRO_BTN_STYLE = ('''
            QPushButton {
                color: rgb(0, 0, 0);\nbackground-color: rgb(150, 150, 150);\n
                border-style: ridge;\nborder-width: 4px;\nborder-radius: 20px;\n
                padding: 8px;\nborder-color: rgb(78, 78, 78);\nfont: bold 10pt\n
            }
            QPushButton:pressed {
                color: rgb(0, 0, 0);\nbackground-color: rgb(150, 150, 150);\n
                border-style: ridge;\nborder-width: 0px;\nborder-radius: 20px;\n
                padding: 4px;\nborder-color: rgb(78, 78, 78);\nfont: 10pt\n
            }''')

# Applied to the button that sets the current coordinate system's origin
SET_COORD_SYS_ORIGIN_STYLE = ('''
                                QPushButton {
                                    color: rgb(0, 0, 0);\nbackground-color: rgb(150, 150, 150);\n
                                    border-style: ridge;\nborder-width: 4px;\nborder-radius: 20px;\n
                                    padding: 8px;\nborder-color: rgb(78, 78, 78);\nfont: bold 8pt\n
                                }
                                QPushButton:pressed {
                                    color: rgb(0, 0, 0);\nbackground-color: rgb(150, 150, 150);\n
                                    border-style: ridge;\nborder-width: 0px;\nborder-radius: 20px;\n
                                    padding: 4px;\nborder-color: rgb(78, 78, 78);\nfont: 8pt\n
                                }''')

# Applied to the command log used for macros
COMMMAND_LOG_STYLE = ('border-style: ridge;\nborder-color: black;\nborder-width: 4px')
