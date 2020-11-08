import argparse
from datetime import datetime

import bankstatementgetter.export as export



def run_exporter(start_date, end_date):
    """Function to run bank statement getter all the way through."""
    
    if not datetime.strptime(end_date, '%d/%m/%Y') > datetime.strptime(start_date, '%d/%m/%Y'):

        raise ValueError(f'end_date ({end_date}) not after start_date ({start_date})')
    
    if datetime.strptime(end_date, '%d/%m/%Y') > datetime.now():

        raise ValueError(f'end_date ({end_date}) is in the future')

    exporter = export.BankStatementGetter(start_date, end_date)
    exporter.run()
    print(exporter.downloaded_file)
    
    
def check_date_format(string):
    """Function to check the date formatting of input args."""

    try:

        return datetime.strptime(string, '%d/%m/%Y').strftime('%d/%m/%Y')

    except Exception as err:

        raise argparse.ArgumentTypeError(f'{string} not in the correct dd/mm/yyyy format - {err}')



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Date range to export')

    parser.add_argument(
        '-s',
        '--start_date',
        type=check_date_format,
        required=True,
        help='start of the date range to export (dd/mm/yyyy)'
    )

    parser.add_argument(
        '-e',
        '--end_date',
        type=check_date_format,
        required=True,
        help='end of the date range to export (dd/mm/yyyy)'
    )

    args = parser.parse_args()

    run_exporter(start_date = args.start_date, end_date = args.end_date)
    