"""Database operations for hospital records."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Entity:
    key: str
    table: str
    id_column: str
    columns: tuple[str, ...]


PATIENT = Entity(
    key="patient",
    table="patient_details",
    id_column="Patient_id",
    columns=("Patient_id", "Name", "Sex", "Age", "Address", "Contact_info"),
)
DOCTOR = Entity(
    key="doctor",
    table="doctor_details",
    id_column="Doctor_id",
    columns=(
        "Doctor_id",
        "Name",
        "Specialisation",
        "Address",
        "Contact_info",
        "Monthly_Salary",
    ),
)
NURSE = Entity(
    key="nurse",
    table="nurse_details",
    id_column="Nurse_id",
    columns=("Nurse_id", "Name", "Address", "Contact_info", "Monthly_Salary"),
)
WORKER = Entity(
    key="worker",
    table="other_workers_details",
    id_column="Worker_id",
    columns=("Worker_id", "Name", "Address", "Contact_info", "Monthly_Salary"),
)


def fetch_all(connection, entity: Entity) -> tuple[tuple[str, ...], list[tuple[Any, ...]]]:
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {entity.table}")
    rows = cursor.fetchall()
    columns = cursor.column_names
    cursor.close()
    return columns, rows


def fetch_one(connection, entity: Entity, record_id: int) -> tuple[Any, ...] | None:
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * FROM {entity.table} WHERE {entity.id_column} = %s",
        (record_id,),
    )
    row = cursor.fetchone()
    cursor.close()
    return row


def insert_record(connection, entity: Entity, values: tuple[Any, ...]) -> None:
    placeholders = ", ".join(["%s"] * len(entity.columns))
    columns = ", ".join(entity.columns)
    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO {entity.table} ({columns}) VALUES ({placeholders})",
        values,
    )
    connection.commit()
    cursor.close()


def update_record(connection, entity: Entity, record_id: int, column: str, value: Any) -> bool:
    if column not in entity.columns or column == entity.id_column:
        raise ValueError(f"Cannot update column: {column}")

    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE {entity.table} SET {column} = %s WHERE {entity.id_column} = %s",
        (value, record_id),
    )
    connection.commit()
    changed = cursor.rowcount > 0
    cursor.close()
    return changed


def delete_record(connection, entity: Entity, record_id: int) -> bool:
    cursor = connection.cursor()
    cursor.execute(
        f"DELETE FROM {entity.table} WHERE {entity.id_column} = %s",
        (record_id,),
    )
    connection.commit()
    deleted = cursor.rowcount > 0
    cursor.close()
    return deleted
