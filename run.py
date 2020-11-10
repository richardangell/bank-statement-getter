from bankstatementgetter.export import BankStatementExporter
from bankstatementgetter.google_sheets import GoogleSheetsManager



class ExporterAndUploader(BankStatementExporter, GoogleSheetsManager):
    """Class combining the exporting and google sheets functionality to run entire process."""

    def __init__(self):

        BankStatementExporter.__init__(self)
        GoogleSheetsManager.__init__(self)

    def run(self):
        """Method to go through the whole process of exporting statement and uploading to 
        google sheets.
        """
        
        # download the current google sheet
        google_sheets_statement = self.download_google_sheet()

        # get the max date in the current statement
        current_max_date = self.get_max_date_from_statement(google_sheets_statement)

        # export bank statement with start_date = current maximum in the statement
        self.export(start_date = current_max_date)

        # read in exported statement
        downloaded_statement = self.load_statement(self.downloaded_file)

        # appned the new downloaded statement to current on from google drive
        appended_statements = self.update_statement(google_sheets_statement, downloaded_statement)

        # upload to google sheets
        self.upload_to_google_sheet(appended_statements)



if __name__ == '__main__':
    
    exporter = ExporterAndUploader()  
    exporter.run()

    