"""Command-line interface for City Hospital Management System."""

from collections.abc import Callable
from typing import Any

from mysql.connector import Error
from prettytable import PrettyTable

from .config import load_config
from .database import create_connection
from .repository import (
    DOCTOR,
    NURSE,
    PATIENT,
    WORKER,
    Entity,
    delete_record,
    fetch_all,
    fetch_one,
    insert_record,
    update_record,
)


ADMIN_ENTITIES = {
    1: ("Doctor", DOCTOR),
    2: ("Nurse", NURSE),
    3: ("Worker", WORKER),
}

DISPLAY_ENTITIES = {
    1: ("Patient", PATIENT),
    2: ("Doctor", DOCTOR),
    3: ("Nurse", NURSE),
    4: ("Worker", WORKER),
}


def read_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Enter a valid number.")


def confirm(prompt: str) -> bool:
    return input(prompt).strip().lower() == "y"


def print_menu(title: str, options: dict[int, str]) -> None:
    print(f"\n{'=' * len(title)}\n{title}\n{'=' * len(title)}")
    for key, label in options.items():
        print(f"{key}. {label}")


def print_table(columns: tuple[str, ...], rows: list[tuple[Any, ...]]) -> None:
    table = PrettyTable(columns)
    for row in rows:
        table.add_row(row)
    print(table)


def show_records(connection, entity: Entity) -> None:
    columns, rows = fetch_all(connection, entity)
    print_table(columns, rows)


def read_doctor() -> tuple[Any, ...]:
    return (
        read_int("Enter doctor's id: "),
        input("Enter doctor's name: ").strip(),
        input("Enter specialisation: ").strip(),
        input("Enter address: ").strip(),
        input("Enter contact no: ").strip(),
        read_int("Enter monthly salary: "),
    )


def read_nurse() -> tuple[Any, ...]:
    return (
        read_int("Enter nurse's id: "),
        input("Enter nurse's name: ").strip(),
        input("Enter address: ").strip(),
        input("Enter contact no: ").strip(),
        read_int("Enter monthly salary: "),
    )


def read_worker() -> tuple[Any, ...]:
    return (
        read_int("Enter worker's id: "),
        input("Enter worker's name: ").strip(),
        input("Enter address: ").strip(),
        input("Enter contact no: ").strip(),
        read_int("Enter monthly salary: "),
    )


def read_patient() -> tuple[Any, ...]:
    return (
        read_int("Enter patient's id: "),
        input("Enter patient's name: ").strip(),
        input("Enter gender: ").strip(),
        read_int("Enter age: "),
        input("Enter address: ").strip(),
        input("Enter contact details: ").strip(),
    )


READERS: dict[str, Callable[[], tuple[Any, ...]]] = {
    "doctor": read_doctor,
    "nurse": read_nurse,
    "worker": read_worker,
    "patient": read_patient,
}


def add_record(connection, entity: Entity) -> None:
    insert_record(connection, entity, READERS[entity.key]())
    print("Record added successfully.")


def update_menu(connection, entity: Entity) -> None:
    choices = {
        1: ("Address", "address"),
        2: ("Contact_info", "contact info"),
        3: ("Monthly_Salary", "monthly salary"),
    }
    print_menu("What do you want to update?", {key: label for key, (_, label) in choices.items()})
    choice = read_int("Enter your choice: ")
    selected = choices.get(choice)
    if not selected:
        return

    column, label = selected
    record_id = read_int(f"Enter {entity.key} id: ")
    row = fetch_one(connection, entity, record_id)
    if row is None:
        print("No record found.")
        return

    print("Record found:")
    print(row)
    if not confirm(f"Update this {label}? (y/n): "):
        print("Update cancelled.")
        return

    value = read_int("Enter new monthly salary: ") if column == "Monthly_Salary" else input(f"Enter new {label}: ").strip()
    if update_record(connection, entity, record_id, column, value):
        print("Record updated successfully.")
    else:
        print("No record changed.")


def delete_menu(connection, entity: Entity) -> None:
    record_id = read_int(f"Enter {entity.key} id: ")
    row = fetch_one(connection, entity, record_id)
    if row is None:
        print("No record found.")
        return

    print("Record found:")
    print(row)
    if confirm("Delete this record? (y/n): "):
        delete_record(connection, entity, record_id)
        print("Record deleted successfully.")
    else:
        print("Delete cancelled.")


def administration_menu(connection) -> bool:
    print_menu(
        "Administration",
        {
            1: "Display records",
            2: "Add staff record",
            3: "Update staff record",
            4: "Delete staff record",
            5: "Sign out",
            6: "Return to main menu",
        },
    )
    choice = read_int("Enter your choice: ")

    if choice == 1:
        print_menu(
            "Display Records",
            {key: f"{name} records" for key, (name, _) in DISPLAY_ENTITIES.items()},
        )
        entity_choice = read_int("Enter your choice: ")
        selected = DISPLAY_ENTITIES.get(entity_choice)
        if selected:
            show_records(connection, selected[1])
    elif choice in {2, 3, 4}:
        action = {2: "Add", 3: "Update", 4: "Delete"}[choice]
        print_menu(
            f"{action} Staff Record",
            {key: f"{name} records" for key, (name, _) in ADMIN_ENTITIES.items()},
        )
        selected = ADMIN_ENTITIES.get(read_int("Enter your choice: "))
        if selected and choice == 2:
            add_record(connection, selected[1])
        elif selected and choice == 3:
            update_menu(connection, selected[1])
        elif selected and choice == 4:
            delete_menu(connection, selected[1])
    elif choice == 5:
        return False

    return True


def patient_menu(connection) -> bool:
    print_menu(
        "Patient",
        {
            1: "Show patient records",
            2: "Add new patient",
            3: "Discharge patient",
            4: "Return to main menu",
        },
    )
    choice = read_int("Enter your choice: ")

    if choice == 1:
        show_records(connection, PATIENT)
    elif choice == 2:
        add_record(connection, PATIENT)
        show_records(connection, PATIENT)
    elif choice == 3:
        record_id = read_int("Enter patient's id: ")
        row = fetch_one(connection, PATIENT, record_id)
        if row is None:
            print("No patient found.")
            return True

        print("Patient found:")
        print(row)
        if confirm("Has the patient paid all bills? (y/n): "):
            delete_record(connection, PATIENT, record_id)
            print("Patient discharged successfully.")
        else:
            print("Discharge cancelled.")

    return True


def run() -> None:
    try:
        connection = create_connection(load_config())
    except Error as exc:
        print(f"Could not connect to MySQL: {exc}")
        return

    try:
        active = True
        while active:
            print_menu(
                "City Hospital Main Menu",
                {
                    1: "Administration",
                    2: "Patient details",
                    3: "Sign out",
                },
            )
            choice = read_int("Enter your choice: ")
            if choice == 1:
                active = administration_menu(connection)
            elif choice == 2:
                active = patient_menu(connection)
            elif choice == 3:
                active = False
    finally:
        connection.close()
        print("Signed out.")
