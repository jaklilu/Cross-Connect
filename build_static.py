"""Prepare the Netlify site folder."""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DATA_SRC = ROOT / "data" / "family.json"
DATA_DST = SITE / "data" / "family.json"


def main():
    SITE.mkdir(exist_ok=True)
    DATA_DST.parent.mkdir(exist_ok=True)
    shutil.copy2(DATA_SRC, DATA_DST)

    # Remove old pre-rendered grid pages; the live site uses grid.html + JS now.
    grid_dir = SITE / "grid"
    if grid_dir.exists():
        shutil.rmtree(grid_dir)

    print(f"Synced family data to {DATA_DST}")


if __name__ == "__main__":
    main()
