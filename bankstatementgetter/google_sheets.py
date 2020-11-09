import pandas as pd
import gspread
# for gspread authentication see 
# https://gspread.readthedocs.io/en/latest/oauth2.html#oauth-client-id



class GoogleSheetsManager():

    def __init__(self):

        self.gc = gspread.oauth()
        self.google_sheets_name = 'statement'
        self.worksheet_name = 'statement'
        self.google_sheet = self.gc.open(self.google_sheets_name)
        self.worksheet = self.get_worksheet()

    def get_worksheet(self): 
        """Get the worksheet of interest from the google sheet."""

        return self.google_sheet.worksheet(self.worksheet_name)

    def download_google_sheet(self):
        """Download google sheet to pandas DataFrame."""

        df = pd.DataFrame(self.worksheet.get_all_records())

        return df

    def upload_to_google_sheet(self, df):
        """Upload pandas DataFrame to google sheet."""

        # rename the original worksheet
        self.worksheet.update_title('statement_old')
        
        # create a new worksheet with the correct name
        self.google_sheet.add_worksheet(title=self.worksheet_name, rows=f"{df.shape[0] + 100}", cols="26")

        # delete the current worksheet
        self.google_sheet.del_worksheet(self.worksheet)

        # get worksheet again 
        self.worksheet = self.get_worksheet()

        self.worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        