#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import argparse
import sqlite3
import typing as t
from pathlib import Path


def display_students(students: t.List[t.Dict[str, t.Any]]) -> None:
    """
    Отобразить список студентов.
    """
    # Проверить, что список студентов не пуст.
    if students:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Ф.И.О.",
                "Группа",
                "Оценки"
            )
        )
        print(line)
        # Вывести данные о всех студентах.
        for idx, student in enumerate(students, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                    ','.join(map(str, student['marks']))
                )
            )
        print(line)
    else:
        print("список студентов пуст")

def create_db(database_path: Path) -> None:
    """
    Создать базу данных.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    # Создать таблицу с информацией о группах.
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS groupss (
        group_id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_num TEXT NOT NULL
        )
        """
    )
    # Создать таблицу с информацией о студентах.
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        group_id INTEGER NOT NULL,
        student_marks LIST NOT NULL,
        FOREIGN KEY(group_id) REFERENCES groupss(group_id)
        )
        """
    )
    conn.close()

def add_student(
        database_path: Path,
        name: str,
        group: str,
        marks: list
) -> None:
    """
    Добавить данные о студенте.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    # Получить идентификатор группы в базе данных.
    # Если такой записи нет, то добавить информацию о новой группе.
    cursor.execute(
        """
        SELECT group_id FROM groupss WHERE group_num = ?
        """,
        (group,)
    )
    row = cursor.fetchone()
    if row is None:
        cursor.execute(
            """
            INSERT INTO groupss (group_num) VALUES (?)
            """,
            (group,)
        )
        group_id = cursor.lastrowid
    else:
        group_id = row[0]
    # Добавить информацию о новом студенте.
    cursor.execute(
        """
        INSERT INTO students (student_name, group_id, student_marks)
        VALUES (?, ?, ?)
        """,
        (name, group_id, marks)
    )
    conn.commit()
    conn.close()


def select_all(database_path: Path) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать всех студентов.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT students.student_name, groupss.group_num, students.student_marks
        FROM students
        INNER JOIN groupss ON groupss.group_id = students.group_id
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "name": row[0],
            "group": row[1],
            "marks": row[2],
        }
        for row in rows
    ]


def find_students(
        database_path: Path
) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать студентов со ср ариф. успеваемости >4.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT students.student_name, groupss.group_num, students.student_marks
        FROM students
        INNER JOIN groupss ON groupss.group_id = students.group_id
        GROUP BY students.student_name, groupss.group_num
        HAVING AVG(students.student_marks) >= 4.0
        """

    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "name": row[0],
            "group": row[1],
            "marks": row[2],
        }
        for row in rows
    ]


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "--db",
        action="store",
        required=False,
        default=str(Path.home() / "students.db"),
        help="The database file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("students")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")
    # Создать субпарсер для добавления работника.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new student"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The student's name"
    )

    add.add_argument(
        "-g",
        "--group",
        action="store",
        help="The student's group"
    )

    add.add_argument(
        "-m",
        "--marks",
        action="store",
        required=True,
        help="The student's marks"
    )

    # Создать субпарсер для отображения всех студентов.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all students"
    )

    # Создать субпарсер для поиска студентов.
    find = subparsers.add_parser(
        "find",
        parents=[file_parser],
        help="find the students"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)
    # Получить путь к файлу базы данных.
    db_path = Path(args.db)
    create_db(db_path)
    # Добавить студента.
    if args.command == "add":
        add_student(db_path, args.name, args.group, args.marks)
    # Отобразить всех студентов.
    elif args.command == "display":
        display_students(select_all(db_path))
    # Выбрать требуемых студентов.
    elif args.command == "find":
        display_students(find_students(db_path))
        pass


if __name__ == '__main__':
    main()