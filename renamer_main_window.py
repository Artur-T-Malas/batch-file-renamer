from typing import Callable

from PyQt6.QtWidgets import QMainWindow

from renamer_layout import RenamerLayout
from renamer import BatchFileRenamer


class RenamerMainWindow(QMainWindow):
    def __init__(
            self,
            renamer: BatchFileRenamer
        ):
        super().__init__()

        self.setWindowTitle("Batch File Renamer")

        self.app = RenamerLayout(renamer)

        self.setCentralWidget(self.app)
