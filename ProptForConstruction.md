
### Instruction:

This script opens a window with the following UI components: 
- a button to add folders and a list of folders displayed under the button to display the selected folders by the user
- a Button to add files and the list of files displayed under the button to display the selected files by the user
- A text box for the user to insert a custom prompt
- A button to add A path for the extracted markdown file
- It takes under the button displaying the destination folder

It reads all the the selected and the files from the folder that cotain code and based on the file extension it will wrap the file content into a markdown code block. 
Before each markdown codeblock it will write as a 4th heading the relative path of each file
For example if the termination is .py it will wrapt the code in a tripple kwote with python, same with kotlin and xml files.
It will then write the content of all the files into a single markdown file and copy it to the clipboadrd and to the selected detination folder that defaults as the desktop for windows and linux users.
To achieve this, you can use Python along with the `tkinter` library for the file browser and the `os` and `pathlib` libraries to handle file operations.
