import urllib.request
import os

# 巴马瑶族自治县 GeoJSON 数据 (行政区划代码: 451227)
GEOJSON_URL = "https://geo.datav.aliyun.com/areas_v3/bound/451227_full.json"
GEOJSON_PATH = "data/bama.json"

# 同时保留广西省级数据备用
GUANGXI_URL = "https://geo.datav.aliyun.com/areas_v3/bound/450000_full.json"
GUANGXI_PATH = "data/guangxi.json"

if not os.path.exists("data"):
    os.makedirs("data")

for url, path, name in [
    (GEOJSON_URL, GEOJSON_PATH, "巴马县"),
    (GUANGXI_URL, GUANGXI_PATH, "广西省")
]:
    if not os.path.exists(path):
        print(f"Downloading {name} GeoJSON to {path}...")
        try:
            urllib.request.urlretrieve(url, path)
            print("Success.")
        except Exception as e:
            print(f"Failed: {e}")
    else:
        print(f"{name} GeoJSON already exists: {path}")
