# Start Guide

## 1. Setting up:

Run this in your terminal:

```bash
$ py -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

## 2. Running:

To run the application, just copy and paste it:

```bash
# Not running the "venv"
.\.venv\Scripts\uvicorn main:app --reload

# "venv" running:
uvicorn main:app --reload
```
