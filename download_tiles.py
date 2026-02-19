import os
import math
import urllib.request
import time
import random
import sys

# ============================================
# 巴马县区域暗色瓦片下载器
# CartoDB Dark Matter (No Labels)
# ============================================

# 巴马县边界范围 (大幅扩大确保全屏覆盖)
MIN_LAT = 23.40
MAX_LAT = 24.80
MIN_LNG = 106.30
MAX_LNG = 108.10

# 下载层级
ZOOM_LEVELS = [10, 11, 12, 13]

TILE_DIR = "assets/tiles"
# Voyager No Labels - 纹理清晰，通过CSS滤镜调暗
TILE_URL = "https://basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}.png"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def download_tile(z, x, y):
    url = TILE_URL.format(z=z, x=x, y=y)
    dir_path = os.path.join(TILE_DIR, str(z), str(x))
    file_path = os.path.join(dir_path, f"{y}.png")
    
    if os.path.exists(file_path):
        return 'skip'
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as response:
            with open(file_path, 'wb') as f:
                f.write(response.read())
        return 'ok'
    except Exception as e:
        return 'fail'

def main():
    print("=" * 50)
    print("  巴马县 暗色瓦片下载器")
    print(f"  层级: {ZOOM_LEVELS}")
    print("=" * 50)
    
    if not os.path.exists(TILE_DIR):
        os.makedirs(TILE_DIR)
    
    total = 0
    dl = 0
    skip = 0
    fail = 0
    
    for z in ZOOM_LEVELS:
        min_x, min_y = deg2num(MAX_LAT, MIN_LNG, z)
        max_x, max_y = deg2num(MIN_LAT, MAX_LNG, z)
        total += (max_x - min_x + 1) * (max_y - min_y + 1)
    
    print(f"\n  总计: {total} 张瓦片\n")
    
    cur = 0
    for z in ZOOM_LEVELS:
        min_x, min_y = deg2num(MAX_LAT, MIN_LNG, z)
        max_x, max_y = deg2num(MIN_LAT, MAX_LNG, z)
        cnt = (max_x - min_x + 1) * (max_y - min_y + 1)
        print(f"  Zoom {z}: {cnt} tiles")
        
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                cur += 1
                pct = cur / total * 100
                sys.stdout.write(f"\r  [{cur}/{total}] {pct:.0f}% dl:{dl} skip:{skip}")
                sys.stdout.flush()
                
                r = download_tile(z, x, y)
                if r == 'ok':
                    dl += 1
                    time.sleep(random.uniform(0.03, 0.1))
                elif r == 'skip':
                    skip += 1
                else:
                    fail += 1
        print()
    
    print(f"\n  完成! 下载:{dl} 跳过:{skip} 失败:{fail}")

if __name__ == "__main__":
    main()
