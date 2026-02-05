from pathlib import Path
#import os

def createDirIfNotExists(directory_path):
    """Create directory if it does not exist."""    
    # Get the current working directory as a Path object
    current_directory = Path.cwd()
    # Construct the full path for the new directory
    new_directory_path = current_directory / directory_path

    # Create the directory
    try:
        # 'exist_ok=True' prevents an error if the directory already exists
        new_directory_path.mkdir(exist_ok=True)
        print(f"Directory created or already exists: {new_directory_path}")
    except OSError as e:
        print(f"Error creating directory: {e}")
        Path(directory_path).mkdir(parents=True, exist_ok=True)
    return new_directory_path
