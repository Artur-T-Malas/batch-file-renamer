"""
This module holds the logic for BatchFileRenamer application.
This includes the extensions getting, extensions filtering
and actual renaming logic.
"""

import logging
import os
import re
from collections.abc import Callable
from re import Pattern
import time

from .models import ISignal


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# Letter, digits, -, _ and spaces
DEFAULT_ALLOWED_PATTERN = r"^[a-zA-Z0-9-_ ]+$"


class Renamer:
    def __init__(self, pattern: str = DEFAULT_ALLOWED_PATTERN) -> None:
        self.pattern: Pattern = re.compile(pattern)

    def get_all_file_extensions(self, path: str) -> set[str]:
        file_list: list[str] = self.filter_directories(path)
        extensions: list[str] = []
        for file in file_list:
            old_name, extension = os.path.splitext(file)
            extensions.append(extension)
        return set(extensions)

    def filter_directories(
        self,
        path: str
    ) -> list[str]:
        file_list: list[str] = os.listdir(path)
        filtered_list: list[str] = [
            file for file in file_list
            if not os.path.isdir(os.path.join(path, file))
        ]
        return filtered_list

    def filter_extensions(
        self,
        file_list: list[str],
        extensions: list[str]
    ) -> list[str]:
        corrected_file_list: list[str] = []
        for file in file_list:
            old_name, extension = os.path.splitext(file)
            if extension in extensions:
                corrected_file_list.append(file)
        return corrected_file_list

    def get_file_number_from_name(
            self,
            filename: str
    ) -> int:
        """
        Returns the number of the file taken from its name.
        Requires the file name to be match this regex pattern:
        `^\S*_\d+.?\S*$` (basically <whatever>_###
        or <whatever>_###.<extension>).
        For more information about patterns and regex visit:
        https://docs.python.org/3/howto/regex.html
        and to try it out visit:
        https://regex101.com/
        """
        split_filename: tuple[str, str] = os.path.splitext(filename)
        filename_without_extension: str = split_filename[0]
        extracted_file_number: str = filename_without_extension.split("_")[-1]
        file_number: int = int(extracted_file_number)
        return file_number

    def get_files_matching_pattern(
            self,
            file_list: list[str],
            pattern: str
    ) -> list[str]:
        """
        Finds and returns names of files which
        match the specified regex pattern.
        For more information about patterns and regex visit:
        https://docs.python.org/3/howto/regex.html
        and to try it out visit:
        https://regex101.com/
        """
        compiled_pattern: Pattern = re.compile(pattern)
        files_matching: list[str] = []
        for file in file_list:
            if re.match(compiled_pattern, file):
                files_matching.append(file)
        return files_matching

    def get_files_matching_range(
            self,
            file_list: list[str],
            max_number: int,
            file_number_getting_function: Callable[[str], int] | None = None
    ) -> list[str]:
        """
        Finds and returns files which have a number
        in the provided range.
        """
        if file_number_getting_function is None:
            file_number_getting_function = self.get_file_number_from_name
        files_matching_range: list[str] = list(
            filter(
                lambda name: file_number_getting_function(name) <= max_number,
                file_list
            )
        )
        return files_matching_range

    def validate_new_name(
            self,
            new_name: str,
            pattern: Pattern | None = None
    ) -> bool:
        """
        Validates the `new_name` by trying to match it
        against REGEX pattern provided or default one,
        stored in `self.pattern` variable, if not explicitly provided.
        """
        pattern = pattern if pattern else self.pattern
        return bool(re.match(pattern, new_name))

    def get_renaming_map(
            self,
            files_to_rename: list[str],
            new_batch_name: str,
            number_padding: int = 3
    ) -> dict[str, str]:
        """
        Prepares and returns a map of old file names to new file names
        (including extensions) to be used for renaming.
        Filters the input file list to check if some files
        have filenames and numbers already matching the pattern
        and removes files and numbers that it finds from the renaming pool.
        """
        files_to_rename.sort()
        max_number: int = len(files_to_rename)
        numbers_pool: list[int] = sorted(list(range(1, max_number + 1)))

        logger.info(f"{files_to_rename=}")

        # Check if any files already have a name that matches the new one
        pattern: str = (
            f"^{new_batch_name}_\d{{{number_padding}}}\.\S*$|"
            f"^{new_batch_name}_\d{{{number_padding}}}$"
        )
        files_with_names_matching_pattern: list[str] = (
            self.get_files_matching_pattern(files_to_rename, pattern)
        )

        # If those files were found, check if their numbers
        # are in the correct range
        files_with_correct_numbers: list[str] = self.get_files_matching_range(
            files_with_names_matching_pattern,
            max_number,
            self.get_file_number_from_name
        )

        # Remove those files and their numbers from the renaming pool
        for file in files_with_correct_numbers:
            files_to_rename.remove(file)
            numbers_pool.remove(self.get_file_number_from_name(file))
        logger.info(
            "Following files have already matching names "
            f"and numbers: {files_with_correct_numbers}"
        )

        files_map: dict[str, str] = {}
        for old_name_with_extension in files_to_rename:
            extension: str = os.path.splitext(old_name_with_extension)[1]
            file_number: int = numbers_pool.pop(0)
            new_name_with_extension: str = (
                f'{new_batch_name}_{str(file_number).zfill(number_padding)}'
                + (extension if extension else '')
            )
            files_map[old_name_with_extension] = new_name_with_extension

        return files_map

    def rename_files_from_file_map(
        self,
        directory: str,
        files_map: dict[str, str]
    ) -> None:
        """Rename files based on the provided map (dict).

        Assume that `keys` are old names and `values` are new names.
        Both `keys` and `values` are assumed to contain necessary
        extensions (or not if files did not have them in the first place).
        """
        logger.info(f'{directory=}')  # DEBUG
        for old_name, new_name in files_map.items():

            if old_name not in os.listdir(directory):
                raise ValueError(
                    f"File {old_name} was not present in the directory. "
                    "Files map is likely incorrect."
                )

            if new_name in os.listdir(directory):
                logger.error(
                    f"File {old_name} could not be renamed to {new_name}, "
                    f"as {new_name} already exists in the directory"
                )
                continue

            old = os.path.join(directory, old_name)
            new = os.path.join(directory, new_name)

            try:
                os.rename(old, new)

            except OSError as e:
                logger.error(
                    f"Failed renaming ({old_name} => {new_name}). "
                    f"{type(e).__name__}: {str(e)}."
                )
                continue

            logger.info(f"Renamed {old_name} => {new_name}")

    def rename_files(
            self,
            directory: str,
            files_to_rename: list[str],
            new_batch_name: str,
            progress_callback: ISignal,
            number_padding: int = 3
    ) -> None:
        """Rename files with the new name and a number.

        Args:
            directory (str): Path to directory containing files to be renamed.
            files_to_rename (list[str]): List of files to be renamed including
                their appropriate extensions.
            new_batch_name (str): New name to be applied
                to all files being renamed.
            number_padding (int): The minimum number of the numeric
                suffix length.
        """

        renaming_map: dict[str, str] = self.get_renaming_map(
            files_to_rename=files_to_rename,
            new_batch_name=new_batch_name,
            number_padding=number_padding
        )

        total: int = len(renaming_map)

        # DEBUG - make the renaming process always run at least 5 s
        sleep_time: float = 5 / total
        logger.info(f'{sleep_time=}')

        for index, key in enumerate(renaming_map):
            self.rename_files_from_file_map(
                directory=directory,
                files_map={key: renaming_map[key]}
            )
            percent_done: float = (index / total) * 100
            progress_callback.emit(percent_done)
            time.sleep(sleep_time)
