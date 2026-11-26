
import sqlite3
from pathlib import Path

from bloom_filter import BloomFilter


# Project paths
PROJECT_FOLDER = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_FOLDER / "data" / "bloom_filter.db"


def load_bloom_filter(connection):

    # 16,000 bits and 6 hash functions
    bloom = BloomFilter(
        size=16000,
        hash_count=6
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT item_type, item_value
        FROM checked_items
        """
    )

    records = cursor.fetchall()

    # Insert database records into Bloom Filter
    for item_type, item_value in records:

        unique_item = f"{item_type}:{item_value}"

        bloom.add(unique_item)

    print("Bloom Filter loaded successfully!")
    print("Total records inserted:", len(records))

    return bloom


def check_item(bloom, connection, item_type, item_value):

    unique_item = f"{item_type}:{item_value}"

    # First check the Bloom Filter
    if not bloom.might_contain(unique_item):

        print(f"\n{item_value}")
        print("Bloom Filter: Definitely absent")
        print("Database lookup: Skipped")
        print("Final result: NOT FOUND")

        return

    # If possibly present, verify using SQLite
    print(f"\n{item_value}")
    print("Bloom Filter: Possibly present")
    print("Checking SQLite database...")

    cursor = connection.cursor()

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

    result = cursor.fetchone()

    if result:
        print("Final result: FOUND in database")
    else:
        print("Final result: NOT FOUND (False Positive)")


def main():

    connection = sqlite3.connect(DATABASE_FILE)

    print("BLOOM FILTER + SQLITE INTEGRATION")
    print("=" * 50)

    bloom = load_bloom_filter(connection)

    print("\nMEMBERSHIP TESTS")
    print("-" * 50)

    # Test existing username
    check_item(
        bloom,
        connection,
        "username",
        "registered_user_10"
    )

    # Test unknown username
    check_item(
        bloom,
        connection,
        "username",
        "unknown_user_9999"
    )

    # Test existing URL
    check_item(
        bloom,
        connection,
        "url",
        "https://example10.com"
    )

    # Test unknown URL
    check_item(
        bloom,
        connection,
        "url",
        "https://unknown-example9999.com"
    )

    connection.close()

    print("\nIntegration testing completed!")


if __name__ == "__main__":
    main()
