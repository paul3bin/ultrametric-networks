"""
AUTHOR: Ebin Paul

"""

import sys

from ui.main_window import MainWindow, QApplication

app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
