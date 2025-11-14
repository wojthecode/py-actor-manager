import sqlite3
from sqlite3 import Cursor
from app.models import Actor


class ActorManager:
    def __init__(self, db_name: str, table_name: str) -> None:
        self.db_name = db_name
        self.table_name = table_name

    def create(self, first_name: str, last_name: str) -> None:
        # Create data base connection
        with sqlite3.connect(self.db_name) as data_base:
            query = data_base.cursor()
            table_exist = self.table_exist(query, self.table_name)
            # Create table if no exist
            if not table_exist:
                query.execute(
                    f"""
                    CREATE TABLE {self.table_name} (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, first_name VARCHAR(100), last_name VARCHAR(100))
                    """
                )
            query.execute(
                f"""
                INSERT INTO {self.table_name} (first_name, last_name) 
                VALUES ('{first_name}', '{last_name}')
                """
            )

    def all(self) -> list:
        # Create data base connection
        with sqlite3.connect(self.db_name) as data_base:
            query = data_base.cursor()
            table_exist = self.table_exist(query, self.table_name)
            if not table_exist:
                return []
            # Return list of Actor class from table
            actors = query.execute(
                f"""
                SELECT * FROM {self.table_name}
                """
            ).fetchall()
            return [Actor(actor[0], actor[1], actor[2]) for actor in actors]

    def update(self, pk: int, new_first_name: str, new_last_name: str) -> None:
        # Create data base connection
        with sqlite3.connect(self.db_name) as data_base:
            query = data_base.cursor()
            table_exist = self.table_exist(query, self.table_name)
            if table_exist:
                record_exist = self.record_exist(query, self.table_name, pk)
                if record_exist:
                    # Update record
                    query.execute(
                        f"""
                        UPDATE {self.table_name}
                        SET first_name = '{new_first_name}', last_name = '{new_last_name}'
                        WHERE id={pk}
                        """
                    )

    def delete(self, pk: int) -> None:
        # Create data base connection
        with sqlite3.connect(self.db_name) as data_base:
            query = data_base.cursor()
            table_exist = self.table_exist(query, self.table_name)
            if table_exist:
                record_exist = self.record_exist(query, self.table_name, pk)
                if record_exist:
                    # Delete record
                    query.execute(
                        f"""
                        DELETE FROM {self.table_name}
                        WHERE id={pk}
                        """
                    )

    @staticmethod
    def table_exist(query: Cursor, table_name: str) -> bool:
        # Check if table exists
        table_exist = query.execute(
            f"""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' 
            AND name='{table_name}'
            """
        ).fetchall()
        if not table_exist:
            return False
        return True

    @staticmethod
    def record_exist(query: Cursor, table_name: str, pk: int) -> bool:
        # Check if record exists
        record_exist = query.execute(
            f"""
            SELECT * FROM {table_name}
            WHERE id={pk}
            """
        )
        if not record_exist:
            return False
        return True
