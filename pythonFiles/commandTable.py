import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QHeaderView, QStyleFactory
from PyQt5.QtCore import Qt

class TableWindow(QMainWindow):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.setWindowTitle("Voice Commands")
        self.setFixedHeight(400)
        self.setStyleSheet("background-color: #222222; color: white;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.load_data(filename)

        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_row)
        self.layout.addWidget(self.add_row_button)

        self.delete_row_button = QPushButton("Delete Row")
        self.delete_row_button.clicked.connect(self.delete_row)
        self.layout.addWidget(self.delete_row_button)

        self.table.cellChanged.connect(self.save_changes)

    def load_data(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        row_count = len(lines)
        col_count = 2

        self.table.setRowCount(row_count)
        self.table.setColumnCount(col_count)

        for i, line in enumerate(lines):
            items = line.strip().split(',')
            for j, item in enumerate(items):
                if j < 2:
                    cell = QTableWidgetItem(item)
                    cell.setFlags(cell.flags() | Qt.ItemIsEditable)  # Set cells as editable
                    self.table.setItem(i, j, cell)

        table_width = self.table.verticalScrollBar().width() + sum([self.table.columnWidth(j) for j in range(self.table.columnCount())]) + 20
        if table_width > 300:
            first_column_width = 175
            second_column_width = 125 - first_column_width - self.table.verticalScrollBar().width() - 20

            self.table.setColumnWidth(0, first_column_width)
            self.table.setColumnWidth(1, second_column_width)

        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalScrollBar().setStyleSheet("QScrollBar:vertical {background: #333333;}")
        self.table.verticalScrollBar().setStyleSheet("QScrollBar:horizontal {background: #333333;}")
        self.table.setStyleSheet("QTableWidget {background-color: #333333; border: none;} "
                                 "QHeaderView::section {background-color: #444444; color: white; border: none;}"
                                 "QTableWidget QScrollBar:vertical {background-color: #333333;}"
                                 "QTableWidget QScrollBar:horizontal {background-color: #333333;}")

        # Set word wrap for the entire table
        self.table.setWordWrap(True)

        self.setFixedWidth(310)

    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        for column in range(self.table.columnCount()):
            self.table.setItem(row_position, column, QTableWidgetItem(""))
        self.table.scrollToBottom()

    def delete_row(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)
            self.save_to_file()

    def save_changes(self, row, column):
        self.save_to_file()

    def save_to_file(self):
        with open(self.filename, 'w') as file:
            for row in range(self.table.rowCount()):
                line = ','.join(self.table.item(row, col).text() if self.table.item(row, col) is not None else "" for col in range(self.table.columnCount()))
                file.write(line + '\n')
    
    #def closeEvent(self, event):
    #    event.ignore()  # Ignore the default close event
    #    self.hide()  # Hide the window instead of closing it    

def launch_table(filename):
    with open(filename, "a") as f:
        pass
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))  # Set Fusion style (modern style)
    window = TableWindow(filename)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_table("commands.txt")
