"""PC Watch entry point."""
from pathlib import Path
import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box
from rich.text import Text

from pcwatch.scanner import (
    APP_DIR, BASELINE_FILE, save_baseline, load_baseline,
    compare_to_baseline, save_report, REVIEW_EXTENSIONS
)

console = Console()

def show_report(report):
    console.print(Panel(
        f"[bold]Folder:[/bold] {report['folder']}\n"
        f"[bold]Checked:[/bold] {report['checked_utc']}\n"
        f"[bold]Files scanned:[/bold] {report['total_files']}",
        title="PC Watch Scan", border_style="bright_magenta"
    ))

    table = Table(box=box.ROUNDED)
    table.add_column("Finding", style="bold")
    table.add_column("Count", justify="right")
    table.add_column("Details")
    for key, label, style in [
        ("added", "Added", "green"),
        ("modified", "Modified", "yellow"),
        ("missing", "Missing", "red"),
        ("review_extensions", "Extension review", "magenta"),
    ]:
        items = report[key]
        preview = ", ".join(items[:4])
        if len(items) > 4:
            preview += f" ... (+{len(items)-4})"
        table.add_row(f"[{style}]{label}[/{style}]", str(len(items)), preview or "None")
    console.print(table)

    if report["scan_errors"]:
        console.print(f"[yellow]Skipped {len(report['scan_errors'])} file(s) due to access errors.[/yellow]")
    console.print(
        "[dim]Extension review is a heuristic only. A file extension does not prove a file is harmful.[/dim]"
    )

def main():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    console.print()
    console.print(Text("██████╗  ██████╗    ██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗", style="bold bright_magenta"))
    console.print(Text("██╔══██╗██╔════╝    ██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║", style="bold bright_magenta"))
    console.print(Text("██████╔╝██║         ██║ █╗ ██║███████║   ██║   ██║     ███████║", style="bold bright_magenta"))
    console.print(Text("██╔═══╝ ██║         ██║███╗██║██╔══██║   ██║   ██║     ██╔══██║", style="bold bright_magenta"))
    console.print(Text("██║     ╚██████╗    ╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║", style="bold bright_magenta"))
    console.print(Text("╚═╝      ╚═════╝     ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝", style="bold bright_magenta"))
    console.print(Panel("PC Watch | Local file integrity monitoring", subtitle="Windows / macOS / Linux"))

    while True:
        console.print("\n[bold]1[/bold] Create or replace baseline")
        console.print("[bold]2[/bold] Scan against baseline")
        console.print("[bold]3[/bold] Show baseline information")
        console.print("[bold]4[/bold] Open reports folder")
        console.print("[bold]5[/bold] Exit")
        choice = Prompt.ask("Select", choices=["1", "2", "3", "4", "5"])

        if choice == "1":
            folder = Prompt.ask("Folder to monitor (paste full path)")
            try:
                if not Confirm.ask(
                    f"Create a baseline for [cyan]{Path(folder).expanduser()}[/cyan]?"
                ):
                    continue
                snapshot = save_baseline(folder)
                console.print(
                    f"[green]Baseline saved.[/green] "
                    f"{len(snapshot['files'])} files recorded."
                )
                console.print(f"[dim]Location: {BASELINE_FILE}[/dim]")
            except (OSError, ValueError) as exc:
                console.print(f"[red]Could not create baseline: {exc}[/red]")

        elif choice == "2":
            try:
                baseline = load_baseline()
                report = compare_to_baseline(baseline)
                show_report(report)
                path = save_report(report)
                console.print(f"[green]Report saved:[/green] {path}")
            except (OSError, ValueError, KeyError) as exc:
                console.print(f"[red]Scan failed: {exc}[/red]")

        elif choice == "3":
            try:
                baseline = load_baseline()
                console.print(Panel(
                    f"Folder: {baseline['folder']}\n"
                    f"Created: {baseline['created_utc']}\n"
                    f"Files: {len(baseline['files'])}\n"
                    f"Baseline file: {BASELINE_FILE}"
                ))
            except (OSError, ValueError) as exc:
                console.print(f"[yellow]{exc}[/yellow]")

        elif choice == "4":
            console.print(f"Reports are stored at: {APP_DIR / 'reports'}")

        elif choice == "5":
            console.print("PC Watch closed.")
            break

if __name__ == "__main__":
    main()
