# City Hospital Management System

A command-line CRUD application for managing hospital patients and staff records with MySQL.

## Features

- Create the `city_hospital` database and required tables automatically.
- Manage patient, doctor, nurse, and worker records.
- Add, display, update, delete, and discharge records.
- Display tabular output with PrettyTable.
- Use parameterized SQL queries for safer database operations.

## Project Structure

```text
hms_crud/
├── hms/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   ├── database.py
│   └── repository.py
├── hms_complete_final.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3.10+
- MySQL Server running locally or remotely
- Python packages listed in `requirements.txt`

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Make sure MySQL Server is running.

4. Run the application:

   ```bash
   python -m hms
   ```

   You can also use the legacy launcher:

   ```bash
   python hms_complete_final.py
   ```

## Optional Environment Variables

Set these to skip interactive database prompts:

```bash
set HMS_DB_HOST=localhost
set HMS_DB_USER=root
set HMS_DB_PASSWORD=your_password
set HMS_DB_NAME=city_hospital
```

## GitHub Push

Initialize a git repo and push:

```bash
git init
git add .
git commit -m "Initial hospital management system"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## Notes

- Keep real database passwords out of GitHub.
- The app creates tables automatically, but it does not seed sample data.
- Delete/discharge actions ask for confirmation before removing records.
