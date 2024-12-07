import os
import json
import argparse
from datetime import datetime
from markdown import markdown
import csv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeElapsedColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

# Initialize Rich console
console = Console()

# Default CSS styling
DEFAULT_CSS = """
body {
    font-family: Arial, sans-serif;
    background-color: #121212;
    color: #E0E0E0;
    padding: 20px;
    line-height: 1.6;
}
.message {
    border: 1px solid #333;
    border-radius: 8px;
    margin-bottom: 15px;
    padding: 15px;
    background-color: #1E1E1E;
}
.author {
    font-weight: bold;
    color: #FFD700;
}
.timestamp {
    color: #999;
    font-size: 0.85em;
}
.content {
    margin-top: 10px;
}
.reactions {
    font-style: italic;
    color: #8FBC8F;
    margin-top: 5px;
}
"""

# Function to repair and parse JSON data
def repair_and_parse_json(file_path):
    try:
        with open(file_path, 'r') as f:
            raw_data = f.read()
        # Repair common JSON issues
        cleaned_data = raw_data.replace(",]", "]").replace(",}", "}").strip()
        try:
            return json.loads(cleaned_data)
        except json.JSONDecodeError:
            start = cleaned_data.find("[")
            end = cleaned_data.rfind("]") + 1
            if start != -1 and end != -1:
                return json.loads(cleaned_data[start:end])
            else:
                raise ValueError("Unable to parse JSON data.")
    except Exception as e:
        console.print(f"[bold red]Error reading or repairing JSON file[/bold red] {file_path}: {e}")
        return None

# Process a single JSON file
def process_json(file_path, output_folder, filters, css_content, progress_task, progress):
    try:
        data = repair_and_parse_json(file_path)
        if not data:
            raise ValueError("Invalid or unrepairable JSON data.")

        # Apply filters
        filtered_messages = []
        for msg in data:
            timestamp = datetime.fromtimestamp(msg.get("timestamp", 0) / 1000)
            if filters["author"] and filters["author"] != msg.get("author", "").lower():
                continue
            if filters["keyword"] and filters["keyword"] not in msg.get("content", "").lower():
                continue
            if filters["start_date"] and timestamp < filters["start_date"]:
                continue
            if filters["end_date"] and timestamp > filters["end_date"]:
                continue
            filtered_messages.append(msg)

        # Sort messages by timestamp
        filtered_messages.sort(key=lambda x: x.get("timestamp", 0))

        # Generate outputs
        file_base = Path(file_path).stem
        create_html(filtered_messages, output_folder, file_base, css_content)
        create_markdown(filtered_messages, output_folder, file_base)
        create_csv(filtered_messages, output_folder, file_base)

        progress.update(progress_task, advance=1)
    except Exception as e:
        error_message = f"Error processing {file_path}: {e}"
        with open(Path(output_folder) / "error_log.txt", "a") as log:
            log.write(error_message + "\n")
        console.print(f"[bold red]{error_message}[/bold red]")

# Output HTML
def create_html(messages, output_folder, file_base, css_content):
    html_content = f"<html><head><style>{css_content}</style></head><body>"
    for msg in messages:
        html_content += f"""
        <div class="message">
            <div class="author">{msg.get("author", "Unknown")}</div>
            <div class="timestamp">{datetime.fromtimestamp(msg.get("timestamp", 0) / 1000)}</div>
            <div class="content">{msg.get("content", "")}</div>
            <div class="reactions">{msg.get("reaction_counts", "")}</div>
        </div>
        """
    html_content += "</body></html>"

    with open(Path(output_folder) / f"{file_base}.html", "w", encoding="utf-8") as f:
        f.write(html_content)

# Output Markdown
def create_markdown(messages, output_folder, file_base):
    md_content = ""
    for msg in messages:
        md_content += f"**{msg.get('author', 'Unknown')}** ({datetime.fromtimestamp(msg.get('timestamp', 0) / 1000)}):\n"
        md_content += f"{msg.get('content', '')}\n"
        md_content += f"_Reactions_: {msg.get('reaction_counts', '')}\n\n"

    with open(Path(output_folder) / f"{file_base}.md", "w", encoding="utf-8") as f:
        f.write(md_content)

# Output CSV
def create_csv(messages, output_folder, file_base):
    csv_file = Path(output_folder) / f"{file_base}.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Author", "Timestamp", "Content", "Reactions"])
        for msg in messages:
            writer.writerow([
                msg.get("author", "Unknown"),
                datetime.fromtimestamp(msg.get("timestamp", 0) / 1000),
                msg.get("content", ""),
                msg.get("reaction_counts", "")
            ])

# Main function with multi-threading
def main():
    parser = argparse.ArgumentParser(description="Convert Discord chat logs to various formats.")
    parser.add_argument("input_dir", help="Directory containing JSON chat logs.")
    parser.add_argument("--css-file", help="Path to a custom CSS file.", default=None)
    parser.add_argument("--author", help="Filter by author.", default=None)
    parser.add_argument("--keyword", help="Filter by keyword.", default=None)
    parser.add_argument("--start-date", help="Filter by start date (YYYY-MM-DD).", default=None)
    parser.add_argument("--end-date", help="Filter by end date (YYYY-MM-DD).", default=None)
    parser.add_argument("--threads", type=int, help="Number of threads for processing.", default=4)
    args = parser.parse_args()

    # Parse filters
    filters = {
        "author": args.author.lower() if args.author else None,
        "keyword": args.keyword.lower() if args.keyword else None,
        "start_date": datetime.strptime(args.start_date, "%Y-%m-%d") if args.start_date else None,
        "end_date": datetime.strptime(args.end_date, "%Y-%m-%d") if args.end_date else None,
    }

    # Load CSS
    css_content = DEFAULT_CSS
    if args.css_file and Path(args.css_file).exists():
        with open(args.css_file, "r") as f:
            css_content = f.read()

    # Create output directory
    output_folder = Path(args.input_dir) / "output_logs"
    output_folder.mkdir(parents=True, exist_ok=True)

    # Gather JSON files
    json_files = list(Path(args.input_dir).rglob("*.json"))

    # Display summary
    console.print(
        Panel(
            f"Processing [bold cyan]{len(json_files)} JSON files[/bold cyan] in directory [bold yellow]{args.input_dir}[/bold yellow]",
            title="[bold green]Discord Log Converter[/bold green]",
            expand=False,
        )
    )

    # Progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
    ) as progress:
        progress_task = progress.add_task("Processing files", total=len(json_files))

        # Process files with multi-threading
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            executor.map(
                partial(
                    process_json,
                    output_folder=output_folder,
                    filters=filters,
                    css_content=css_content,
                    progress_task=progress_task,
                    progress=progress,
                ),
                json_files,
            )

    console.print(f"[bold green]Processing complete![/bold green] Output files are saved in [bold yellow]{output_folder}[/bold yellow]")

if __name__ == "__main__":
    main()
