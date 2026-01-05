# NeuroChair Cloud - Windows Setup Guide

Follow these steps to set up and run the NeuroChair Dashboard on a Windows machine.

## Prerequisites

1.  **Install Python:**
    *   Download and install Python 3.11 or later from [python.org](https://www.python.org/downloads/windows/).
    *   **Important:** Check the box **"Add Python to PATH"** during installation.

2.  **Install Git (Optional):**
    *   If you plan to clone the repository, install Git from [git-scm.com](https://git-scm.com/download/win).

## Setup Instructions

### 1. Get the Code
Open Command Prompt (cmd) or PowerShell and clone the repository:
```powershell
git clone https://github.com/dilmithp/neuroChair.git
cd neuroChair
git checkout login-page
```
*(Or simply download and extract the ZIP file)*

### 2. Create a Virtual Environment
It is recommended to use a logical virtual environment to manage dependencies.
```powershell
python -m venv venv
```

### 3. Activate the Virtual Environment
*   **Command Prompt:**
    ```cmd
    venv\Scripts\activate.bat
    ```
*   **PowerShell:**
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
    *(If you get a permission error in PowerShell, run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` first)*

### 4. Install Dependencies
Install the required libraries from `requirements.txt`:
```powershell
pip install -r dashboard/requirements.txt
```

## Running the Application

### Option 1: Run Locally (Python)
Ensure your virtual environment is activated, then run:
```powershell
python dashboard/app.py
```
*   Open your browser and navigate to: [http://127.0.0.1:8050](http://127.0.0.1:8050)
*   **Login:** `U01` / `1234`

### Option 2: Run with Docker Desktop (If installed)
1.  Install Docker Desktop for Windows.
2.  Run the following command in the project root:
    ```powershell
    docker-compose up -d --build dashboard
    ```

## Troubleshooting

*   **"Python not found":** Ensure Python is added to your system PATH.
*   **"Scripts is disabled":** Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell.
*   **"Module not found":** Make sure you activated the venv before running `pip install` or `python app.py`.
