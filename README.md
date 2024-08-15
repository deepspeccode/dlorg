# 📁 Downloads Organizer (dlorg)

![dlorg-banner](assets/dlorg-banner.png)

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

**dlorg** is a powerful and intuitive Python script that automatically organizes your cluttered Downloads folder into a neatly structured directory system. Say goodbye to the chaos and hello to a tidy digital workspace!

## ✨ Features

- 🚀 **Efficient Organization**: Sorts files based on their types into dedicated folders.
- 🎭 **Wide File Support**: Handles various file types including documents, images, videos, and more.
- 🔍 **Smart Recognition**: Automatically detects file types and places them in appropriate folders.
- 🛡️ **Safe Operation**: Doesn't delete any files, just moves them to new locations.
- 🎬 **Demo Mode**: Includes a demonstration mode for testing and presentation purposes.

## 🚀 Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/dlorg.git
   ```

2. Navigate to the dlorg directory:
   ```
   cd dlorg
   ```

3. Run the script:
   ```
   python dlorg.py
   ```

## 📋 Requirements

- Python 3.6 or higher

## 🛠️ Installation

1. Ensure you have Python 3.6+ installed on your system.
2. Download the `dlorg.py` script from this repository.
3. Place the script in a convenient location on your computer.

## 🖥️ Usage

### Basic Usage

Run the script from your terminal:

```
python path/to/dlorg.py
```

The script will automatically organize files from your Downloads folder into a new "Organized" directory.

### Demo Mode

To run the script in demo mode (for testing or presentation):

```
python path/to/dlorg_demo.py
```

This will create dummy files and demonstrate the organization process without affecting your actual files.

## 📁 Folder Structure

After running dlorg, your files will be organized into the following structure:

```
Organized/
├── PDFs/
├── Executables/
├── Images/
├── ZipFiles/
├── Documents/
├── Spreadsheets/
├── Audio/
├── Video/
├── HTML/
├── DiscImages/
├── PHP/
├── JSON/
├── QIF/
└── CRDOWNLOAD/
```

## 🎨 Customization

You can easily customize the script to fit your needs:

- Add new file types by editing the `folders` dictionary in the script.
- Change the destination folder by modifying the `main_destination` variable.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/yourusername/dlorg/issues).

## 📜 License

This project is [MIT](https://opensource.org/licenses/MIT) licensed.

## 👏 Acknowledgements

- Thanks to all the open-source projects that inspired this tool.
- Special thanks to the Python community for their invaluable resources.

---

<p align="center">
  Made with ❤️ by [Your Name]
</p>