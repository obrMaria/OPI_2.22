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
        self.db_path = "test.db"
        create_db(self.db_path)

    def tearDown(self):
        """Tear down for test"""
        print("Tear down for [" + self.shortDescription() + "]")
        print("The test DB has been deleted")
        Path(self.db_path).unlink()

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
        add_student(self.db_path, 'саша', '112', '4,5,4,3,5')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM students
            """
        )
        row = cursor.fetchone()
        self.assertEqual(row, (1, 'саша', '112', '4,5,4,3,5'))
        conn.close()

    def test_select_all(self):
        """
        Проверка выбора всего списка
        """
        add_student(self.db_path, 'саша', '112', '4,5,4,3,5')
        add_student(self.db_path, 'вова', '145', '5,5,4,3')
        add_student(self.db_path, 'кристина', '45', '4,1,5,4,2')

        r_output = [
            {'name': 'саша', 'group': '112', 'marks': '4,5,4,3,5'},
            {'name': 'вова', 'group': '145', 'marks': '5,5,4,3'},
            {'name': 'кристина', 'group': '45', 'marks': '4,1,5,4,2'}
        ]
        self.assertEqual(select_all(self.db_path), r_output)

    def test_find_students(self):
        """
        Проверка вывода студентов с хорошей успеваемостью
        """
        add_student(self.db_path, 'саша', '112', '4,5,4,3,5')
        add_student(self.db_path, 'вова', '145', '5,5,4,3')
        add_student(self.db_path, 'кристина', '45', '4,1,5,4,2')
        r_output = [
            {'name': 'саша', 'group': '112', 'marks': '4,5,4,3,5'},
            {'name': 'вова', 'group': '145', 'marks': '5,5,4,3'}
        ]
        self.assertEqual(find_students(self.db_path), r_output)

    if __name__ == '__main__':
        unittest.main()

