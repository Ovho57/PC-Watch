import pyfiglet
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

ACCENT = "#a855f7" 

GRADIENT = ["#a855f7", "#a855f7"]

def title(text):
    print("[bold " + ACCENT + "]" + text + "[/bold " + ACCENT + "]")

def good(text):
    print("[green]" + text + "[/green]")

def warn(text):
    print("[yellow]" + text + "[/yellow]")

def bad(text):
    print("[red]" + text + "[/red]")

def hex_to_rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]

def gradient_color(pos, stops):
    # pos goes from 0.0 (left) to 1.0 (right)
    n = len(stops) - 1
    x = min(max(pos, 0), 1) * n
    i = min(int(x), n - 1)
    f = x - i
    a = hex_to_rgb(stops[i])
    b = hex_to_rgb(stops[i + 1])
    r, g, bl = [round(a[k] + (b[k] - a[k]) * f) for k in range(3)]
    return "#{:02x}{:02x}{:02x}".format(r, g, bl)

def block_text(text, bulky=True):
    art = pyfiglet.figlet_format(text, font="banner3", width=200)
    lines = art.rstrip().split("\n")
    width = max(len(l) for l in lines) + 1
    lines = [l.ljust(width) for l in lines]

    t = Text()
    for line in lines:
        for col, ch in enumerate(line):
            filled = ch == "#"
            if bulky and col > 0 and line[col - 1] == "#":
                filled = True         
            if filled:
                t.append("█", style=gradient_color(col / (width - 1), GRADIENT))
            else:
                t.append(" ")
        t.append("\n")
    t.rstrip()
    return t

def header():
    console.print(Panel("[" + ACCENT + "][/" + ACCENT + "] Welcome to [bold]PC Watch[/bold]",
                        expand=False, border_style=ACCENT, padding=(0, 2)))
    console.print()
    console.print(block_text("PC WATCH"))
    console.print()
    console.print("[dim]Press [bold]Enter[/bold] to continue[/dim]")