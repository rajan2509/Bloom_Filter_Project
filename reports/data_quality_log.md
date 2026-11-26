
# DATA QUALITY LOG

## Project Title
Bloom Filter for Username and URL Checking

## 1. Dataset Description

This project uses simulated username and URL datasets
for testing Bloom Filter membership checking.

The database contains:
- 1,000 simulated usernames
- 1,000 simulated URLs
- Total: 2,000 records

Additional experimental datasets contain:
- 1,000 inserted usernames
- 5,000 unseen test usernames

These datasets were generated programmatically using
Python. They are not real user accounts or verified
malicious URLs.

## 2. Data Sources

| Dataset | Source | Type |
|---|---|---|
| Usernames | Python-generated values | Simulated |
| URLs | Python-generated example URLs | Simulated |
| Experiment data | Python experiment program | Generated |

## 3. Data Quality Checks

| Quality Check | Method | Result |
|---|---|---|
| Missing values | NOT NULL database constraint | Passed |
| Duplicate records | UNIQUE constraint | Prevented |
| Invalid item types | CHECK constraint | Prevented |
| Username count | SQL COUNT query | 1,000 |
| URL count | SQL COUNT query | 1,000 |
| Total records | SQL COUNT query | 2,000 |
| False-negative testing | Bloom Filter validation | 0 detected |
| Unseen test records | Separate generated dataset | 5,000 |

## 4. Data Cleaning and Validation

The following checks were performed:

1. Usernames and URLs were stored as text.
2. Separate item types were maintained.
3. Duplicate records of the same type were prevented.
4. Missing item types and values were restricted.
5. Inserted and unseen experimental usernames
   were generated using different naming patterns.
6. Bloom Filter membership was tested against
   the original inserted dataset.

## 5. Experimental Data Quality

The experiment tested 12 configurations.

Each configuration used:
- 1,000 inserted usernames
- 5,000 unseen usernames

Results showed zero false negatives across
all 12 configurations.

Observed false-positive rates varied according
to filter size and hash-function count.

## 6. Known Limitations

1. The datasets are simulated rather than real-world.
2. The URLs are examples and are not confirmed
   malicious or safe.
3. The experiment uses a limited dataset size.
4. Timing results depend on the computer and
   system environment.
5. Theoretical false-positive rates are approximate.
6. A false-positive result must be verified
   against the original database.

## 7. Conclusion

The data quality checks confirmed that the
simulated datasets were suitable for the
project's implementation and experiments.

The database constraints helped maintain
record consistency, and the membership tests
confirmed that no false negatives were detected.

The dataset limitations must be considered
when interpreting the experimental findings.
