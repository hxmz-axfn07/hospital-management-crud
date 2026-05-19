# City Hospital Management System

Simple Python + MySQL command-line CRUD project for hospital records.

## What It Can Do

- Add, show, update, and delete doctor records.
- Add, show, update, and delete nurse records.
- Add, show, update, and delete worker records.
- Add, show, and discharge patient records.
- Create the MySQL database and tables automatically.

## Folder Structure

```text
hms_crud/
├── hms/
│   ├── __init__.py
│   ├── __main__.py
│   ├── app.py
│   └── db.py
├── hms_complete_final.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3.10 or newer
- MySQL Server
- Packages from `requirements.txt`

## Setup

Create virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Run app:

```bash
python -m hms
```

Old filename also works:

```bash
python hms_complete_final.py
```

## Database Login

App asks for MySQL username and password when it starts.

You can also set these environment variables:

```bash
set HMS_DB_HOST=localhost
set HMS_DB_USER=root
set HMS_DB_PASSWORD=your_password
```

## Push To GitHub

Create empty GitHub repo first, then run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```
