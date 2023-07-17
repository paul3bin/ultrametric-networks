"""
AUTHOR: Ebin Paul

REFERENCES: 
    - https://www.geeksforgeeks.org/python-introduction-to-pyqt5/

"""

import sys

from ui.main_window import MainWindow, QApplication

app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
