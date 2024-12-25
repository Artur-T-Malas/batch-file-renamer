"""
This module holds the logic for BatchFileRenamer application.
This includes the extensions getting, extensions filtering
and actual renaming logic.
"""

import logging
import os


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

    def rename_files(
            self,
            directory: str,
            files_to_rename: list[str],
            new_batch_name: str,
            number_padding: int = 3
        ):

        files_to_rename.sort()

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
