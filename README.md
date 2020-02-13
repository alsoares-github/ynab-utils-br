# ynab-utils-br
Collection of utility scripts to fix some Brazilian bank and credit card statements to a format suitable for importing into YNAB.

This is a previously personal collection of scripts that I used to prepare bank and credit card statements to use with YNAB. The various scripts and corresponding notes on usage are listed below.

-------------------------

## Scripts

### Banco do Brasil
* `fix-bb-checking` Unix shell script to prepares a checking account statement. It expects a file named `extrato.ofx` containing the statement to be prepared in OFX format to be present in the directory. The scripts outputs the file `extrato_fixed.ofx` that can be directly imported into YNAB. Invokes the Python script `fix_bb_checking.py`.
* `fix-bb-credit` Unix shell script to prepare a credit card statement. It expects as argument the name of the statement file in OFX format to be prepared. It outputs the file `ourocard_fixed.odx`. Invokes the Python script `fix_bb_credit.py`.

### Bradesco
* `fix_bradesco_csv.py` Python script to prepare a credit card statement. It expects as argument the name of the statement file in CSV format to be prepated. The script outputs the file `bradesco_fixed.csv` that can be directly imported into YNAB.
