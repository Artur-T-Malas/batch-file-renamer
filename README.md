![RenamerEmpty](./docs/img/renamer_empty.png "Application with no input")
![RenamerWithInput](./docs/img/renamer_with_input.png "Application with input")



## Changelog
### 2024-11-24
1. Fixed CRITICAL bug causing loss of files if some of the files had names that the script would try to rename other files to, which resulted in overwriting and loss of original files

### 2024-11-21
1. Allow user to define the number of leading 0s (padding) in the file numeration
2. By default apply the padding automatically based on the number of files in the choosen directory

## Features to add
- Filename input validation (REGEX) (eg. no "/" and "\\")
- Be able to select specific files to renames (instead of whole directories) - could be with a switch (radio button) to let user decide whether they want whole directory or just some files
- Add a switch (checkbox maybe or iPhone-like switch) to have the number padding only automatic (disable user input) or forced by user (still the default value will be automatic)
- Add a loader (based on the number of files already renamed vs remaining)
- Add choosing of file extensions and option to rename files will extensions (launch an alert dialog because this is dangerous and not recommended)

## Known bugs
- Renamed files may have missing numbers in between them, or the same numbers on two or more files if the extensions are different (eg. after running the script you may end up with both `NewName_1.jpg` and `NewName_1.png` files)
- Script also renames hidden system files like `.DS_Store` and folders/directories if they are in the target folder/directory

## Fixes to do
- Ignore extensions like .DS_Store etc.
- Add typing where possible
- Use logger instead of print functions
- Store logs in a file
- Rework renaming logic
