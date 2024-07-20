# rm_analyzer

## Installation
- [ ] Install `Python 3.12` and `Git`.
- [ ] `cd` to the project directory.
- [ ] Run `pip install -r requirements.txt`.
- [ ] Run `mkdir .config`. Ask me for the `config.json` to place in the `.config` folder.
- [ ] Run `mkdir .auth`. Ask me for the `credentials.json` to place in the `.auth` folder.

## Usage
```
# Open shell
# Project located at '~/rm_analyzer', e.g.
cd ~

# Analyze latest '*-transactions.csv' in the Downloads folder
python rm_analyzer

# Analyze latest CSV saved to a dedicated folder
python rm_analyzer /Users/roccodavino/Documents/Transactions/

# Analyze a particular CSV
python rm_analyzer /Users/roccodavino/Documents/Transactions/test-transactions.csv
```
