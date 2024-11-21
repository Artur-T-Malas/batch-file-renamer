![RenamerEmpty](./docs/img/renamer_empty.png "Application with no input")
![RenamerWithInput](./docs/img/renamer_with_input.png "Application with input")

### Functional Requirements
User Story: As a User, I want to choose files from a dialog window
1. Get paths to files and their current names from a dialog window
   - Use PyQt GUI elements for desktop app

User Story: As a User, I want to set the new name for the file batch
1. Get the desired name from an input field from the user
   - Use PyQt
2. Change the names of all the files in the batch

Engineer Story: As an Engineer I want to see unit tests
1. Implement unit tests

## Changelog
### 2024-11-21
1. Allow user to define the number of leading 0s (padding) in the file numeration
2. By default apply the padding automatically based on the number of files in the choosen directory

## Features to add
- Filename input validation (REGEX) (eg. no "/" and "\\")
- Be able to select specific files to renames (instead of whole directories) - could be with a switch (radio button) to let user decide whether they want whole directory or just some files

## Fixes to do
- Add typing where possible
- Use logger instead of print functions
- Store logs in a file
