from PyQt5.QtWidgets import (QComboBox, QDialog, QFileDialog, QLabel,
                             QPushButton, QVBoxLayout)


class ExportVisualisationWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Set the size of the window
        self.setFixedSize(300, 200)

        # Create widgets for the export window
        layout_label = QLabel("Choose Layout:")
        self.layout_dropdown = QComboBox()
        self.layout_dropdown.addItem("Layout 1")
        self.layout_dropdown.addItem("Layout 2")

        file_type_label = QLabel("File Type:")
        self.file_type_dropdown = QComboBox()
        self.file_type_dropdown.addItem("PNG")
        self.file_type_dropdown.addItem("JPEG")
        self.file_type_dropdown.addItem("PDF")

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

    def export(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self,
            "Save File",
            "",
            f"{self.file_type_dropdown.currentText()} Files (*.{self.file_type_dropdown.currentText().lower()})",
        )
        # Process the selected file path as needed
