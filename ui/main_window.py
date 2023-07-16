import os
import sys

from PyQt5.QtWidgets import (QApplication, QComboBox, QFileDialog, QHBoxLayout,
                             QLabel, QLineEdit, QMessageBox, QPushButton,
                             QTextEdit, QVBoxLayout, QWidget)

from algorithms.floyd_warshall import get_network_edges
from utils.nexus_parser import get_distance_block
from utils.visualizer import VisualiseNetwork

from .alert_window import MessageBox
from .export_window import ExportVisualisationWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file = None
        self.network = None

        # File Information
        file_info_label = QLabel("File Information")
        file_info_textbox = QTextEdit()
        file_info_textbox.setReadOnly(True)

        # Algorithm Selection
        algorithm_label = QLabel("Algorithm:")
        algorithm_dropdown = QComboBox()
        algorithm_dropdown.addItem("Floyd-Warshall")
        algorithm_dropdown.addItem("UltraNet")
        algorithm_dropdown.setItemData(1, Qt.ItemFlags(Qt.ItemIsEnabled), Qt.ItemFlags)

        # Algorithm Parameters
        threshold_label = QLabel("Threshold:")
        threshold_input = QLineEdit()

        # Run/Execute Button
        self.run_button = QPushButton("Run/Execute")
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.view_network)

        # Export/Save Button
        self.export_button = QPushButton("Export Network")
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.open_export_window)

        # Reset/Clear Button
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_application)

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

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.export_button)
        hbox4.addWidget(reset_button)
        hbox4.addWidget(select_file_button)

        vbox.addStretch(1)
        vbox.addLayout(hbox4)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.run_button)

        vbox.addLayout(hbox3)

        self.setLayout(vbox)
        self.setWindowTitle("UltraNet Viewer")
        self.setGeometry(100, 100, 400, 400)
        self.show()

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Choose Nexus File")
        if file_path:
            # getting the file extension of the selected file
            file_extension = file_path.split("\\")[-1].split(".")[-1]
            print(f"{file_extension = }")

            # checking if the selected file is nexus format or not.
            if file_extension not in ("nex", "nexus"):
                # creating an object of MessageBox for raising error message
                error_message = MessageBox(
                    "Wrong file type",
                    "Selected file should be a nexus file",
                    QMessageBox.Warning,  # Corrected icon enum value
                    QMessageBox.Ok | QMessageBox.Cancel,
                )
                error_message.show()
                self.reset_application()  # resetting the application to initial state

            else:
                self.selected_file = file_path
                self.enable_buttons()

    def enable_buttons(self):
        self.run_button.setEnabled(True)
        self.export_button.setEnabled(True)

    def reset_application(self):
        self.run_button.setEnabled(False)
        self.export_button.setEnabled(False)
        self.selected_file = None

    def open_export_window(self):
        export_window = ExportVisualisationWindow()
        export_window.exec_()

    def view_network(self):
        file_path = self.selected_file
        title = file_path.split("\\")[-1].split(".")[0]
        file_extension = file_path.split("\\")[-1].split(".")[1]

        print(f"{file_extension = }")

        # verifying if file path exists
        if os.path.exists(file_path):
            distance_matrix, vertices = get_distance_block(file_path)

            ultrametric_network, ultrametric_network_delta = get_network_edges(
                distance_matrix, vertices
            )

            print(f"{ultrametric_network = }")

            self.network = VisualiseNetwork(vertices, ultrametric_network, title)

            self.network.display()

        else:
            error_message = MessageBox(
                "File not found",
                "File does not exists!",
                QMessageBox.warning,
                QMessageBox.Ok | QMessageBox.Cancel,
            )
            self.reset_application()

            error_message.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
