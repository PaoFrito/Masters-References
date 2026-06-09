from pathlib import Path
import xml.etree.ElementTree as ET
from html import escape

xml_path = "./references.xml"
html_path = "./references.html"

tree = ET.parse(xml_path)
root = tree.getroot()

records = root.findall(".//record")

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Readable Library</title>
<style>
body{font-family:Arial,sans-serif;background:#f5f5f5;margin:20px}
.card{background:white;border-radius:10px;padding:16px;margin:12px 0;box-shadow:0 1px 4px rgba(0,0,0,.15)}
h2{margin:0 0 8px 0}
.meta{color:#555;font-size:14px;margin-bottom:8px}
details{margin-top:8px}
.abstract{line-height:1.5}
.authors{font-weight:bold}
</style>
</head><body>
<h1>Library References</h1>
<p>Total records: %d</p>
""" % len(records)

for rec in records:
    title = (rec.findtext("./titles/title") or "Untitled").strip()
    year = (rec.findtext("./dates/year") or "").strip()
    rtype = rec.find("./ref-type")
    rtype = rtype.get("name") if rtype is not None else ""

    authors = []
    for a in rec.findall("./contributors/authors/author"):
        t = " ".join(a.text.split()) if a.text else ""
        if t:
            authors.append(t)

    abstract = rec.findtext("./abstract") or ""
    doi = rec.findtext("./electronic-resource-num") or ""
    keywords = [k.text.strip() for k in rec.findall("./keywords/keyword") if k.text]

    html += f"""
    <div class="card">
      <h2>{escape(title)}</h2>
      <div class="meta">{escape(rtype)} {'• ' + escape(year) if year else ''}</div>
      <div class="authors">{escape(', '.join(authors))}</div>
    """

    if doi:
        html += f"<p><strong>DOI:</strong> {escape(doi)}</p>"

    if keywords:
        html += f"<p><strong>Keywords:</strong> {escape(', '.join(keywords))}</p>"

    if abstract.strip():
        html += f"""
        <details>
          <summary>Abstract</summary>
          <div class="abstract">{escape(abstract)}</div>
        </details>
        """

    html += "</div>"

html += "</body></html>"

Path(html_path).write_text(html, encoding="utf-8")

print(html_path)