from PySide6.QtWidgets import QWidget, QCheckBox, QGroupBox


class ExtensionCheckbox:
    def __init__(
            self,
            extension: str,
            parent: QWidget,
            extensions_list: list[str],
            renaming_group_box: QGroupBox | None = None
    ) -> None:
        """
        Each object of this class is a QCheckBox with a method toggle_extension
        automatically connected to its stateChanged signal.
        The toggling (adding or removing) happens in-place on a provided list.
        """

        self.extension = extension
        if self.extension:
            self.checkbox: QCheckBox = QCheckBox(self.extension, parent)
        else:
            self.checkbox = QCheckBox("No extension", parent)

        self.extensions_list = extensions_list
        self.checkbox.stateChanged.connect(self.toggle_extension)
        self.renaming_group_box: QGroupBox | None = renaming_group_box

    def toggle_extension(self) -> None:

        if self.checkbox.isChecked():
            self.extensions_list.append(self.extension)
        else:
            self.extensions_list.remove(self.extension)

        if self.renaming_group_box is not None:
            self.renaming_group_box.setEnabled(len(self.extensions_list) > 0)
