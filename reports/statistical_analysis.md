
# STATISTICAL ANALYSIS REPORT

## Project Title
Bloom Filter for Username and URL Checking

## 1. Objective of Statistical Analysis

The purpose of this analysis is to evaluate the performance of the Bloom Filter using statistical methods.

The analysis focuses on:

- The effect of bit-array size on false-positive rate.
- The effect of the number of hash functions.
- Comparison of theoretical and observed false-positive rates.
- Calculation of 95% confidence intervals.
- Memory usage.
- Performance comparison with SQLite and Python Set.

## 2. Experimental Dataset

The Bloom Filter experiment used the following dataset:

| Parameter | Value |
|---|---:|
| Inserted usernames | 1,000 |
| Unseen test usernames | 5,000 |
| Total configurations | 12 |
| Bit-array sizes | 8,000, 12,000, 16,000 bits |
| Hash-function counts | 3, 5, 6, 7, 8, 11 |

Each configuration was tested using the same inserted and unseen username datasets.

## 3. Statistical Hypotheses

The following hypotheses were considered:

**H1: Effect of bit-array size**

Increasing the bit-array size reduces the false-positive rate when the number of inserted items remains constant.

**H2: Effect of hash functions**

The false-positive rate depends on the number of hash functions. A suitable optimal value produces a lower false-positive rate.

**H3: Theoretical vs. observed results**

The observed false-positive rate should generally be close to the theoretical false-positive rate.

**H4: Database performance**

Using a Bloom Filter before SQLite lookup can reduce unnecessary database queries compared with direct SQLite lookup.

## 4. Theoretical Statistical Model

The theoretical false-positive probability of a Bloom Filter is:

P(FP) = (1 - e^(-kn/m))^k

Where:

- m = Number of bits in the filter
- n = Number of inserted items
- k = Number of hash functions
- e = Euler's number

The approximate optimal number of hash functions is:

k(opt) = (m/n) × ln(2)

For this experiment, the number of inserted usernames was 1,000.

Therefore:

| Bit-array size | Optimal hash functions |
|---:|---:|
| 8,000 | 6 |
| 12,000 | 8 |
| 16,000 | 11 |

## 5. Experimental Results

The following table presents the observed and theoretical false-positive rates.

| Bits | Hashes | Observed FPR | Theoretical FPR |
|---:|---:|---:|---:|
| 8,000 | 3 | 3.26% | 3.0579% |
| 8,000 | 5 | 1.94% | 2.1679% |
| 8,000 | 7 | 2.44% | 2.2930% |
| 12,000 | 3 | 1.16% | 1.0823% |
| 12,000 | 5 | 0.48% | 0.4595% |
| 12,000 | 7 | 0.42% | 0.3294% |
| 16,000 | 3 | 0.72% | 0.4998% |
| 16,000 | 5 | 0.08% | 0.1392% |
| 16,000 | 7 | 0.08% | 0.0702% |
| 8,000 | 6 | 1.94% | 2.1577% |
| 12,000 | 8 | 0.52% | 0.3142% |
| 16,000 | 11 | 0.06% | 0.0459% |

### Observations

1. The false-positive rate generally decreased as the bit-array size increased.
2. The 16,000-bit filter produced lower false-positive rates than the 8,000-bit filter in the tested configurations.
3. The best observed configuration was 16,000 bits with 11 hash functions.
4. This configuration produced only 3 false positives among 5,000 unseen usernames.
5. No false negatives were detected in any of the 12 configurations.

## 6. False-Positive Rate Calculation

The observed false-positive rate is calculated using:

Observed FPR = (False Positives / Unseen Test Queries) × 100

For the best configuration:

- False positives = 3
- Unseen test queries = 5,000

Observed FPR = (3 / 5,000) × 100

Observed FPR = 0.06%

This means that only 0.06% of unseen usernames were incorrectly reported as possibly present.

## 7. Binomial Probability Analysis

The number of false positives can be modelled approximately using a binomial distribution.

X ~ Binomial(N, p)

Where:

- N = Number of unseen test queries
- p = Theoretical false-positive probability
- X = Number of false positives

For each configuration:

N = 5,000

The observed false-positive rate is an estimate of the probability of a false positive.

The experiment assumes that individual query outcomes are approximately independent and have a common false-positive probability.

## 8. 95% Confidence Interval

A 95% Wilson confidence interval was calculated for each observed false-positive proportion.

For the best configuration:

- Bit-array size = 16,000 bits
- Hash functions = 11
- False positives = 3
- Test queries = 5,000
- Observed FPR = 0.06%

95% confidence interval:

0.0204% to 0.1763%

This interval represents statistical uncertainty around the observed false-positive proportion.

It does not guarantee that every future experiment will fall within this interval.

## 9. Effect Size Analysis

Effect size helps measure how much the false-positive rate changes when the bit-array size increases.

The relative reduction is calculated as:

Relative Reduction = 
((Old FPR - New FPR) / Old FPR) × 100

### Comparison at the same hash-function count

| Hash functions | 8,000-bit FPR | 16,000-bit FPR | Reduction |
|---:|---:|---:|---:|
| 3 | 3.26% | 0.72% | 77.91% |
| 5 | 1.94% | 0.08% | 95.88% |
| 7 | 2.44% | 0.08% | 96.72% |

### Interpretation

Increasing the bit-array size from 8,000 to 16,000 bits substantially reduced the observed false-positive rate in all three comparisons.

The largest relative reduction was approximately 96.72% when using 7 hash functions.

## 10. Memory Usage Analysis

The memory required for the bit array is:

Memory in bytes = Ceiling(m / 8)

| Bit-array size | Memory usage |
|---:|---:|
| 8,000 bits | 1,000 bytes |
| 12,000 bits | 1,500 bytes |
| 16,000 bits | 2,000 bytes |

The memory figures represent the bit-array storage only. They do not include the additional memory used by the Python object or other program data.

## 11. Theory vs. Experiment

The experimental results were generally close to the theoretical predictions.

However, some configurations showed differences between the observed and theoretical rates.

For example:

- At 8,000 bits and 3 hash functions, observed FPR was 3.26%, compared with theoretical FPR of 3.0579%.
- At 16,000 bits and 11 hash functions, observed FPR was 0.06%, compared with theoretical FPR of 0.0459%.

The theoretical formula is an approximation based on assumptions about hash distribution.

Differences can occur because of the finite test dataset and the actual hash positions generated by the implementation.

The theoretical values for two configurations (16,000 bits with 3 hashes, and 12,000 bits with 8 hashes) also fell slightly below their calculated 95% Wilson intervals. These differences should be considered when interpreting the model.

## 12. Assumption Checks and Limitations

The analysis uses the following assumptions:

1. Inserted usernames and unseen usernames are distinct.
2. Each configuration uses 1,000 inserted items and 5,000 unseen queries.
3. The hash functions distribute positions approximately uniformly.
4. Individual query outcomes are treated as approximately independent for the binomial model.
5. The theoretical formula is an approximation rather than an exact prediction.

### Limitations

- The dataset contains simulated usernames rather than real user records.
- Only one generated dataset was used for the main experiment.
- The experiment was not repeated across multiple independently generated datasets.
- The theoretical model assumes approximately uniform hash distribution.
- Results may vary with different datasets and system environments.

## 13. Performance Comparison

The project compared three lookup methods.

| Method | Median time |
|---|---:|
| Bloom Filter + SQLite | 0.052499 seconds |
| Python Set | 0.000405 seconds |
| SQLite Direct Lookup | 0.060597 seconds |

The performance experiment used:

- 2,000 database records
- 2,000 existing queries
- 2,000 unseen queries
- 4,000 total queries
- 5 repetitions, with median time reported

### Key Findings

1. Bloom Filter + SQLite was faster than direct SQLite lookup in this experiment.
2. Bloom Filter + SQLite reduced database lookups from 4,000 to 2,038.
3. This represents a reduction of approximately 49.05% in database queries.
4. The measured lookup-time improvement over direct SQLite was approximately 13.36%.
5. Python Set was the fastest because it performs in-memory lookups without database access.

The Python Set comparison is not a direct database-to-database comparison because it does not perform SQLite queries.

The measured times exclude the time required to build the data structures.

## 14. Final Statistical Findings

The statistical analysis supports the following findings:

- Increasing bit-array size generally reduces false-positive probability.
- Selecting a suitable number of hash functions improves Bloom Filter performance.
- The best observed configuration was 16,000 bits with 11 hash functions.
- Its observed false-positive rate was only 0.06%.
- No false negatives were detected in the experiment.
- Bloom Filter + SQLite reduced database queries by approximately 49.05%.
- The experimental results were generally consistent with the theoretical model, with some differences.

## 15. Conclusion

The statistical analysis demonstrates that Bloom Filters can provide efficient preliminary membership checking for usernames and URLs.

The experiment showed that bit-array size and the number of hash functions have an important effect on false-positive probability.

The best tested configuration achieved an observed false-positive rate of 0.06%, while maintaining zero false negatives.

The integration with SQLite also reduced the number of database lookups and improved measured lookup time compared with direct SQLite lookup.

Overall, the results demonstrate the usefulness of Bloom Filters as a space-efficient preliminary checking technique. Positive results must still be verified against the original database.
