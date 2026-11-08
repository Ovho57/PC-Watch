from rich import print
from rich.table import Table

def show_report(results):
    table = Table(title="PC Watch Report")
    table.add_column("Type")
    table.add_column("File")
    colors = {"added": "green", "modified": "yellow", "missing": "red", "suspicious": "red"}

    for kind in results:
        c = colors[kind]
        for name in results[kind]:
            table.add_row("[" + c + "]" + kind.upper() + "[/" + c + "]", name)
    print(table)
