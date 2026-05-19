"""MySQL connection and schema management."""

from mysql.connector import connect

from .config import DatabaseConfig


TABLE_DEFINITIONS = (
    """
    CREATE TABLE IF NOT EXISTS patient_details (
        Patient_id INT PRIMARY KEY,
        Name VARCHAR(30) NOT NULL,
        Sex VARCHAR(15) NOT NULL,
        Age INT NOT NULL,
        Address VARCHAR(50) NOT NULL,
        Contact_info VARCHAR(20) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS doctor_details (
        Doctor_id INT PRIMARY KEY,
        Name VARCHAR(30) NOT NULL,
        Specialisation VARCHAR(40) NOT NULL,
        Address VARCHAR(30) NOT NULL,
        Contact_info VARCHAR(20) NOT NULL,
        Monthly_Salary INT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS nurse_details (
        Nurse_id INT PRIMARY KEY,
        Name VARCHAR(30) NOT NULL,
        Address VARCHAR(30) NOT NULL,
        Contact_info VARCHAR(20) NOT NULL,
        Monthly_Salary INT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS other_workers_details (
        Worker_id INT PRIMARY KEY,
        Name VARCHAR(30) NOT NULL,
        Address VARCHAR(30) NOT NULL,
        Contact_info VARCHAR(20) NOT NULL,
        Monthly_Salary INT NOT NULL
    )
    """,
)


def create_connection(config: DatabaseConfig):
    """Create database if needed, then return a connection using it."""
    server_connection = connect(
        host=config.host,
        user=config.user,
        password=config.password,
    )
    cursor = server_connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.database}")
    cursor.close()
    server_connection.close()

    connection = connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database,
    )
    initialize_schema(connection)
    return connection


def initialize_schema(connection) -> None:
    cursor = connection.cursor()
    for statement in TABLE_DEFINITIONS:
        cursor.execute(statement)
    connection.commit()
    cursor.close()
