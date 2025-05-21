'''
File System Utilities Module

Provides functions for managing temporary files and directories.
'''
from pathlib import Path

from logs import get_logger


logger = get_logger(__name__)

def clear_temp_folder(folder_path):
    '''
    Deletes all files in the specified folder.
    '''
    folder_path = Path(folder_path).resolve()
    deleted_files = []

    if not folder_path.exists():        
        logger.warning(f'Folder {folder_path} does not exist')        
        
        return deleted_files        
    
    if not folder_path.is_dir():
        logger.warning(f'Folder {folder_path} is not a directory')

        return deleted_files    
    
    logger.info(f'Absolute path being cleared: {folder_path}')

    for file in folder_path.rglob('*'):
        logger.info(f'Checking: {file} (is_file: {file.is_file()})')
        if file.is_file():
            try:
                file.unlink()
                deleted_files.append(file.name)                 
                logger.info(F'Deleted: {file.name}')
            except Exception as e:
                logger.error(f'Failed to delete {file.name} -> {e}')

    return deleted_files