import sys
from PyQt6.QtWidgets import QApplication

from renamer import BatchFileRenamer
from renamer_main_window import RenamerMainWindow


def main() -> None:

    # Create an instance of QApplication. Pass in sys.argv to allow command line arguments (not used right now).
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window
    renamer = BatchFileRenamer()
    window = RenamerMainWindow(renamer)
    # Show the window
    window.show()

    # Start the event loop
    app.exec()


if __name__ == "__main__":
    main()