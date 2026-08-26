# CSV Sum

**Task:** "Write Python code that reads sales.csv and sums the 'amount' column."

Verbatim model output from a benchmark run — Claude Haiku 4.5, no-skill arm vs ken arm, temperature 1, source `benchmarks/output.json`. Reproduce: `npx promptfoo@latest eval -c benchmarks/promptfooconfig.openrouter.yaml`.

## Without Ken — 14 lines of code

# Python code to read sales.csv and sum the 'amount' column

Here's a simple solution using pandas:

```python
import pandas as pd

# Read the CSV file
df = pd.read_csv('sales.csv')

# Sum the 'amount' column
total_amount = df['amount'].sum()

print(f"Total amount: ${total_amount:,.2f}")
```

## Alternative solutions:

**Using CSV module (without pandas):**
```python
import csv

total_amount = 0

with open('sales.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        total_amount += float(row['amount'])

print(f"Total amount: ${total_amount:,.2f}")
```

**Using DuckDB (efficient for large files):**
```python
import duckdb

result = duckdb.query("SELECT SUM(amount) as total FROM read_csv_auto('sales.csv')").to_df()
print(f"Total amount: ${result['total'][0]:,.2f}")
```

## Which to use?

- **pandas** - Best for general data analysis
- **csv module** - Lightweight, no dependencies
- **duckdb** - Best for large datasets

All assume your CSV has a header row with a column named `'amount'`.

## With Ken — 7 lines of code

```python
import csv

total = 0
with open('sales.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total += float(row['amount'])

print(total)
```

→ threw away: pandas (overkill for one column), ceiling: none — csv module owns it.

**14 → 7 lines of code** — same model, same prompt.
