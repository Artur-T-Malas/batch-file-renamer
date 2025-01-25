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


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Renamer:
    def __init__(self): ...

    def get_all_file_extensions(self, path) -> set[str]:
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
        filtered_list: list[str] = [file for file in file_list if not os.path.isdir(os.path.join(path, file))]
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
        `^\S*_\d+.?\S*$` (basically <whatever>_### or <whatever>_###.<extension>)
        For more information about patterns and regex visit:
        https://docs.python.org/3/howto/regex.html
        and to try it out visit:
        https://regex101.com/
        """
        split_filename: list[str] = filename.split(".")
        filename_without_extension: str = ''.join(split_filename[:-1] if len(split_filename) > 1 else split_filename)
        extracted_file_number: str = filename_without_extension.split("_")[-1]
        file_number: int = int(extracted_file_number)
        return file_number


    def get_files_matching_pattern(
            self,
            file_list: list[str],
            pattern: str
    ) -> list[str]:
        """
        Finds and returns names of files which match the specified regex pattern.
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
        files_matching_range: list[str] = list(filter(lambda name: file_number_getting_function(name) <= max_number, file_list))
        return files_matching_range


    def rename_files(
            self,
            directory: str,
            files_to_rename: list[str],
            new_batch_name: str,
            number_padding: int = 3
        ):

        files_to_rename.sort()
        max_number: int = len(files_to_rename)
        numbers_pool: set = set(range(max_number + 1))

        logger.info(f"{files_to_rename = }")

        # Check if any files already have a name that matches the new one
        pattern: str = f"^{new_batch_name}_\d{{{number_padding}}}.?\S*$"
        files_with_names_matching_pattern: list[str] = self.get_files_matching_pattern(files_to_rename, pattern)

        # If those files were found, check if their numbers are in the correct range
        files_with_correct_numbers: list[str] = self.get_files_matching_range(
            files_with_names_matching_pattern,
            max_number,
            self.get_file_number_from_name
        )
        #   If yes, 
        #       remove those numbers from the pool, 
        #       and remove those files from the list of files_to_rename
        for file in files_with_correct_numbers:
            files_to_rename.remove(file)
            numbers_pool.remove(self.get_file_number_from_name(file))
        #   If not, 
        #       don't do anything

        logger.info(f"After looking for already renamed files: {files_to_rename = }")

        # TODO:
        # Instead of the complicated logic, since we've already checked for files already renamed to
        # our format, don't do the actual renaming in this method
        # and just do the mapping of "old" -> "new" and execute it somewhere else
        # this way this function's logic will be testable!


        i = 1

        for file in files_to_rename:

            old_name, extension = os.path.splitext(file)
            new_name = f'{new_batch_name}_{str(i).zfill(number_padding)}'

            # While a file with the new name already exists in the directory,
            # try to find either the first available name or to leave the file's current name if it matches
            if new_name in [os.path.splitext(file_name)[0] for file_name in os.listdir(directory)] and f"{new_name}{extension}" != file:
                logger.debug(f"File {old_name}{extension} not renamed, because {new_name}{extension} already exists in directory.")
                k = 1
                while new_name in [os.path.splitext(file_name)[0] for file_name in os.listdir(directory)] and f"{new_name}{extension}" != file:
                    new_name = f'{new_batch_name}_{str(k).zfill(number_padding)}'
                    logger.debug(f'\tTrying {new_name}{extension}')
                    k += 1
                    i = k

            # If a file's name will not change, continue
            if file == f"{new_name}{extension}":
                logger.info(f"File {old_name}{extension} not renamed - new name the same as old name.")
                i += 1
                continue

            old = os.path.join(directory, f'{old_name}{extension}')
            new = os.path.join(directory, f'{new_name}{extension}')

            os.rename(old, new)
            logger.info(f"{old_name}{extension} => {new_name}{extension}")

            i += 1
