"""
AUTHOR: Ebin Paul

"""

import os

from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from ui.alert_window import MessageBox
from utils.visualizer import VisualiseNetwork


class ExportVisualisationWindow(QDialog):
    def __init__(self, network: VisualiseNetwork):
        super().__init__()

        # Set the size of the window
        self.setFixedSize(300, 200)
        self.network = network
        self.file_type = "png"
        self.network_layout = "Spring"

        # Create widgets for the export window
        layout_label = QLabel("Choose Layout:")
        self.layout_dropdown = QComboBox()
        self.layout_dropdown.addItem("Spring")
        self.layout_dropdown.addItem("Random")
        self.layout_dropdown.addItem("Shell")
        self.layout_dropdown.addItem("Circular")
        self.layout_dropdown.addItem("Planar")
        self.layout_dropdown.currentIndexChanged.connect(self.update_layout)

        file_type_label = QLabel("File Type:")
        self.file_type_dropdown = QComboBox()
        self.file_type_dropdown.addItem("PNG")
        self.file_type_dropdown.addItem("JPEG")
        self.file_type_dropdown.addItem("PDF")
        self.file_type_dropdown.currentIndexChanged.connect(self.update_file_type)

        export_button = QPushButton("Export")
        export_button.clicked.connect(self.export)

        # Create layout for the export window
        layout = QVBoxLayout()
        layout.addWidget(layout_label)
        layout.addWidget(self.layout_dropdown)
        layout.addWidget(file_type_label)
        layout.addWidget(self.file_type_dropdown)
        layout.addWidget(export_button)

        self.setWindowTitle("Export Visualisation")

        self.setLayout(layout)

    def update_layout(self, index):
        self.network_layout = self.layout_dropdown.currentText()

    def update_file_type(self, index):
        self.file_type = self.file_type_dropdown.currentText()

    def export(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self,
            "Save File",
            "",
            f"{self.file_type} Files (*.{self.file_type.lower()})",
        )
        print(f"{file_path = }")
        if file_path:
            # Check if a valid filename was entered
            filename = os.path.basename(file_path)

            print(f"{filename = }")
            if filename:
                self.network.export_to_file(
                    file_path=file_path,
                    layout=self.network_layout,
                    file_type=self.file_type.lower(),
                )
                self.accept()
            else:
                # Show an error message indicating that a filename is required
                error_message = MessageBox(
                    "Error",
                    "Please enter a filename.",
                    QMessageBox.warning,
                    QMessageBox.Ok | QMessageBox.Cancel,
                )

        else:
            # The user canceled the save file operation
            self.path = None
