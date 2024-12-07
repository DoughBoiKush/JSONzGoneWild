README.md

# **Discord Chat Log Converter**

This script converts Discord JSON chat logs into **HTML**, **Markdown**, and **CSV** formats with support for non-standard JSON formats, filtering options, and customizable CSS styling. It is optimized for large datasets with multi-threaded processing and detailed error handling.

---

## **Features**
- Converts Discord JSON chat logs into:
  - **HTML** (stylized with CSS)
  - **Markdown** (for easy sharing)
  - **CSV** (structured data export)
- Repairs inconsistent or corrupted JSON files.
- Multi-threaded processing for high performance with large datasets.
- Filter options for:
  - Authors
  - Keywords
  - Date ranges
- Detailed error handling and logging for problematic files.
- Customizable CSS styling for HTML output.
- CLI-based terminal GUI for visual progress and status updates.

---

## **Requirements and Prerequisites**

### **Software Requirements**
- **Python 3.8+**

### **Python Libraries**
Install the required Python libraries:
```bash
pip install rich markdown

JSON Requirements

JSON files should represent Discord chat logs in a dictionary or list format. The script includes support for repairing common JSON inconsistencies.



---

Folder Structure

Before running the script, organize your files as follows:

project/
├── input_logs/          # Directory for JSON chat logs
│   ├── chat1.json
│   ├── chat2.json
│   └── ...
├── output_logs/         # Directory where output files will be saved
│   ├── chat1.html
│   ├── chat1.md
│   ├── chat1.csv
│   ├── ...
│   └── error_log.txt
├── converter.py         # Main script
└── custom.css           # Optional CSS file for styling HTML


---

Installation

1. Clone or download the repository:

git clone <repository_url>
cd project


2. Install dependencies:

pip install rich markdown


3. (Optional) Create a custom.css file to define your own HTML styling.




---

Usage

Run the script with the following command:

python3 converter.py <input_directory> [options]

Options


---

Examples

1. Convert all logs in the input_logs/ directory:

python3 converter.py input_logs/


2. Convert logs from a specific author:

python3 converter.py input_logs/ --author "JohnDoe"


3. Convert logs with a date range filter and custom CSS:

python3 converter.py input_logs/ --start-date 2024-01-01 --end-date 2024-12-31 --css-file custom.css


4. Enable multi-threading for better performance:

python3 converter.py input_logs/ --threads 8




---

Output Formats

1. HTML: Stylized chat logs with optional custom CSS.


2. Markdown: Easily shareable, structured Markdown files.


3. CSV: Tabular data for analysis, including Author, Timestamp, Content, and Reactions.




---

Error Handling

1. Invalid JSON Files:

The script attempts to repair common JSON issues (e.g., trailing commas, improperly formatted arrays).

Irreparable files are skipped, and errors are logged in output_logs/error_log.txt.



2. Invalid CLI Arguments:

Descriptive error messages guide users on correcting input or options.



3. Missing Data:

Fields missing in JSON files are replaced with placeholders (e.g., "Unknown").





---

CSS Customization

To customize the HTML output style, create or modify the custom.css file. Example:

body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
    color: #333;
}

.message {
    border-bottom: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 5px;
}

Use the --css-file option to specify a custom CSS file.


---

Deleting Prior Outputs

The script includes a utility to delete all previously generated outputs:

python3 startfresh.py

This removes only the output files (HTML, Markdown, CSV) in the output_logs/ directory.


---

Enhancements

Multi-threading: Processes multiple files concurrently for efficiency.

Repair Functionality: Repairs inconsistencies in non-standard JSON files.

Customizable CSS: Define styles for better HTML output aesthetics.

Terminal GUI: Progress bars and status updates using the Rich library.



---

Contributions

Feel free to contribute by submitting a pull request or suggesting new features via GitHub Issues!



