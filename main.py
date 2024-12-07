import sys
from PyQt6.QtWidgets import QApplication

from renamer import BatchFileRenamerApp


def main() -> None:

    # Create an instance of QApplication. Pass in sys.argv to allow command line arguments (not used right now).
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window
    window = BatchFileRenamerApp()
    # Show the window
    window.show()

    # Start the event loop
    app.exec()


if __name__ == "__main__":
    main()