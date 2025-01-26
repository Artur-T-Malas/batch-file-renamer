![RenamerEmpty](./docs/img/renamer_empty.png "Application with no input")
![RenamerWithInput](./docs/img/renamer_with_input.png "Application with input")

## Renaming Logic
> Work in progress. The logic described below may (and hopefully will) change in the future

Script will always try to rename files to `new-name_i.extension`, with `i` being the next value starting from „1” (may include leading 0s based on user’s choice). The input list of files (read from directory) will always be sorted by file names.

For all examples below, let’s assume that user chose the new name to be `Holidays`.

Eg.
Files will be renamed like so:
```
IMG_123.jpg -> Holidays_1.jpg
IMG_234.jpg -> Holidays_2.jpg
IMG_235.jpg -> Holidays_3.jpg
```

It may however happen that some files already have a name exactly the same as the chosen new name. If they end up being in the correct spot, they will simply remain like they were

Eg.
```
Holidays_1.jpg	->	not renamed
IMG_234.jpg     ->	Holidays_2.jpg
IMG_235.jpg 	->	Holidays_3.jpg
```

Another possible situation is when some files already have a name which script is going to give to another file. In the previous version of the script this resulted in a Critical error of replacing files (essentially removing some). Right now the script will attempt to find the first available file name in such a case.

Eg.
```
Holidays_0.jpg	->  Holidays_2.jpg
Holidays_1.jpg	-> 	not renamed
IMG_123.jpg		->	Holidays_3.jpg
```

For `Holidays_0.jpg` the script will first try to rename it to `Holidays_1.jpg`, but it will fail to do so as `Holidays_1.jpg` already exists (so it would result in replacing and loss of the original `Holidays_1.jpg` file).
Script then tries to find the first available name (still starting from 1) and ends up at `Holidays_2.jpg`.

For `Holidays_1.jpg` the script will first try to rename it to `Holidays_2.jpg`, but will fail to do so as we just created such file. Script will then try to find the first available name (starting from `Holidays_1`) or to leave the current name and arrives at `Holidays_1.jpg`, which means that the file will not be renamed in the end, as this is the current name of the file.


## Changelog

### 2025-01-26
1. Added a confirmation dialog after clicking "Rename files" button to confirm execution

### 2024-12-25
1. Directories are now ignored when both looking for extensions and renaming

### 2024-11-27
1. Added extension choosing (only files with one of the chosen extensions will be renamed). The list of available extensions (checkboxes) is generated automatically for any chosen directory/folder

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
- Have a counter next to each extension to show how many files have that extension
- Add a separate toggle to also rename directories (eg. smth like `isDir` check)

## Known bugs
- CRITICAL Folders / Directories need to be entered into in the selection dialog, not just highighted! If they are only highlighted the parent directory will be chosen!
- Renamed files may have missing numbers in between them, or the same numbers on two or more files if the extensions are different (eg. after running the script you may end up with both `NewName_1.jpg` and `NewName_1.png` files)

## Fixes to do
- Make the extension list "fold" when it get's too wide
- Automatically resize the window back to a smaller side if it got extended by something like a long directory path or file name or a lot of extensions
- Hide the extensions Group Box until a directory is selected
- Ignore extensions like .DS_Store etc.
- Add typing where possible
- Use logger instead of print functions
- Store logs in a file
- Rework renaming logic
