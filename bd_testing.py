#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import unittest
from data_base_prog import Path, create_db, add_account, sum_check


class TestCreateDB(unittest.TestCase):

    def setUp(self):
        self.database_path = Path('test.db')

    def test_create_db(self):
        create_db(self.database_path)
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Transfers'")
        result = cursor.fetchone()
        self.assertEqual(result, ('Transfers',))
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Accounts'")
        result = cursor.fetchone()
        self.assertEqual(result, ('Accounts',))
        conn.close()

    def tearDown(self):
        self.database_path.unlink()

    def setUp(self):
        self.database_path = Path('test.db')
        create_db(self.database_path)

    def test_add_account(self):
        add_account(self.database_path, Sender=1, Receiver=2, Transfer_ammount=100)
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Accounts")
        result = cursor.fetchall()
        conn.close()

        # Проверяем ID, отправителя и получателя в первой бд
        self.assertEqual(result[0][1], 1)
        self.assertEqual(result[0][2], 1)
        self.assertEqual(result[0][3], 2)

        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Transfers")
        result = cursor.fetchall()
        conn.close()

        # Проверяем сумму трансфера
        self.assertEqual(result[0][1], 100)

    def tearDown(self):
        self.database_path.unlink()

    def setUp(self):
        self.database_path = Path('test.db')
        create_db(self.database_path)

    def test_sum_check(self):
        add_account(self.database_path, Sender=1, Receiver=2, Transfer_ammount=100)
        add_account(self.database_path, Sender=1, Receiver=2, Transfer_ammount=50)
        result = sum_check(self.database_path, Sender=1)
        self.assertTrue(result)
        self.assertEqual(result, 150)

    def tearDown(self):
        self.database_path.unlink()