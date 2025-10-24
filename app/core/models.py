from typing import Protocol
from re import Pattern


class Renamer(Protocol):
    """Protocol class for a file renamer used by the application.

    Used for static type checking without having
    to import the actual `Renamer` class.

    Provides a blueprint for creating other file renamers
    to be used plug&play in the GUI app.
    """
    def __init__(self, pattern: str) -> None:
        ...

    def get_all_file_extensions(self, path: str) -> set[str]:
        ...

    def filter_directories(self, path: str) -> list[str]:
        ...

    def filter_extensions(
            self,
            file_list: list[str],
            extensions: list[str]
    ) -> list[str]:
        ...

    def validate_new_name(
            self,
            new_name: str,
            pattern: Pattern | None = None
    ) -> bool:
        ...

    def get_renaming_map(
            self,
            files_to_rename: list[str],
            new_batch_name: str,
            number_padding: int = 3
    ) -> dict[str, str]:
        ...

    def rename_files(
            self,
            directory: str,
            files_map: dict[str, str]
    ) -> None:
        ...
