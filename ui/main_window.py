import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initiate_ui()

    def initiate_ui(self):
        # Application Name
        # app_name_label = QLabel("UltraNet Viewer")

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
        run_button = QPushButton("Run/Execute")

        # Choose Layout
        layout_label = QLabel("Choose Layout:")
        layout_dropdown = QComboBox()
        layout_dropdown.addItem("Floyd-Warshall")
        layout_dropdown.addItem("UltraNet")

        # Export/Save and Reset/Clear Buttons
        export_button = QPushButton("Export/Save")
        reset_button = QPushButton("Reset/Clear")

        # Layout
        vbox = QVBoxLayout()
        # vbox.addWidget(app_name_label)
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

        vbox.addWidget(run_button)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(layout_label)
        hbox3.addWidget(layout_dropdown)

        vbox.addLayout(hbox3)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(export_button)
        hbox4.addWidget(reset_button)

        vbox.addStretch(1)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)
        self.setWindowTitle("UltraNet Viewer")
        self.setGeometry(100, 100, 400, 400)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
