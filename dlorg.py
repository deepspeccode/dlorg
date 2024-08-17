import os
import shutil
import sys
import time
import argparse
import json
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, TaskID
from rich import print as rprint
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.align import Align

# Constants
ELLIPSIS_SLEEP_TIME = 0.5
ELLIPSIS_ITERATIONS = 6

# Initialize Rich console
console = Console()

# ASCII Art Logo
DLORG_LOGO = """
[bold cyan]
 ____  _     ___  ____   ____ 
|  _ \| |   / _ \|  _ \ / ___|
| | | | |  | | | | |_) | |  _ 
| |_| | |__| |_| |  _ <| |_| |
|____/|_____\___/|_| \_\\\\____|
[/bold cyan]
"""

def load_config(config_path: str) -> Dict[str, List[str]]:
    """Load folder configuration from a JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)

def save_config(config_path: str, folders: Dict[str, List[str]]) -> None:
    """Save folder configuration to a JSON file."""
    with open(config_path, 'w') as f:
        json.dump(folders, f, indent=4)

def print_with_ellipsis(message: str) -> None:
    """Print a message with animated ellipsis using Rich."""
    with console.status(message, spinner="dots"):
        time.sleep(ELLIPSIS_ITERATIONS * ELLIPSIS_SLEEP_TIME)
    console.print(f"[bold green]{message} Done![/bold green]")

def move_file(item: str, source: str, destination: str) -> None:
    """Move a file from source to destination."""
    source_path = os.path.join(source, item)
    dest_path = os.path.join(destination, item)
    
    if os.path.exists(dest_path):
        base, extension = os.path.splitext(item)
        counter = 1
        while os.path.exists(dest_path):
            new_name = f"{base}_{counter}{extension}"
            dest_path = os.path.join(destination, new_name)
            counter += 1
    
    shutil.move(source_path, dest_path)

def organize_downloads(downloads_path: str, main_destination: str, folders: Dict[str, List[str]], dry_run: bool = False) -> List[str]:
    """Organize files from downloads_path into categorized folders in main_destination."""
    moved_files = []

    print_with_ellipsis("Creating Folders")
    for folder in folders:
        folder_path = os.path.join(main_destination, folder)
        os.makedirs(folder_path, exist_ok=True)

    print_with_ellipsis("Organizing Files")
    with Progress() as progress:
        task = progress.add_task("[cyan]Moving files...", total=len(os.listdir(downloads_path)))
        with ThreadPoolExecutor() as executor:
            futures = []
            for item in os.listdir(downloads_path):
                item_path = os.path.join(downloads_path, item)
                if os.path.isfile(item_path):
                    file_ext = os.path.splitext(item)[1].lower()
                    for folder, extensions in folders.items():
                        if file_ext in extensions:
                            destination = os.path.join(main_destination, folder)
                            if not dry_run:
                                futures.append(executor.submit(move_file, item, downloads_path, destination))
                            moved_files.append(f"{'Would move' if dry_run else 'Moved'} {item} to {folder}")
                            break

            if not dry_run:
                for future in as_completed(futures):
                    future.result()
                    progress.update(task, advance=1)

    return moved_files

def display_menu():
    menu_items = [
        "[1] [bold green]Organize files[/bold green]",
        "[2] [bold yellow]View current configuration[/bold yellow]",
        "[3] [bold blue]Add new folder[/bold blue]",
        "[4] [bold red]Remove folder[/bold red]",
        "[5] [bold magenta]Add file extension to folder[/bold magenta]",
        "[6] [bold cyan]Remove file extension from folder[/bold cyan]",
        "[7] [bold]Exit[/bold]"
    ]
    menu_text = "\n".join(menu_items)
    console.print(Panel(menu_text, title="[bold]Dlorg Menu[/bold]", border_style="bold green", expand=False))

def view_configuration(folders: Dict[str, List[str]]):
    table = Table(title="[bold]Current Configuration[/bold]", show_header=True, header_style="bold magenta", border_style="cyan")
    table.add_column("Folder", style="cyan", no_wrap=True)
    table.add_column("File Extensions", style="green")

    for folder, extensions in folders.items():
        table.add_row(folder, ", ".join(extensions))

    console.print(table)

def add_folder(folders: Dict[str, List[str]]):
    folder_name = Prompt.ask("[bold blue]Enter the name of the new folder[/bold blue]")
    extensions = Prompt.ask("[bold blue]Enter file extensions for this folder (comma-separated)[/bold blue]")
    folders[folder_name] = [ext.strip().lower() for ext in extensions.split(",")]
    console.print(f"[bold green]Added folder '{folder_name}' with extensions: {', '.join(folders[folder_name])}[/bold green]")

def remove_folder(folders: Dict[str, List[str]]):
    folder_name = Prompt.ask("[bold red]Enter the name of the folder to remove[/bold red]")
    if folder_name in folders:
        del folders[folder_name]
        console.print(f"[bold green]Removed folder '{folder_name}'[/bold green]")
    else:
        console.print(f"[bold red]Folder '{folder_name}' not found[/bold red]")

def add_extension(folders: Dict[str, List[str]]):
    folder_name = Prompt.ask("[bold magenta]Enter the name of the folder to add extension to[/bold magenta]")
    if folder_name in folders:
        extension = Prompt.ask("[bold magenta]Enter the file extension to add[/bold magenta]").strip().lower()
        if extension not in folders[folder_name]:
            folders[folder_name].append(extension)
            console.print(f"[bold green]Added extension '{extension}' to folder '{folder_name}'[/bold green]")
        else:
            console.print(f"[bold yellow]Extension '{extension}' already exists in folder '{folder_name}'[/bold yellow]")
    else:
        console.print(f"[bold red]Folder '{folder_name}' not found[/bold red]")

def remove_extension(folders: Dict[str, List[str]]):
    folder_name = Prompt.ask("[bold cyan]Enter the name of the folder to remove extension from[/bold cyan]")
    if folder_name in folders:
        extension = Prompt.ask("[bold cyan]Enter the file extension to remove[/bold cyan]").strip().lower()
        if extension in folders[folder_name]:
            folders[folder_name].remove(extension)
            console.print(f"[bold green]Removed extension '{extension}' from folder '{folder_name}'[/bold green]")
        else:
            console.print(f"[bold yellow]Extension '{extension}' not found in folder '{folder_name}'[/bold yellow]")
    else:
        console.print(f"[bold red]Folder '{folder_name}' not found[/bold red]")

def main():
    parser = argparse.ArgumentParser(description="Organize files from a source directory into categorized folders in a destination directory.")
    parser.add_argument("-s", "--source", help="Source directory to organize (default: ~/Downloads)", default=os.path.expanduser("~/Downloads"))
    parser.add_argument("-d", "--destination", help="Destination directory for organized files (default: ~/Organized)", default=os.path.expanduser("~/Organized"))
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without moving files")
    parser.add_argument("--config", help="Path to the folder configuration JSON file", default="folder_config.json")
    args = parser.parse_args()

    downloads_path = args.source
    main_destination = args.destination
    config_path = args.config

    console.print(Align.center(DLORG_LOGO))
    console.print(Panel.fit(
        f"[bold cyan]Source folder:[/bold cyan] {downloads_path}\n"
        f"[bold cyan]Destination folder:[/bold cyan] {main_destination}",
        title="[bold]Dlorg - File Organizer[/bold]",
        border_style="bold green"
    ))

    try:
        folders = load_config(config_path)
    except FileNotFoundError:
        console.print(f"[bold yellow]Config file not found: {config_path}[/bold yellow]")
        console.print("[bold yellow]Using default folder configuration.[/bold yellow]")
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

    while True:
        display_menu()
        choice = Prompt.ask("[bold]Enter your choice[/bold]", choices=["1", "2", "3", "4", "5", "6", "7"], default="7")

        if choice == "1":
            moved_files = organize_downloads(downloads_path, main_destination, folders, args.dry_run)
            console.print("\n[bold green]Dlorg Complete![/bold green]")
            
            if args.dry_run:
                console.print("\n[bold yellow]Dry run completed. No files were actually moved.[/bold yellow]")
            else:
                console.print("\n[bold green]Files have been organized successfully.[/bold green]")
            
            console.print("\n[bold cyan]Summary of actions:[/bold cyan]")
            table = Table(show_header=True, header_style="bold magenta", border_style="cyan")
            table.add_column("Action", style="cyan", width=12)
            table.add_column("File", style="green")
            table.add_column("Destination", style="yellow")

            for action in moved_files:
                parts = action.split()
                table.add_row(parts[0], parts[1], parts[3])

            console.print(table)
        elif choice == "2":
            view_configuration(folders)
        elif choice == "3":
            add_folder(folders)
        elif choice == "4":
            remove_folder(folders)
        elif choice == "5":
            add_extension(folders)
        elif choice == "6":
            remove_extension(folders)
        elif choice == "7":
            break

        save_config(config_path, folders)

    console.print("\n[bold cyan]Thank you for using Dlorg. Have a wonderful day![/bold cyan]")

if __name__ == "__main__":
    main()