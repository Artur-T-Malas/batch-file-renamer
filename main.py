import sys
from PyQt6.QtWidgets import QApplication

from core.renamer import Renamer
from gui.app_layout import AppLayout
from gui.app_main_window import AppMainWindow


def main() -> None:

    app = QApplication(sys.argv)

    renamer = Renamer()
    layout = AppLayout(renamer)
    window = AppMainWindow(layout, "Batch File Renamer")

    window.show()
    app.exec()


if __name__ == "__main__":
    main()
