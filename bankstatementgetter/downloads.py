from pathlib import Path



def get_latest_download(path):
    """Function to get the latest file in a directory."""

    path = Path(path)
    files = path.glob('*')
    return max(files, key=lambda x: x.stat().st_ctime)

