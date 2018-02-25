import os
import time

def get_downloads(download_dir = None):
    """
    Get the files in the download folder.
    Currently only works on mac.
    
    Args:
        None

    Returns:
        list: Files in the download folder.
    """
    
    if download_dir == None:
    
        if os.name == 'posix':

            download_dir = '/Users/richardangell/Downloads'
    
    download_dir_files = os.listdir(download_dir)
    
    return(download_dir_files)
    
    
def get_new_download(previous_files, timeout = 5):
    """
    Export bank statements from Halifax.
    
    Args:
        previous_files (list): list of files already in downloads folder.
        timeout (int): number of seconds to wait for new files to appear.

    Returns:
        str: The filename and path of the exported statement (single file).
    """
    
    count = 0
    
    # while the number of files in the downloads folder remains the same
    while (len(get_downloads()) == len(previous_files)) & (count < timeout):
        
        time.sleep(1)
    
        count += 1
        
    current_downloads = get_downloads()
    
    if len(current_downloads) == len(previous_files):
        
        raise ValueError('no file was not downloaded within timeout')
        
    else:
        
        # get the new files in the downloads folder
        new_files = list(set(current_downloads) - set(previous_files))

        if (len(new_files) != 1):
            
            print('new files: ', new_files)
            
            raise ValueError('more than one file added to download folder')
            
        else:
            
            return(new_files[0])
    
    
    
    
    
if __name__ == '__main__':

    files_download_folder = get_downloads()

    for f in files_download_folder:
        
        print(f)
        