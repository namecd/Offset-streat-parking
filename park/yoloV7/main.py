import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_banben1 import *

# app = QApplication(sys.argv)
# mainwindow = QMainWindow()
# ui = Ui_MainWindow()
# ui.setupUi(mainwindow)
# mainwindow.show()
# sys.exit(app.exec_())

if __name__ == '__main__':
    # ui = Ui_MainWindow()
    app = QApplication(sys.argv)
    mainwindow = QMainWindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())



