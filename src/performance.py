
import sqlite3
import time
import csv
import statistics
from pathlib import Path

from bloom_filter import BloomFilter


# Project paths
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATABASE_FILE = PROJECT_FOLDER / "data" / "bloom_filter.db"
OUTPUT_FILE = PROJECT_FOLDER / "data" / "performance_results.csv"

# Experiment settings
NUMBER_OF_ROUNDS = 5
BLOOM_SIZE = 16000
HASH_COUNT = 6


def load_database_records(connection):

    cursor = connection.cursor()

    cursor.execute(
        "SELECT item_type, item_value FROM checked_items"
    )

    return cursor.fetchall()


def create_test_queries(records):

    # Existing database records
    existing_queries = [
        (item_type, item_value)
        for item_type, item_value in records
    ]

    # Generate equally many usernames and URLs that do not exist
    unknown_queries = []

    for i in range(len(records)):

        if i % 2 == 0:
            unknown_queries.append(
                ("username", f"unknown_user_{i}")
            )
        else:
            unknown_queries.append(
                ("url", f"https://unknown{i}.example")
            )

    return existing_queries + unknown_queries


def create_bloom_filter(records):

    bloom = BloomFilter(
        size=BLOOM_SIZE,
        hash_count=HASH_COUNT
    )

    for item_type, item_value in records:
        bloom.add(f"{item_type}:{item_value}")

    return bloom


def create_python_set(records):

    return {
        f"{item_type}:{item_value}"
        for item_type, item_value in records
    }


def bloom_sqlite_lookup(bloom, cursor, queries):

    found = 0
    database_lookups = 0

    for item_type, item_value in queries:

        key = f"{item_type}:{item_value}"

        if bloom.might_contain(key):

            database_lookups += 1

            cursor.execute(
                """
                SELECT 1
                FROM checked_items
                WHERE item_type = ?
                AND item_value = ?
                LIMIT 1
                """,
                (item_type, item_value)
            )

            if cursor.fetchone():
                found += 1

    return found, database_lookups


def python_set_lookup(python_set, queries):

    found = 0

    for item_type, item_value in queries:

        key = f"{item_type}:{item_value}"

        if key in python_set:
            found += 1

    return found


def sqlite_direct_lookup(cursor, queries):

    found = 0

    for item_type, item_value in queries:

        cursor.execute(
            """
            SELECT 1
            FROM checked_items
            WHERE item_type = ?
            AND item_value = ?
            LIMIT 1
            """,
            (item_type, item_value)
        )

        if cursor.fetchone():
            found += 1

    return found


def measure_time(function):

    timings = []
    result = None

    # Repeat each method to reduce timing noise
    for _ in range(NUMBER_OF_ROUNDS):

        start = time.perf_counter()

        result = function()

        end = time.perf_counter()

        timings.append(end - start)

    return statistics.median(timings), result


def main():

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    print("BLOOM FILTER PERFORMANCE COMPARISON")
    print("=" * 55)

    records = load_database_records(connection)
    queries = create_test_queries(records)

    print("Database records:", len(records))
    print("Total test queries:", len(queries))
    print("Existing queries:", len(records))
    print("Unseen queries:", len(records))

    # Prepare data structures before measuring lookup time
    bloom = create_bloom_filter(records)
    python_set = create_python_set(records)

    print("\nMeasuring lookup performance...")

    bloom_time, bloom_result = measure_time(
        lambda: bloom_sqlite_lookup(
            bloom, cursor, queries
        )
    )

    set_time, set_result = measure_time(
        lambda: python_set_lookup(
            python_set, queries
        )
    )

    sqlite_time, sqlite_result = measure_time(
        lambda: sqlite_direct_lookup(
            cursor, queries
        )
    )

    bloom_found, database_lookups = bloom_result

    # Check that all methods return the same answer
    if not (
        bloom_found == set_result == sqlite_result
    ):
        raise RuntimeError(
            "The lookup methods returned different results!"
        )

    results = [
        {
            "method": "Bloom Filter + SQLite",
            "median_time_seconds": bloom_time,
            "found_records": bloom_found,
            "total_queries": len(queries),
            "database_lookups": database_lookups
        },
        {
            "method": "Python Set",
            "median_time_seconds": set_time,
            "found_records": set_result,
            "total_queries": len(queries),
            "database_lookups": 0
        },
        {
            "method": "SQLite Direct Lookup",
            "median_time_seconds": sqlite_time,
            "found_records": sqlite_result,
            "total_queries": len(queries),
            "database_lookups": len(queries)
        }
    ]

    print("\nPERFORMANCE RESULTS")
    print("-" * 55)

    for result in results:

        print("\nMethod:", result["method"])

        print(
            "Median time:",
            round(result["median_time_seconds"], 6),
            "seconds"
        )

        print(
            "Records found:",
            result["found_records"]
        )

        print(
            "Database lookups:",
            result["database_lookups"]
        )

    # Save performance results
    with open(OUTPUT_FILE, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()
        writer.writerows(results)

    print("\nAll methods returned the same results.")
    print("Performance results saved to:", OUTPUT_FILE)

    connection.close()


if __name__ == "__main__":
    main()
