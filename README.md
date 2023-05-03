# goodchain

## Requirement for the application
1. install python 
2. install pip
3. run the following command: `pip3 install -r requirementes.txt`
4. make sure u have the same goodchain database
5. Alter the server.py file:
    - `server_ip ` = ip of your own machine
    - `client_ip ` = ip of the receiving machine


## Run the application
1. navigate to the directory 
2. run the command: `python3 goodchain.py`
**Note** make sure ur first complete point 3 in the application


## LunarVim Basic Commands
This is a list of some basic commands for LunarVim, a powerful and customizable Vim-based IDE.

### Navigation
* Go to end of the file: G
* Go to top of the file: gg
* Go to line number: :<line_number>

### Editing
* Comment code: gcc (in normal mode)
* Select all: ggVG (in normal mode)
* Delete line: dd (in normal mode)
* Undo: u
* Redo: ctrl+r
* Saving and Quitting
* Save file: :w
* Quit: :q
* Force quit (discard changes): :q!

### Plugins
LunarVim comes with many plugins pre-installed. Here are a few basic commands for some of them:

### Telescope
Find files: :Telescope find_files
`Search for string in files: :Telescope live_grep`

### NERDTree
* Open NERDTree: :NERDTreeToggle

### Git
* Git add current file: :Git add %
* Git commit: :Git commit

### Customization
LunarVim is highly customizable. You can add your own keybindings and configure plugins in the config.lua file located in the ~/.config/lvim directory.

For more information on customization, please refer to the LunarVim documentation.j

