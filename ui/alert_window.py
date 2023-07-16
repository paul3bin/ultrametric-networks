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
