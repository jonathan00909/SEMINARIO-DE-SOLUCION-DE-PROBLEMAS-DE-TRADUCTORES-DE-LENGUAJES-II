from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow
import sys

#Aplicacion de Qt
app = QApplication()
#Invocacion de la ventana principal
window = MainWindow()
#Se hace visible la ventana
window.show()
# Qt Loop
sys.exit(app.exec())