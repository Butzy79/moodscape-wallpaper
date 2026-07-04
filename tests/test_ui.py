import sys
from PyQt6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
w = QLabel("PyQt6 OK su macOS")
w.show()
sys.exit(app.exec())