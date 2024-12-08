from PyQt6.QtWidgets import QWidget, QCheckBox

class ExtensionCheckbox:
    def __init__(self, extension: str, parent: QWidget, extensions_list: list[str]) -> None:
        """
        Each object of this class is a QCheckBox with a method toggle_extension
        automatically connected to its stateChanged signal.
        The toggling (adding or removing) happens in-place on a provided list.
        """
        
        self.extension = extension
        self.extensions_list = extensions_list
        self.checkbox: QCheckBox = QCheckBox(self.extension, parent) if self.extension else QCheckBox("No extension", parent)
        self.checkbox.stateChanged.connect(self.toggle_extension)


    def toggle_extension(self) -> None:

        if self.checkbox.isChecked():
            self.extensions_list.append(self.extension)
        else:
            self.extensions_list.remove(self.extension)
        