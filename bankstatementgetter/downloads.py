import pandas as pd
from pathlib import Path



def get_latest_download(path):
    """Function to get the latest file in a directory."""

    path = Path(path)
    files = path.glob('*')
    return max(files, key=lambda x: x.stat().st_ctime)


def rename_download_file(path, start_date, end_date):
    """Function to rename file."""

    path = Path(path)

    start_date = start_date.replace('/', '')
    end_date = end_date.replace('/', '')

    new_name = path.parents[0] / f"statement-download_{start_date}-{end_date}.csv"

    path.rename(new_name)

    return str(new_name)



def load_statement(file):
    """Load downloaded statement file in pandas DataFrame."""

    df = pd.read_csv(file)

    expected_cols = [
        'Transaction Date',
        'Transaction Type',
        'Transaction Description',
        'Debit Amount',
        'Credit Amount',
        'Balance'
    ]

    for col in expected_cols:

        if not col in df.columns.values:

            raise ValueError(f'column {col} not in {file}')

    df = df[expected_cols]

    # add column that will be manually filled later
    df['Category'] = None

    return df




