#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import sqlite3
import unittest
from ind import create_db, add_student, select_all, find_students


class StudTest(unittest.TestCase):
    """
    Тест программы для списка студентов
    """
    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        print("setUpClass")
        print("==========")

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("tearDownClass")

    def setUp(self):
        """Set up for test"""
        print("Set up for [" + self.shortDescription() + "]")
        print("Creating the test DB...")

    def tearDown(self):
        """Tear down for test"""
        print("Tear down for [" + self.shortDescription() + "]")
        print("The test DB has been deleted")

    # //////////////////////

    def test_create_db(self):
        """
        Проверка создания БД.
        """
        database_path = "test.db"
        if Path(database_path).exists():
            Path(database_path).unlink()

        create_db(database_path)
        self.assertTrue(Path(database_path).is_file())
        Path(database_path).unlink()

    def test_add_student(self):
        """
        Проверка добавления записи о товаре.
        """
        database_path = "test.db"
        create_db(database_path)
        add_student(database_path, 'саша', '112', [4,5,4,3,5])
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM students
            """
        )
        row = cursor.fetchone()
        self.assertEqual(row, (1, 'саша', 1, [4,5,4,3,5]))
        conn.close()
        Path(database_path).unlink()

    def test_select_all(self):
        """
        Проверка выбора всего списка
        """
        database_path = "test.db"
        create_db(database_path)
        add_student(database_path, 'саша', '112', [4,5,4,3,5])
        add_student(database_path, 'вова', '145', [5,3,4,3])

        r_output = [
            {'name': 'саша', 'group': '112', 'marks': [4,5,4,3,5]},
            {'name': 'вова', 'group': '145', 'marks': [5,3,4,3]}
        ]
        self.assertEqual(select_all(database_path), r_output)
        Path(database_path).unlink()

    def test_find_students(self):
        """
        Проверка вывода студентов с хорошей успеваемостью
        """
        database_path = "test.db"
        create_db(database_path)
        add_student(database_path, 'миша', '002', [2,2,3,1,4])
        add_student(database_path, 'соня', '454', [5,4,5,4,5])
        r_output = [
            {'name': 'саша', 'group': '112', 'marks': [4,5,4,3,5]},
            {'name': 'соня', 'group': '454', 'marks': [5,4,5,4,5]}

        ]
        self.assertCountEqual(find_students(database_path), r_output)
        Path(database_path).unlink()

    if __name__ == '__main__':
        unittest.main()