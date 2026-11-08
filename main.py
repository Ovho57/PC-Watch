"""PC Watch simple terminal interface."""
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import box
from rich.text import Text

from pcwatch.scanner import APP_DIR, save_baseline, load_baseline, check_changes, save_report

console = Console()


def print_items(title, items, color):
    console.print(f"\n[bold {color}]{title} ({len(items)})[/bold {color}]")
    if not items:
        console.print("[dim]Nothing to show.[/dim]")
        return
    table = Table(box=box.SIMPLE)
    table.add_column("Type", style="cyan")
    table.add_column("Path")
    table.add_column("Date / time")
    for path, meta in items:
        table.add_row(meta.get("type", "item"), path, meta.get("modified_display", "Unknown"))
    console.print(table)


def show_changes(report):
    console.print(Panel(
        f"[bold]Monitoring:[/bold] {report['folder']}\n"
        f"[bold]Checked:[/bold] {report['checked']}",
        title="PC WATCH — Quick Check", border_style="bright_magenta"
    ))
    print_items("Added files / folders", report["added"], "green")
    print_items("Modified files / folders", report["modified"], "yellow")
    print_items("Missing files / folders", report["missing"], "red")
    if report["errors"]:
        console.print(f"[yellow]Some entries could not be read: {len(report['errors'])}[/yellow]")


def select_folder():
    current = None
    try:
        current = load_baseline().get("folder")
    except (OSError, ValueError, KeyError):
        pass

    console.print("\nPaste the full folder path you want PC Watch to monitor.")
    if current:
        console.print(f"[dim]Current folder: {current}[/dim]")
    folder = Prompt.ask("Folder path", default=current or str(Path.home()))
    try:
        snapshot = save_baseline(folder)
        console.print(Panel(
            f"Monitoring folder set to:\n[cyan]{snapshot['folder']}[/cyan]\n"
            f"Recorded {len(snapshot['entries'])} files and folders.\n"
            "This setup uses file size and modified time, not slow hashing.",
            title="PC Watch ready", border_style="green"
        ))
    except (OSError, ValueError) as exc:
        console.print(f"[red]Could not set folder: {exc}[/red]")


def main():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    console.print()
    console.print(Text("██████╗  ██████╗    ██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗", style="bold bright_magenta"))
    console.print(Text("██╔══██╗██╔════╝    ██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║", style="bold bright_magenta"))
    console.print(Text("██████╔╝██║         ██║ █╗ ██║███████║   ██║   ██║     ███████║", style="bold bright_magenta"))
    console.print(Text("██╔═══╝ ██║         ██║███╗██║██╔══██║   ██║   ██║     ██╔══██║", style="bold bright_magenta"))
    console.print(Text("██║     ╚██████╗    ╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║", style="bold bright_magenta"))
    console.print(Text("╚═╝      ╚═════╝     ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝", style="bold bright_magenta"))
    console.print(Panel(
        "[bold bright_magenta]PC WATCH[/bold bright_magenta]\n"
        "Fast file and folder change monitor",
        subtitle="Local monitoring • No file hashing"
    ))

    try:
        load_baseline()
    except (OSError, ValueError, KeyError):
        console.print("[yellow]First run: choose a folder to monitor.[/yellow]")
        select_folder()

    while True:
        console.print("\n[bold]1[/bold] View added / modified / missing files and folders")
        console.print("[bold]2[/bold] Change monitored folder / reset starting point")
        console.print("[bold]3[/bold] Exit")
        choice = Prompt.ask("Choose", choices=["1", "2", "3"])

        if choice == "1":
            try:
                report = check_changes(load_baseline())
                show_changes(report)
                report_path = save_report(report)
                console.print(f"\n[dim]Report saved: {report_path}[/dim]")
            except (OSError, ValueError, KeyError) as exc:
                console.print(f"[red]Check failed: {exc}[/red]")
        elif choice == "2":
            select_folder()
        else:
            console.print("PC Watch closed.")
            break


if __name__ == "__main__":
    main()
