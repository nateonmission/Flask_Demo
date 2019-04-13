from flask import Flask, render_template, redirect, url_for, g, flash
import sqlite3
from sqlite3 import Error


def db_create(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        result = "success"
    except Error as e:
        result = e
    finally:
        conn.close()
        return result
