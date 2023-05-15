import sqlite3
import pytest
import os
import sys
sys.path.append('./')
from Ind.data_base_prog import Path, create_db, add_account, sum_check


def test_create_db():
    database_path = Path('test.db')
    create_db(database_path)
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Transfers'")
    result = cursor.fetchone()
    assert result == ('Transfers',)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Accounts'")
    result = cursor.fetchone()
    assert result == ('Accounts',)
    conn.close()
    os.remove(database_path)


def test_add_account():
    database_path = Path('test.db')
    create_db(database_path)
    add_account(database_path, Sender=1, Receiver=2, Transfer_ammount=100)
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Accounts")
    result = cursor.fetchall()
    conn.close()

    # Проверяем ID, отправителя и получателя в первой бд
    assert result[0][1] == 1
    assert result[0][2] == 1
    assert result[0][3] == 2

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transfers")
    result = cursor.fetchall()
    conn.close()

    # Проверяем сумму трансфера
    assert result[0][1] == 100
    os.remove(database_path)


def test_sum_check():
    database_path = Path('test.db')
    create_db(database_path)
    add_account(database_path, Sender=1, Receiver=2, Transfer_ammount=100)
    add_account(database_path, Sender=1, Receiver=2, Transfer_ammount=50)
    result = sum_check(database_path, Sender=1)
    assert result == 150
    os.remove(database_path)
