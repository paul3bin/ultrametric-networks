"""
AUTHOR: Ebin Paul

DESCRIPTION: The code snippet provided defines a class called MessageBox that encapsulates 
             the functionality of displaying a message box using PyQt5's QMessageBox. This 
             class allows for easy creation and display of customized message boxes with 
             various features.

REFERENCES:
    - https://www.geeksforgeeks.org/pyqt5-message-box/
    - https://pythonprogramminglanguage.com/pyqt5-message-box/

"""


from PyQt5.QtWidgets import QMessageBox


class MessageBox:
    def __init__(
        self, title, text, icon=QMessageBox.Information, buttons=QMessageBox.Ok
    ):
        self.title = title
        self.text = text
        self.icon = icon
        self.buttons = buttons

    def show(self):
        message_box = QMessageBox()
        message_box.setIcon(self.icon)
        message_box.setWindowTitle(self.title)
        message_box.setText(self.text)
        message_box.setStandardButtons(self.buttons)
        message_box.exec_()
