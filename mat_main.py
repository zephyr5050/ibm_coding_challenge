#============================== IBM Code Challenge =============================
# mat_main.py
#
# Main entry point for the matrix operations program.
#
# Description:
#     This simply creates an application, generates the matrix operation GUI and
#     shows it to the user. This file can be executed directly or launched from
#     the command line via the command 'python main.py'.
#
#===============================================================================

import sys
from PyQt5.QtWidgets import QApplication

from mat_gui import *

def main():
    """
    Main method for creating the Matrix Operation GUI
    """
    
    app = QApplication(sys.argv)
    gui = MatOpGUI()
    app.exec_()

if __name__ == '__main__':
    main()
