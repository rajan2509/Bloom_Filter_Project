
import sqlite3
from pathlib import Path


# Project paths
PROJECT_FOLDER = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_FOLDER / "data" / "bloom_filter.db"
QUERY_FILE = PROJECT_FOLDER / "sql" / "queries.sql"


def run_queries():

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    with open(QUERY_FILE, "r") as file:
        sql_content = file.read()

    # Split the file into individual SQL queries
    queries = [
        query.strip()
        for query in sql_content.split(";")
        if query.strip()
    ]

    print("BLOOM FILTER DATABASE - SQL ANALYSIS")
    print("=" * 55)

    for number, query in enumerate(queries, start=1):

        print(f"\nQUERY {number}")
        print("-" * 55)

        cursor.execute(query)

        rows = cursor.fetchall()

        if cursor.description:

            columns = [
                description[0]
                for description in cursor.description
            ]

            print("Columns:", columns)
            print("Total rows returned:", len(rows))

            # Display only the first 5 rows
            for row in rows[:5]:
                print(row)

            if len(rows) > 5:
                print("...more records not displayed")

        else:
            print("Query executed successfully.")

    connection.close()

    print("\nAll SQL queries executed successfully!")


if __name__ == "__main__":
    run_queries()
