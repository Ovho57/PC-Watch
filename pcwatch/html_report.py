def make_html(results):
    html = "<html><body><h1>PC Watch Report</h1>"
    for kind in results:
        html += "<h2>" + kind.title() + "</h2><ul>"
        for name in results[kind]:
            html += "<li>" + name + "</li>"
        html += "</ul>"
    html += "</body></html>"
    with open("report.html", "w") as f:
        f.write(html)