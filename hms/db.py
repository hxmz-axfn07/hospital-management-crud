"""Database setup for City Hospital Management System."""

import getpass
import os

import mysql.connector


DATABASE_NAME = "city_hospital"


def get_connection():
    """Ask for MySQL login, create database/tables, then return connection."""
    username = os.getenv("HMS_DB_USER") or input("Enter your MySQL username: ")
    password = os.getenv("HMS_DB_PASSWORD") or getpass.getpass(
        "Enter your MySQL password: "
    )
    host = os.getenv("HMS_DB_HOST", "localhost")

    connection = mysql.connector.connect(host=host, user=username, password=password)
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    cursor.execute(f"USE {DATABASE_NAME}")
    create_tables(cursor)
    connection.commit()
    return connection


def create_tables(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patient_details (
            Patient_id INT PRIMARY KEY,
            Name VARCHAR(30) NOT NULL,
            Sex VARCHAR(15) NOT NULL,
            Age INT NOT NULL,
            Address VARCHAR(50) NOT NULL,
            Contact_info VARCHAR(20) NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS doctor_details (
            Doctor_id INT PRIMARY KEY,
            Name VARCHAR(30) NOT NULL,
            Specialisation VARCHAR(40) NOT NULL,
            Address VARCHAR(30) NOT NULL,
            Contact_info VARCHAR(20) NOT NULL,
            Monthly_Salary INT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS nurse_details (
            Nurse_id INT PRIMARY KEY,
            Name VARCHAR(30) NOT NULL,
            Address VARCHAR(30) NOT NULL,
            Contact_info VARCHAR(20) NOT NULL,
            Monthly_Salary INT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS other_workers_details (
            Worker_id INT PRIMARY KEY,
            Name VARCHAR(30) NOT NULL,
            Address VARCHAR(30) NOT NULL,
            Contact_info VARCHAR(20) NOT NULL,
            Monthly_Salary INT NOT NULL
        )
        """
    )
