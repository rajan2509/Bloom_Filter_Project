
import sqlite3
from pathlib import Path


# Project paths
PROJECT_FOLDER = Path(__file__).resolve().parent.parent

DATABASE_FOLDER = PROJECT_FOLDER / "data"
DATABASE_FILE = DATABASE_FOLDER / "bloom_filter.db"

SCHEMA_FILE = PROJECT_FOLDER / "sql" / "schema.sql"


def create_database():

    DATABASE_FOLDER.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)

    with open(SCHEMA_FILE, "r") as file:
        schema = file.read()

    connection.executescript(schema)

    connection.commit()

    print("Database and table created successfully!")

    return connection


def insert_sample_data(connection):

    cursor = connection.cursor()

    # Generate sample usernames
    usernames = [
        (f"registered_user_{i}",)
        for i in range(1000)
    ]

    # Generate sample URLs
    urls = [
        (f"https://example{i}.com",)
        for i in range(1000)
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO checked_items
        (item_type, item_value)
        VALUES ('username', ?)
        """,
        usernames
    )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO checked_items
        (item_type, item_value)
        VALUES ('url', ?)
        """,
        urls
    )

    connection.commit()

    print("Sample records inserted successfully!")


def display_record_counts(connection):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT item_type, COUNT(*)
        FROM checked_items
        GROUP BY item_type
        """
    )

    print("\nDATABASE RECORD SUMMARY")
    print("-----------------------")

    for item_type, count in cursor.fetchall():
        print(f"{item_type}: {count}")


def main():

    connection = create_database()

    insert_sample_data(connection)

    display_record_counts(connection)

    connection.close()

    print("\nDatabase setup completed!")


if __name__ == "__main__":
    main()
