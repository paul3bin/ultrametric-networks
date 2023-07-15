import sys
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initiate_ui()

    def initiate_ui(self):
        self.selected_file = None

        # File Information
        file_info_label = QLabel("File Information")
        file_info_textbox = QTextEdit()
        file_info_textbox.setReadOnly(True)

        # Algorithm Selection
        algorithm_label = QLabel("Algorithm:")
        algorithm_dropdown = QComboBox()
        algorithm_dropdown.addItem("Algorithm 1")
        algorithm_dropdown.addItem("Algorithm 2")

        # Algorithm Parameters
        threshold_label = QLabel("Threshold:")
        threshold_input = QLineEdit()

        # Run/Execute Button
        self.run_button = QPushButton("Run/Execute")
        self.run_button.setEnabled(False)

        # Choose Layout
        layout_label = QLabel("Choose Layout:")
        layout_dropdown = QComboBox()
        layout_dropdown.addItem("Floyd-Warshall")
        layout_dropdown.addItem("UltraNet")

        # Export/Save Button
        self.export_button = QPushButton("Export/Save")
        self.export_button.setEnabled(False)

        # Reset/Clear Button
        reset_button = QPushButton("Reset/Clear")
        reset_button.clicked.connect(self.reset_action)

        # File Selection Button
        select_file_button = QPushButton("Select File")
        select_file_button.clicked.connect(self.open_file_dialog)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(file_info_label)
        vbox.addWidget(file_info_textbox)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(algorithm_label)
        hbox1.addWidget(algorithm_dropdown)

        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(threshold_label)
        hbox2.addWidget(threshold_input)

        vbox.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.run_button)
        hbox3.addWidget(layout_label)
        hbox3.addWidget(layout_dropdown)

        vbox.addLayout(hbox3)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.export_button)
        hbox4.addWidget(reset_button)

        vbox.addStretch(1)
        vbox.addLayout(hbox4)
        vbox.addWidget(select_file_button)

        self.setLayout(vbox)
        self.setWindowTitle("UltraNet Viewer")
        self.setGeometry(100, 100, 400, 400)
        self.show()

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Choose Nexus File")
        if file_path:
            self.selected_file = file_path
            self.enable_buttons()

    def enable_buttons(self):
        self.run_button.setEnabled(True)
        self.export_button.setEnabled(True)

    def reset_action(self):
        self.run_button.setEnabled(False)
        self.export_button.setEnabled(False)
        self.selected_file = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
