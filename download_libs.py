import urllib.request
import os

libs = [
    ("https://unpkg.com/leaflet@1.9.4/dist/leaflet.js", "lib/leaflet.js"),
    ("https://unpkg.com/leaflet@1.9.4/dist/leaflet.css", "lib/leaflet.css"),
    ("https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png", "lib/images/marker-icon.png"),
    ("https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png", "lib/images/marker-icon-2x.png"),
    ("https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png", "lib/images/marker-shadow.png"),
    ("https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js", "lib/echarts.min.js")
]

if not os.path.exists("lib"):
    os.makedirs("lib")
if not os.path.exists("lib/images"):
    os.makedirs("lib/images")

for url, path in libs:
    print(f"Downloading {url} to {path}...")
    try:
        urllib.request.urlretrieve(url, path)
        print("Success.")
    except Exception as e:
        print(f"Failed: {e}")
