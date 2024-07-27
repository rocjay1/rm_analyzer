# rm_analyzer

## Installation

Windows: download executable at [rma.exe](https://gitlab.com/api/v4/projects/60171926/jobs/artifacts/main/raw/dist/rma.exe?job=build-windows).

## Configuration

Create `~/.rma/config.json`. Example:

```json
{
    "Categories": [
        "Dining & Drinks",
        "Groceries",
        "Bills & Utilities",
        "Travel & Vacation"
    ],
    "People": [
        {
            "Name": "George",
            "Accounts": [
                1234
            ],
            "Email": "boygeorge@gmail.com"
        },
        {
            "Name": "Tootie",
            "Accounts": [
                1313
            ],
            "Email": "tuttifruity@hotmail.com"
        }
    ],
    "Email": "bebas@gmail.com",
    "Factor": 0.5
}
```

## Usage
```
# Open shell
# Executable located at '~/Downloads', e.g.

# Analyze latest '*-transactions.csv' in the Downloads folder
~/Downloads/rma

# Analyze latest CSV saved to a dedicated folder
~/Downloads/rma /Users/roccodavino/Documents/Transactions/

# Analyze a particular CSV
~/Downloads/rma /Users/roccodavino/Documents/Transactions/test-transactions.csv
```
