import os
import shutil
import sys

def organize_downloads(downloads_path, main_destination):
    # Define folders for different file types
    folders = {
        'PDFs': ['.pdf'],
        'Executables': ['.exe', '.msi'],
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'ZipFiles': ['.zip', '.rar', '.7z'],
        'Documents': ['.doc', '.docx', '.txt', '.rtf', '.md'],
        'Spreadsheets': ['.xls', '.xlsx', '.csv'],
        'Audio': ['.mp3', '.wav', '.aac', '.flac'],
        'Video': ['.mp4', '.avi', '.mkv', '.mov'],
        'HTML': ['.html', '.htm'],
        'DiscImages': ['.iso', '.img'],
        'PHP': ['.php'],
        'JSON': ['.json'],
        'QIF': ['.qif'],
        'CRDOWNLOAD': ['.crdownload']
    }

    # Create destination folders
    for folder in folders:
        folder_path = os.path.join(main_destination, folder)
        os.makedirs(folder_path, exist_ok=True)

    try:
        for item in os.listdir(downloads_path):
            item_path = os.path.join(downloads_path, item)
            if os.path.isfile(item_path):
                file_ext = os.path.splitext(item)[1].lower()
                moved = False
                for folder, extensions in folders.items():
                    if file_ext in extensions:
                        destination = os.path.join(main_destination, folder, item)
                        shutil.move(item_path, destination)
                        print(f"Moved {item} to {folder}")
                        moved = True
                        break
                if not moved:
                    print(f"Unhandled file type: {item}")

    except FileNotFoundError:
        print(f"Error: The Downloads folder path '{downloads_path}' was not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when accessing '{downloads_path}'.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    downloads_path = os.path.expanduser("~/Downloads")
    main_destination = r"D:\Documents"

    print(f"Using Downloads folder: {downloads_path}")
    print(f"Main destination folder: {main_destination}")

    organize_downloads(downloads_path, main_destination)
    print("Downloads folder organization complete!")