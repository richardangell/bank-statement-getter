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

