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

## Features to add
- Filename input validation (REGEX) (eg. no "/" and "\\")
- Have a predefined (user input) number of 0s before the number (to avoid sorting having 1, 10, 11, 3 etc.)

## Fixes to do
- Add typing where possible
- Use logger instead of print functions
- Store logs in a file
