import sys
from PyQt5.QtWidgets import QApplication

from frontend.main_widget import MainWidget

if __name__ == "__main__":
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)
    sys.__excepthoock__ = hook  # para que muestre los errores si se cae
    
    app = QApplication(sys.argv)
    mw = MainWidget()
    mw.show()
    sys.exit(app.exec_())
