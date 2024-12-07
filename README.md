Here is the detailed Usage Documentation and Function Documentation in Markdown format:


---

Discord Chat Log Converter

This Python script converts Discord chat logs (in JSON format) into multiple output formats (HTML, Markdown, and CSV) while offering filtering options, error handling, and customizable CSS styling. It includes features like multi-threaded processing for large datasets and terminal-based progress visualization using the Rich library.


---

Features

Supports input JSON chat logs with non-standard formats.

Outputs in HTML, Markdown, and CSV formats.

Filters by author, keyword, and date ranges (start and end).

Repairs and handles inconsistent JSON structures.

Includes a customizable CSS template for the HTML output.

Multi-threaded processing for enhanced performance on large datasets.

Terminal GUI with progress bars and clear logs for errors.

Error handling: logs errors to an error file and skips problematic files.



---

Installation

Requirements

1. Python 3.8+


2. Install dependencies:

pip install rich markdown



Folder Structure

project/
├── input_logs/
│   ├── chat1.json
│   ├── chat2.json
│   └── ...
├── output_logs/
│   ├── chat1.html
│   ├── chat1.md
│   ├── chat1.csv
│   ├── ...
│   └── error_log.txt
├── converter.py
└── custom.css (optional)


---

Usage

Command

python3 converter.py <input_directory> [options]

Options

Examples

1. Convert logs with no filters:

python3 converter.py input_logs/


2. Convert logs, filtering for messages from a specific author:

python3 converter.py input_logs/ --author "johndoe"


3. Convert logs with date filtering and custom CSS:

python3 converter.py input_logs/ --start-date 2024-01-01 --end-date 2024-12-31 --css-file custom.css


4. Use multi-threading for large datasets:

python3 converter.py input_logs/ --threads 8




---

Output Formats

1. HTML:

Stylish logs with CSS formatting applied.

Stored as chatname.html in output_logs/.



2. Markdown:

Exported in Markdown format for easy sharing.

Stored as chatname.md in output_logs/.



3. CSV:

Structured as rows with Author, Timestamp, Content, and Reactions.

Stored as chatname.csv in output_logs/.



4. Error Logs:

Files with issues are logged in error_log.txt.





---

Output Folder Structure

After processing, the output is organized in the output_logs folder:

output_logs/
├── chat1.html
├── chat1.md
├── chat1.csv
├── chat2.html
├── ...
└── error_log.txt


---

Function Documentation

repair_and_parse_json

def repair_and_parse_json(file_path):
    """
    Repairs and parses non-standard JSON files.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict | None: Parsed JSON data or None if unrecoverable.
    """

Repairs common JSON issues like trailing commas or improperly formatted arrays.

Attempts to recover data by trimming invalid segments if needed.



---

process_json

def process_json(file_path, output_folder, filters, css_content, progress_task, progress):
    """
    Processes a single JSON file, applying filters, and generates outputs.

    Args:
        file_path (str): Path to the JSON file.
        output_folder (str): Directory for saving outputs.
        filters (dict): Filtering options.
        css_content (str): CSS content for HTML styling.
        progress_task (Progress Task): Rich progress task instance.
        progress (Progress): Rich progress instance.
    """

Applies filters and repairs inconsistent data.

Generates HTML, Markdown, and CSV outputs.

Logs errors for problematic files.



---

create_html

def create_html(messages, output_folder, file_base, css_content):
    """
    Generates an HTML file with chat logs.

    Args:
        messages (list): Filtered chat messages.
        output_folder (str): Directory for saving outputs.
        file_base (str): Base name for the output file.
        css_content (str): CSS content for styling.
    """


---

create_markdown

def create_markdown(messages, output_folder, file_base):
    """
    Generates a Markdown file with chat logs.

    Args:
        messages (list): Filtered chat messages.
        output_folder (str): Directory for saving outputs.
        file_base (str): Base name for the output file.
    """


---

create_csv

def create_csv(messages, output_folder, file_base):
    """
    Generates a CSV file with chat logs.

    Args:
        messages (list): Filtered chat messages.
        output_folder (str): Directory for saving outputs.
        file_base (str): Base name for the output file.
    """


---

main

def main():
    """
    The main entry point of the script.
    - Parses arguments.
    - Applies filters.
    - Sets up multi-threading for JSON file processing.
    """


---

Error Handling

1. Invalid JSON:

Attempts to repair the file.

Logs irreparable files in error_log.txt.



2. Missing/Invalid Parameters:

Provides descriptive error messages for incorrect arguments.





---

Enhancements

Multi-threading: Processes multiple files simultaneously to save time.

Custom CSS: Modify custom.css or use the --css-file option.

Error Logs: Detailed logs for troubleshooting.



---

Contributions

Feel free to suggest improvements or contribute by submitting a pull request!

