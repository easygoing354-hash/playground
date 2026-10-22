"""Bundle the web app into one self-contained HTML file:  python3 single_file.py <app dir> <out.html>"""
import base64
import os
import re
import sys

app, out = sys.argv[1], sys.argv[2]
read = lambda n: open(os.path.join(app, n), encoding="utf-8").read()
html = read("index.html")
for js in ("art.js", "app.js", "voice.js"):
    assert "</script" not in read(js).lower()
icon = base64.b64encode(open(os.path.join(app, "icon-192.png"), "rb").read()).decode()
html = html.replace('  <link rel="manifest" href="manifest.webmanifest">\n', "")
html = html.replace('<link rel="icon" href="icon-192.png">', f'<link rel="icon" href="data:image/png;base64,{icon}">')
html = html.replace('  <link rel="apple-touch-icon" href="apple-touch-icon.png">\n', "")
html = html.replace('<link rel="stylesheet" href="fonts.css">', "<style>\n" + read("fonts.css") + "</style>")
html = html.replace('<link rel="stylesheet" href="styles.css">', "<style>\n" + read("styles.css") + "</style>")
html = html.replace('<script src="art.js"></script>', "<script>\n" + read("art.js") + "</script>")
html = html.replace('<script src="app.js"></script>', "<script>\n" + read("app.js") + "</script>")
html = html.replace('<script src="voice.js" async></script>', "<script>\n" + read("voice.js") + "</script>")
html = re.sub(r"\s*<script>\s*if \('serviceWorker'.*?</script>", "", html, flags=re.S)
assert 'src="' not in html and 'href="fonts' not in html and "serviceWorker" not in html
open(out, "w", encoding="utf-8").write(html)
print(out, os.path.getsize(out) // 1024, "KB")
