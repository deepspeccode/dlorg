import os
import shutil
import sys
import time
import argparse

def print_with_ellipsis(message):
    print(message, end='', flush=True)
    for _ in range(6):
        time.sleep(0.5)
        print('.', end='', flush=True)
    print("Done!")

def organize_downloads(downloads_path, main_destination):
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

    print_with_ellipsis("Creating Folders")
    for folder in folders:
        folder_path = os.path.join(main_destination, folder)
        os.makedirs(folder_path, exist_ok=True)

    print_with_ellipsis("Moving Files")
    for item in os.listdir(downloads_path):
        item_path = os.path.join(downloads_path, item)
        if os.path.isfile(item_path):
            file_ext = os.path.splitext(item)[1].lower()
            for folder, extensions in folders.items():
                if file_ext in extensions:
                    destination = os.path.join(main_destination, folder, item)
                    shutil.move(item_path, destination)
                    print(f"Moved {item} to {folder}")
                    break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files from a source directory into categorized folders in a destination directory.")
    parser.add_argument("-s", "--source", help="Source directory to organize (default: ~/Downloads)", default=os.path.expanduser("~/Downloads"))
    parser.add_argument("-d", "--destination", help="Destination directory for organized files (default: ~/Organized)", default=os.path.expanduser("~/Organized"))
    args = parser.parse_args()

    downloads_path = args.source
    main_destination = args.destination

    print(f"Source folder: {downloads_path}")
    print(f"Destination folder: {main_destination}")

    print_with_ellipsis("Searching Downloads folder")
    print_with_ellipsis("Checking file types")

    organize_downloads(downloads_path, main_destination)

    print("\nDlorg Complete!")
    print("\nHave a wonderful day!")
    
    print(f"\nYou can now cd into the new folder: {main_destination}")
    print("To see the organized files, use 'ls' or 'dir' command in the terminal.")