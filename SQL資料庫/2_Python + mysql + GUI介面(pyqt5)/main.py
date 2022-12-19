#要執行的時候跑此檔案，F5即可跑全部程式(main)

import sys
from PyQt5.QtWidgets import QApplication

from main_control import MainWindow #載入邏輯判斷(mainwindow.py)檔


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())