
# Bloom Filter for Username and URL Checking

## 1. Project Overview

This project implements a Bloom Filter to efficiently check whether a username or URL may exist in a database.

A Bloom Filter is a space-efficient probabilistic data structure used for membership testing.

It can tell us:
- Definitely not present
- Possibly present

A Bloom Filter may produce false positives, but a correctly implemented standard Bloom Filter does not produce false negatives for inserted items.

Positive results are verified using an SQLite database.

## 2. Project Objectives

- Implement a Bloom Filter from scratch using Python.
- Check usernames and URLs efficiently.
- Understand hash functions and bit arrays.
- Measure false-positive probability.
- Compare theoretical and experimental results.
- Analyse memory usage.
- Compare lookup performance with SQLite and Python sets.

## 3. Technologies Used

- Python
- SQLite
- Matplotlib
- CSV
- Git and GitHub

## 4. Project Structure

```text
Bloom_Filter_Project/
│
├── data/
│   ├── bloom_filter.db
│   ├── experiment_results.csv
│   ├── experiment_results_v2.csv
│   └── performance_results.csv
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── src/
│   ├── bloom_filter.py
│   ├── experiment.py
│   ├── visualization.py
│   ├── database.py
│   ├── run_queries.py
│   ├── integration.py
│   └── performance.py
│
├── notebooks/
│
├── reports/
│   ├── graph1_theoretical_vs_observed.png
│   ├── graph2_filter_size_effect.png
│   ├── graph3_hash_function_effect.png
│   ├── data_quality_log.md
│   ├── statistical_analysis.md
│   └── er_diagram.md
│
├── README.md
└── requirements.txt
```

## 5. Installation

Make sure Python 3.10 or newer is installed.

Install the required library:

```bash
pip install -r requirements.txt
```

## 6. How to Run the Project

Run these commands from the project root directory.

### Step 1: Test Bloom Filter

```bash
python src/bloom_filter.py
```

### Step 2: Run Experiments

```bash
python src/experiment.py
```

### Step 3: Generate Graphs

```bash
python src/visualization.py
```

### Step 4: Create Database

```bash
python src/database.py
```

### Step 5: Execute SQL Queries

```bash
python src/run_queries.py
```

### Step 6: Test Bloom Filter and SQLite Integration

```bash
python src/integration.py
```

### Step 7: Compare Lookup Performance

```bash
python src/performance.py
```

## 7. Experimental Dataset

The project uses simulated data:

- 1,000 usernames and 1,000 URLs in the SQLite database.
- 1,000 inserted usernames in the false-positive experiments.
- 5,000 unseen usernames for testing.

The generated URLs are examples and are not verified malicious or safe URLs.

## 8. Statistical Formulas

### Theoretical False-Positive Probability

P(FP) = (1 - e^(-kn/m))^k

### Optimal Number of Hash Functions

k(opt) = (m/n) × ln(2)

Where:

- m = Number of bits in the filter
- n = Number of inserted items
- k = Number of hash functions

## 9. Performance Comparison

The project compares:

1. Bloom Filter + SQLite
2. Python Set
3. SQLite Direct Lookup

The performance experiment tests 4,000 queries and measures lookup time and the number of database lookups.

## 10. Key Experimental Finding

The lowest observed false-positive rate in the experiment was 0.06%, using:

- Filter size: 16,000 bits
- Hash functions: 11
- Inserted usernames: 1,000
- Unseen test usernames: 5,000

## 11. Important Note

A Bloom Filter is a probabilistic membership-checking structure.

It does not independently determine whether a URL is malicious or whether a username is genuinely registered. Positive results must be verified against the original database.

## Interactive Username and URL Checking

The project includes an interactive membership checker that allows users to check whether a username or URL may exist in the database.

### How to Run

1. Open the project folder in the terminal.
2. Run the following command:

```bash
python src/integration.py
```

3. Select the type of item you want to check:
   - Username
   - URL
4. Enter the username or URL when prompted.
5. The program checks the item using the Bloom Filter and verifies possible matches against the SQLite database.

### Understanding the Results

- **Definitely Not Present:** The Bloom Filter confirms that the item is not in the database.
- **Possibly Present:** The Bloom Filter indicates a possible match, so the SQLite database performs the final verification.
- **Found in Database:** The item exists in the database.
- **Not Found in Database:** The item does not exist in the database.

**Note:** A Bloom Filter can produce false positives. Therefore, a positive result must always be verified using the database.

## 12. Conclusion

This project demonstrates how Bloom Filters can reduce unnecessary database lookups while using compact memory.

It combines data structures, database management, probability, statistics, and experimental performance analysis.
