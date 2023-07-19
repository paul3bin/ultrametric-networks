"""
AUTHOR: Ebin Paul

DESCRIPTION:

REFERENCES:
    - https://www.geeksforgeeks.org/python-introduction-to-pyqt5/
    - https://www.geeksforgeeks.org/pyqt5-setting-disabling-the-frame-of-combobox/
    - https://www.geeksforgeeks.org/pyqt5-setting-font-to-line-editbox-item-of-non-editable-combobox/
    - https://realpython.com/python-pyqt-gui-calculator/
    - https://sabe.io/blog/python-get-file-details
    - https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
    - https://doc.qt.io/qtforpython-5/PySide2/QtGui/QIntValidator.html

"""

import os
import sys
from datetime import datetime
from math import log

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
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

        # instance variables for network related functionality
        self.network = None
        self.threshold = 0
        self.distance_matrix = None
        self.vertices = None
        self.ultrametric_network = None
        self.ultrametric_network_delta = None

        # File Information
        file_info_label = QLabel("File Information")
        self.file_info_textbox = QTextEdit()
        self.file_info_textbox.setReadOnly(True)

        # Algorithm Selection
        algorithm_label = QLabel("Algorithm:")
        self.algorithm_dropdown = QComboBox()
        self.algorithm_dropdown.addItem("Floyd-Warshall")
        self.algorithm_dropdown.addItem("UltraNet")
        self.algorithm_dropdown.setItemData(
            1, Qt.ItemFlags(Qt.ItemIsEnabled), Qt.ItemDataRole.UserRole
        )
        self.algorithm_dropdown.setEnabled(False)

        # Algorithm Parameters
        threshold_label = QLabel("Threshold:")
        self.threshold_input = QLineEdit()
        self.threshold_input.setPlaceholderText("Enter a whole number")
        self.threshold_input.setValidator(QIntValidator())
        self.threshold_input.setEnabled(False)
        self.threshold_input.textChanged.connect(self.update_threshold)

        # Run/Execute Button
        self.run_button = QPushButton("View Ultrametric Network")
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
        vbox.addWidget(self.file_info_textbox)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(algorithm_label)
        hbox1.addWidget(self.algorithm_dropdown)

        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(threshold_label)
        hbox2.addWidget(self.threshold_input)

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

    def update_network(self):
        (
            self.ultrametric_network,
            self.ultrametric_network_delta,
        ) = get_network_edges(self.distance_matrix, self.vertices, self.threshold)

        if self.threshold > 0:
            # Creating an instance of VisualiseNetwork class
            # and assigning it as a instance variable
            self.network = VisualiseNetwork(
                self.vertices, self.ultrametric_network_delta
            )

        else:
            self.network = VisualiseNetwork(self.vertices, self.ultrametric_network)

    def update_threshold(self):
        try:
            if self.threshold_input.text():
                self.threshold = int(self.threshold_input.text())
            else:
                self.threshold = 0

            print(f"{self.threshold_input.text() = }")
            print(f"{self.threshold = }")
            self.update_network()
        except ValueError:
            # If the user enters a non-integer value, set the threshold to 0
            self.threshold = 0

    def load_file_details(self, file_path: str):
        """
        Loads the file details to the non-editable text box of the main window.
        """
        # getting the file size of the selected file
        file_size = os.path.getsize(file_path)

        # Define suffixes for file sizes (B: Bytes, KB: Kilobytes, MB: Megabytes, GB: Gigabytes, TB: Terabytes)
        size_suffixes = ("B", "KB", "MB", "GB", "TB")

        # Calculate the index based on the log of file_size to the base 1024
        # (this will give us the index corresponding to the appropriate size suffix)
        index = min(
            (int(log(file_size, 1024)) if file_size > 0 else 0), len(size_suffixes) - 1
        )

        # Convert the file size to the appropriate unit (B, KB, MB, GB, TB)
        file_size /= 1024**index

        # getting the timestamps and converting them to human-readable format
        date_created = datetime.fromtimestamp(os.path.getctime(file_path))
        last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))

        # Generating text string for the textbox
        text = f"""File Path: {file_path}
        \nFile Size: {file_size:.2f} {size_suffixes[index]} 
        \nDate Created: {date_created.strftime('%Y-%m-%d %H:%M:%S')}
        \nLast Modified: {last_modified.strftime('%Y-%m-%d %H:%M:%S')}"""

        # setting the text to the textbox
        self.file_info_textbox.setText(text)

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
                    QMessageBox.Warning,
                    QMessageBox.Ok | QMessageBox.Cancel,
                )
                error_message.show()
                self.reset_application()  # resetting the application to initial state

            else:
                self.load_file_details(file_path)

                title = file_path.split("\\")[-1].split(".")[0]
                file_extension = file_path.split("\\")[-1].split(".")[1]

                print(f"{file_extension = }")

                # verifying if file path exists
                if os.path.exists(file_path):
                    # calling the nexus parser to obtain distance matrix and list of vertices
                    self.distance_matrix, self.vertices = get_distance_block(file_path)
                    # updating the network instance variable
                    self.update_network()

                else:
                    error_message = MessageBox(
                        "File not found",
                        "File does not exists!",
                        QMessageBox.warning,
                        QMessageBox.Ok | QMessageBox.Cancel,
                    )
                    self.reset_application()

                    error_message.show()

                self.enable_widgets()

    def enable_widgets(self):
        """
        the method enables the run, export buttons and threshold field
        """
        self.run_button.setEnabled(True)
        self.export_button.setEnabled(True)
        self.threshold_input.setEnabled(True)

    def reset_application(self):
        self.run_button.setEnabled(False)
        self.export_button.setEnabled(False)
        self.threshold_input.setEnabled(False)
        self.network = None
        self.threshold = 0
        self.distance_matrix = None
        self.vertices = None
        self.ultrametric_network = None
        self.ultrametric_network_delta = None

    def open_export_window(self):
        export_window = ExportVisualisationWindow(self.network)
        export_window.exec_()

    def view_network(self):
        # uses the object of NetworkVisualiser class to view network
        self.network.display()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
