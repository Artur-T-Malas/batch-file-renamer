import sys
from PySide6.QtWidgets import QApplication

from app.core.renamer import Renamer
from app.gui.app_layout import AppLayout
from app.gui.app_main_window import AppMainWindow


def main() -> None:

    app = QApplication(sys.argv)

    renamer = Renamer()
    layout = AppLayout(renamer)
    window = AppMainWindow(layout, "Batch File Renamer")

    window.show()
    app.exec()


if __name__ == "__main__":
    main()
