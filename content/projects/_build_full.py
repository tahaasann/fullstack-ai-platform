# -*- coding: utf-8 -*-
"""Build complete project-08.json"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "project-08.json")

# Load full data from separate JSON parts
exec(open(os.path.join(BASE, "_p08_data.py"), encoding="utf-8").read())

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(PROJECT_DATA, f, ensure_ascii=False, indent=2)

size = os.path.getsize(OUT)
print(f"Written {size} bytes ({size/1024:.1f} KB)")
