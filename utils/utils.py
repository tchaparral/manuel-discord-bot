from pathlib import Path

def clear_temp_folder(folder_path, verbose = True):
    '''
    Deletes all files in the specified folder.
    '''
    folder_path = Path(folder_path).resolve()
    deleted_files = []

    if not folder_path.exists():
        if verbose:
            print(f'[WARNING] - Folder {folder_path} does not exist')        
        return deleted_files        
    
    if not folder_path.is_dir():
        if verbose:
            print(f'[WARNING] - Folder {folder_path} is not a directory')
        return deleted_files
    
    if verbose:
        print(f'[DEBUG] - Absolute path being cleared: {folder_path}')

    for file in folder_path.rglob('*'):
        print(f'[DEBUG] - Checking: {file} (is_file: {file.is_file()})')
        if file.is_file():
            try:
                file.unlink()
                deleted_files.append(file.name)
                if verbose: 
                    print(F'[INFO] - Deleted: {file.name}')
            except Exception as e:
                if verbose:
                    print(f'[ERROR] - Failed to delete {file.name} -> {e}')

    return deleted_files