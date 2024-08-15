import os
import shutil
import sys
import random
import time

def print_with_ellipsis(message):
    print(message, end='', flush=True)
    for _ in range(6):
        time.sleep(0.5)
        print('.', end='', flush=True)
    print("Done!")

def create_dummy_files(dummy_downloads):
    file_types = {
        'PDFs': ['.pdf'],
        'Executables': ['.exe', '.msi'],
        'Images': ['.jpg', '.png'],
        'ZipFiles': ['.zip', '.rar'],
        'Documents': ['.doc', '.txt'],
        'Spreadsheets': ['.xlsx', '.csv'],
        'Audio': ['.mp3', '.wav'],
        'Video': ['.mp4', '.avi'],
        'HTML': ['.html'],
        'DiscImages': ['.iso'],
        'PHP': ['.php'],
        'JSON': ['.json'],
        'QIF': ['.qif'],
        'CRDOWNLOAD': ['.crdownload']
    }

    for category, extensions in file_types.items():
        for ext in extensions:
            for i in range(random.randint(1, 3)):
                filename = f"dummy_{category}_{i}{ext}"
                filepath = os.path.join(dummy_downloads, filename)
                with open(filepath, 'w') as f:
                    f.write(f"Dummy content for {filename}")

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
                    break

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dummy_downloads = os.path.join(script_dir, "Downloads")
    dummy_destination = os.path.join(script_dir, "Organized")

    os.makedirs(dummy_downloads, exist_ok=True)
    
    print_with_ellipsis("Searching Downloads folder")
    create_dummy_files(dummy_downloads)
    
    print_with_ellipsis("Checking file types")
    
    organize_downloads(dummy_downloads, dummy_destination)

    print("\nDlorg Complete!")
    print("\nHave a wonderful day!")
    
    print(f"\nYou can now cd into the new folder: {dummy_destination}")
    print("To see the organized files, use 'ls' or 'dir' command in the terminal.")