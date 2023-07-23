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
    """
    A class to display message boxes using PyQt5.

    Parameters:
        title (str): The title of the message box.
        text (str): The text to be displayed in the message box.
        icon (int, optional): The icon to be shown in the message box. Default is QMessageBox.Information.
        buttons (int, optional): The buttons to be displayed in the message box. Default is QMessageBox.Ok.
    """

    def __init__(
        self, title, text, icon=QMessageBox.Information, buttons=QMessageBox.Ok
    ):
        self.title = title
        self.text = text
        self.icon = icon
        self.buttons = buttons

    def show(self):
        """
        Display the message box with the specified parameters.

        Returns:
            int: The button that was clicked by the user.
        """
        message_box = QMessageBox()
        message_box.setIcon(self.icon)
        message_box.setWindowTitle(self.title)
        message_box.setText(self.text)
        message_box.setStandardButtons(self.buttons)
        message_box.exec_()
