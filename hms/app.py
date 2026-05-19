"""Simple command-line hospital management app."""

from mysql.connector import Error
from prettytable import PrettyTable

from hms.db import get_connection


TABLES = {
    "patient": ("patient_details", "Patient_id"),
    "doctor": ("doctor_details", "Doctor_id"),
    "nurse": ("nurse_details", "Nurse_id"),
    "worker": ("other_workers_details", "Worker_id"),
}


def read_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a valid number.")


def confirm(message):
    return input(message).strip().lower() == "y"


def show_menu(title, options):
    print(f"\n{title}")
    print("-" * len(title))
    for number, text in options.items():
        print(f"{number}. {text}")


def show_table(cursor, query, values=None):
    cursor.execute(query, values or ())
    rows = cursor.fetchall()

    table = PrettyTable(cursor.column_names)
    for row in rows:
        table.add_row(row)
    print(table)


def show_all_records(cursor, record_type):
    table_name = TABLES[record_type][0]
    show_table(cursor, f"SELECT * FROM {table_name}")


def find_record(cursor, record_type, record_id):
    table_name, id_column = TABLES[record_type]
    cursor.execute(
        f"SELECT * FROM {table_name} WHERE {id_column} = %s",
        (record_id,),
    )
    return cursor.fetchone()


def add_doctor(cursor, connection):
    doctor_id = read_int("Enter doctor's id: ")
    name = input("Enter doctor's name: ")
    specialisation = input("Enter specialisation: ")
    address = input("Enter address: ")
    contact = input("Enter contact no: ")
    salary = read_int("Enter monthly salary: ")

    cursor.execute(
        """
        INSERT INTO doctor_details
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (doctor_id, name, specialisation, address, contact, salary),
    )
    connection.commit()
    print("Doctor added successfully.")


def add_nurse(cursor, connection):
    nurse_id = read_int("Enter nurse's id: ")
    name = input("Enter nurse's name: ")
    address = input("Enter address: ")
    contact = input("Enter contact no: ")
    salary = read_int("Enter monthly salary: ")

    cursor.execute(
        "INSERT INTO nurse_details VALUES (%s, %s, %s, %s, %s)",
        (nurse_id, name, address, contact, salary),
    )
    connection.commit()
    print("Nurse added successfully.")


def add_worker(cursor, connection):
    worker_id = read_int("Enter worker's id: ")
    name = input("Enter worker's name: ")
    address = input("Enter address: ")
    contact = input("Enter contact no: ")
    salary = read_int("Enter monthly salary: ")

    cursor.execute(
        "INSERT INTO other_workers_details VALUES (%s, %s, %s, %s, %s)",
        (worker_id, name, address, contact, salary),
    )
    connection.commit()
    print("Worker added successfully.")


def add_patient(cursor, connection):
    patient_id = read_int("Enter patient's id: ")
    name = input("Enter patient's name: ")
    sex = input("Enter gender: ")
    age = read_int("Enter age: ")
    address = input("Enter address: ")
    contact = input("Enter contact details: ")

    cursor.execute(
        "INSERT INTO patient_details VALUES (%s, %s, %s, %s, %s, %s)",
        (patient_id, name, sex, age, address, contact),
    )
    connection.commit()
    print("Patient added successfully.")


def choose_staff_type():
    show_menu(
        "Choose Staff Type",
        {
            1: "Doctor",
            2: "Nurse",
            3: "Worker",
            4: "Back",
        },
    )
    choice = read_int("Enter your choice: ")
    return {1: "doctor", 2: "nurse", 3: "worker"}.get(choice)


def choose_record_type():
    show_menu(
        "Choose Record Type",
        {
            1: "Patient",
            2: "Doctor",
            3: "Nurse",
            4: "Worker",
            5: "Back",
        },
    )
    choice = read_int("Enter your choice: ")
    return {1: "patient", 2: "doctor", 3: "nurse", 4: "worker"}.get(choice)


def add_staff(cursor, connection):
    staff_type = choose_staff_type()
    if staff_type == "doctor":
        add_doctor(cursor, connection)
    elif staff_type == "nurse":
        add_nurse(cursor, connection)
    elif staff_type == "worker":
        add_worker(cursor, connection)


def update_staff(cursor, connection):
    staff_type = choose_staff_type()
    if staff_type is None:
        return

    record_id = read_int(f"Enter {staff_type} id: ")
    record = find_record(cursor, staff_type, record_id)
    if record is None:
        print("No record found.")
        return

    print("Record found:")
    print(record)

    show_menu(
        "Update Field",
        {
            1: "Address",
            2: "Contact info",
            3: "Monthly salary",
            4: "Back",
        },
    )
    choice = read_int("Enter your choice: ")
    columns = {1: "Address", 2: "Contact_info", 3: "Monthly_Salary"}
    column = columns.get(choice)
    if column is None:
        return

    value = read_int("Enter new monthly salary: ") if column == "Monthly_Salary" else input("Enter new value: ")
    table_name, id_column = TABLES[staff_type]
    cursor.execute(
        f"UPDATE {table_name} SET {column} = %s WHERE {id_column} = %s",
        (value, record_id),
    )
    connection.commit()
    print("Record updated successfully.")


def delete_staff(cursor, connection):
    staff_type = choose_staff_type()
    if staff_type is None:
        return

    record_id = read_int(f"Enter {staff_type} id: ")
    record = find_record(cursor, staff_type, record_id)
    if record is None:
        print("No record found.")
        return

    print("Record found:")
    print(record)
    if not confirm("Delete this record? (y/n): "):
        print("Delete cancelled.")
        return

    table_name, id_column = TABLES[staff_type]
    cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", (record_id,))
    connection.commit()
    print("Record deleted successfully.")


def administration_menu(cursor, connection):
    while True:
        show_menu(
            "Administration",
            {
                1: "Display records",
                2: "Add staff record",
                3: "Update staff record",
                4: "Delete staff record",
                5: "Back",
            },
        )
        choice = read_int("Enter your choice: ")

        if choice == 1:
            record_type = choose_record_type()
            if record_type:
                show_all_records(cursor, record_type)
        elif choice == 2:
            add_staff(cursor, connection)
        elif choice == 3:
            update_staff(cursor, connection)
        elif choice == 4:
            delete_staff(cursor, connection)
        elif choice == 5:
            break


def patient_menu(cursor, connection):
    while True:
        show_menu(
            "Patient",
            {
                1: "Show patient records",
                2: "Add new patient",
                3: "Discharge patient",
                4: "Back",
            },
        )
        choice = read_int("Enter your choice: ")

        if choice == 1:
            show_all_records(cursor, "patient")
        elif choice == 2:
            add_patient(cursor, connection)
        elif choice == 3:
            discharge_patient(cursor, connection)
        elif choice == 4:
            break


def discharge_patient(cursor, connection):
    patient_id = read_int("Enter patient's id: ")
    record = find_record(cursor, "patient", patient_id)
    if record is None:
        print("No patient found.")
        return

    print("Patient found:")
    print(record)
    if confirm("Has the patient paid all bills? (y/n): "):
        cursor.execute(
            "DELETE FROM patient_details WHERE Patient_id = %s",
            (patient_id,),
        )
        connection.commit()
        print("Patient discharged successfully.")
    else:
        print("Discharge cancelled.")


def run():
    try:
        connection = get_connection()
    except Error as error:
        print(f"MySQL connection failed: {error}")
        return

    cursor = connection.cursor()

    try:
        while True:
            show_menu(
                "City Hospital Main Menu",
                {
                    1: "Administration",
                    2: "Patient details",
                    3: "Sign out",
                },
            )
            choice = read_int("Enter your choice: ")

            if choice == 1:
                administration_menu(cursor, connection)
            elif choice == 2:
                patient_menu(cursor, connection)
            elif choice == 3:
                break
    finally:
        cursor.close()
        connection.close()
        print("Signed out.")
