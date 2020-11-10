import pandas as pd
from pathlib import Path



class DownloadsManager():
    """Class to manage all the actions related to downloaded files."""

    def __init__(self):

        self.expected_statement_cols = [
            'Transaction Date',
            'Transaction Type',
            'Transaction Description',
            'Debit Amount',
            'Credit Amount',
            'Balance'
        ]

    def get_latest_download(self, path):
        """Function to get the latest file in a directory."""

        path = Path(path)
        files = path.glob('*')
        return max(files, key=lambda x: x.stat().st_ctime)

    def rename_download_file(self, path, start_date, end_date):
        """Function to rename file."""

        path = Path(path)

        start_date = start_date.replace('/', '')
        end_date = end_date.replace('/', '')

        new_name = path.parents[0] / f"statement-download_{start_date}-{end_date}.csv"

        path.rename(new_name)

        return str(new_name)

    def load_statement(self, file):
        """Load downloaded statement file in pandas DataFrame."""

        df = pd.read_csv(file)

        for col in self.expected_statement_cols:

            if not col in df.columns.values:

                raise ValueError(f'column {col} not in {file}')

        df = df[self.expected_statement_cols]

        # add column that will be manually filled later
        df['Category'] = None

        return df

    def get_max_date_from_statement(self, df):
        """Function to get the maximum date from a statement."""

        if not 'Transaction Date' in df.columns.values:

            raise ValueError('''expecting 'Transaction Date' to be in df columns''')

        max_date_in_file = pd.to_datetime(df['Transaction Date'], dayfirst = True).max().strftime('%d/%m/%Y')

        return max_date_in_file
    
    def update_statement(self, df1, df2):
        """Function to append 2 statement files and exclude any duplicated transactions.
        
        df2 contains last transactions and df1 is appended onto df2.
        """

        if df2.duplicated(subset = self.expected_statement_cols).sum() > 0:

            raise ValueError('duplicate transactions in df2')

        df_appended = df2.append(df1)

        df_appended = df_appended.loc[~df_appended.duplicated(subset = self.expected_statement_cols)]

        return df_appended

