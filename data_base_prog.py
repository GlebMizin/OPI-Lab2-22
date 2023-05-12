#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sqlite3
import typing as t
from pathlib import Path


def create_db(database_path: Path) -> None:
    """
    Создать базу данных.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Создать таблицу с информацией об Трансферах.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Transfers (
            Transfer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Transfer_ammount INTEGER
        )
        """
    )

    # Создать таблицу с информацией об аккаунтах получателя и отправителя .
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Accounts (
            Sender_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Sender INTEGER,
            Receiver_id INTEGER,
            Receiver INTEGER,
            FOREIGN KEY(Sender_id) REFERENCES Transfers(Transfer_id)
        )
        """
    )

    conn.close()


def add_account(
        database_path: Path,
        Sender: int,
        Receiver: int,
        Transfer_ammount: int
) -> None:
    """
    Добавить работника в базу данных.
    """

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Получить идентификатор должности в базе данных.
    # Если такой записи нет, то добавить информацию о новой должности.
    cursor.execute(
        """
        INSERT INTO Transfers (Transfer_ammount) VALUES (?)
        """,
        (Transfer_ammount,)
    )
    Sender_id = cursor.lastrowid

    # Добавить информацию о новом работнике.
    cursor.execute(
        """
        INSERT INTO Accounts (Sender, Receiver_id, Receiver)
        VALUES (?, ?, ?)
        """,
        (Sender, Sender_id, Receiver)
    )

    conn.commit()
    conn.close()


def select_all(database_path: Path) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать всех работников.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT Accounts.Sender, Accounts.Receiver, Transfers.Transfer_ammount
        FROM Accounts
        INNER JOIN Transfers ON Accounts.Sender_id = Transfers.Transfer_id
        """
    )
    rows = cursor.fetchall()

    conn.close()
    return [
        {
            "s_b_a": row[0],
            "b_a": row[1],
            "t_a": row[2],
        }
        for row in rows
    ]


def display_accs(accounts: t.List[t.Dict[str, t.Any]]) -> None:
    """
    Отобразить список аккаунтов.
    """

    if accounts:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 2,
            '-' * 25,
            '-' * 25,
            '-' * 10
        )
        print(line)
        print(
            '| {:^2} | {:^25} | {:^25} | {:^10} |'.format(
                "№",
                "Sender bank account",
                "beneficiary account",
                "Amount",
            )
        )
        print(line)
        # Вывести данные о всех сотрудниках.
        for ind, requisite in enumerate(accounts, 1):
            print(
                '| {:^2} | {:^25} | {:^25} | {:^10} |'.format(
                    ind,
                    requisite.get('s_b_a'),
                    requisite.get('b_a'),
                    requisite.get('t_a'),
                )
            )
            print(line)
    else:
        print("Нет введенных банковских счетов.")


def sum_check(
    database_path: Path, Sender: int
) -> t.List[t.Dict[str, t.Any]]:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT SUM(Transfer_ammount) FROM Transfers WHERE Transfer_id 
        IN ( SELECT Sender_id FROM Accounts WHERE Sender = ? )
        """,
        (Sender,)
    )

    sum_result = cursor.fetchone()[0]

    conn.close()

    return sum_result


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "--db",
        action="store",
        required=False,
        default=str(Path.cwd() / "reqs.db"),
        help="The database file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("workers")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new acc"
    )
    add.add_argument(
        "-s",
        "--s_b_a",
        action="store",
        type=int,
        required=True,
        help="Аккаунт отправитель"
    )
    add.add_argument(
        "-r",
        "--b_a",
        action="store",
        type=int,
        help="Аккаунт получатель"
    )
    add.add_argument(
        "-t",
        "--t_a",
        action="store",
        type=int,
        required=True,
        help="Сумма трансфера"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Отобразить все аккаунты"
    )

    select = subparsers.add_parser(
        "check",
        parents=[file_parser],
        help="Проверить"
    )
    select.add_argument(
        "-t",
        "--s_b_a",
        action="store",
        type=int,
        required=True,
        help="Аккаунт для которого необходимо получить общую сумму трансферов"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Получить путь к файлу базы данных.
    db_path = Path(args.db)
    create_db(db_path)

    # Добавить работника.
    if args.command == "add":
        add_account(db_path, args.s_b_a, args.b_a, args.t_a)

    # Отобразить всех работников.
    elif args.command == "display":
        display_accs(select_all(db_path))

    # Выбрать требуемых работников.
    elif args.command == "check":
        sum_check(db_path, args.s_b_a)
        pass


if __name__ == "__main__":
    main()

