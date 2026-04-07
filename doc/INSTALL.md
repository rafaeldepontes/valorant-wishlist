# Installation Guide

## Requirements

-   Python 3.10+ installed
-   `pip` available in your terminal

------------------------------------------------------------------------

## 1. Set up the virtual environment

Create a virtual environment in the project root:

``` bash
py -m venv .venv
```

Activate it:

### Windows (Command Prompt)

``` bat
.venv\Scripts\activate.bat
```

### Windows (PowerShell)

``` powershell
.venv\Scripts\Activate.ps1
```

### macOS / Linux

``` bash
source .venv/bin/activate
```

Install the dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 2. Run the application

Start the development server with:

``` bash
uvicorn app.main:app --reload
```

If `uvicorn` is not available in your shell, use:

``` bash
python -m uvicorn app.main:app --reload
```

------------------------------------------------------------------------

## 3. Deactivate the virtual environment

When you are done, deactivate it with:

``` bash
deactivate
```