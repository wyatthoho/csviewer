# CSViewer

CSViewer is a Python-based tool designed to visualize 
multiple CSV files. It processes and displays data in 
an interactive and user-friendly GUI.


## Installation

To use CSViewer, clone the repository and install the required dependencies:

```bash
git clone https://github.com/wyatthoho/csviewer.git
```

Initialize a virtual environment. 
```bash
cd csviewer
py -m venv env
```

Activate the virtual environment and install required dependencies. 
For PowerShell, follow these steps:
```bash

# HINT: If the current PowerShell execution policy prevents 
#       activating the environment, run the following command
#       to allow script execution:
#
# `Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser`

.\env\Scripts\Activate.ps1
pip install -r .\requirements.txt
```

After installation, deactivate the environment:
```bash
deactivate
```

## Running the Project

To run the project, execute the following:
```bash
.\run_in_venv.ps1
```
