import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from MainWindow import MainWindow


def exception_hook(type_, value, tb):
    # logger.error('Unhandled top level exception:\n%s', ''.join(traceback.format_exception(type_, value, tb)))
    # print(type_, value, tb)
    print(traceback.format_exception(type_, value, tb))


# Точка входа приложения
if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
