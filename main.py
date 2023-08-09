import sys
from PyQt5.QtWidgets import QApplication
from ui_window import WindowClass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
