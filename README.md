# Excel Merger

A Django web application for merging multiple Excel files into a single output file, with column selection, fuzzy column matching, and session logging.

## What it does

- Upload a folder of Excel files
- Select a primary file and a sheet
- Choose which columns to keep
- Merge all selected files into an output Excel file
- Columns with minor name differences (e.g. `Nmae` vs `Name`) are matched automatically
- Every merge session is logged in the database

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/SayaDezerm/excel_merger.git
cd <project-folder>
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install django djangorestframework pandas openpyxl
```

### 4. Create superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 7. Run the server

```bash
python manage.py runserver
```
