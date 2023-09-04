from gui.widgets import Window
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon


def main():
    app = QApplication([])
    app.setWindowIcon(QIcon("gui/media/Brush.png"))
    form = Window()

    form.show()
    app.exec()


if __name__ == "__main__":
    main()
