"""Cousin's CrossConnect assignment logic (from CrossConnectAll_V2.py)."""

from datetime import datetime

BASE_YEAR = 2026

# 65&over — order used for 20s/30s cards
ELDERS_20S = [
    "Ken",
    "Etalem",
    "Solomon",
    "Vero",
    "Tony",
    "Chief",
    "Hailelul",
    "Martha",
    "Joseph",
    "Loreta",
    "Senny",
    "Belle",
    "Membe",
]

# 30s&40s — left side of 20s/30s cards
THIRTIES_FOR_20S = [
    "Elias",
    "Eskender",
    "Veronica",
    "Sal",
    "Josh A",
    "Romeo",
    "Daweet",
    "Kristopher",
    "Betu",
    "Matti",
    "Macki",
    "Nadeen",
    "Mickey",
    "Neb",
]

# 20s&30s — card holders
TWENTIES = [
    "Amanu",
    "Danu",
    "Maya",
    "Abel",
    "Natu",
    "Bethel",
    "Liyu",
    "Menna",
    "Josh M",
    "Faven",
    "Hosanna",
    "Amara",
    "Emu",
    "Jano",
]

# under12 — bottom of 20s/30s cards
KIDS_20S = ["Abesha", "Helah", "Kayla", "Layla", "Soliana"]

# 65&over — order used for 30s/40s cards
ELDERS_30S = [
    "Membe",
    "Etalem",
    "Belle",
    "Solomon",
    "Tony",
    "Chief",
    "Martha",
    "Vero",
    "Joseph",
    "Loreta",
    "Hailelul",
    "Senny",
    "Ken",
]

# 30s&40s — card holders
THIRTIES = [
    "Elias",
    "Veronica",
    "Eskender",
    "Sal",
    "Josh A",
    "Romeo",
    "Kristopher",
    "Daweet",
    "Nadeen",
    "Betu",
    "Matti",
    "Macki",
    "Mickey",
    "Neb",
]

# 20s&30s — left side of 30s/40s cards
TWENTIES_FOR_30S = [
    "Amanu",
    "Maya",
    "Liyu",
    "Bethel",
    "Abel",
    "Faven",
    "Josh M",
    "Amara",
    "Hosanna",
    "Emu",
    "Danu",
    "Menna",
    "Jano",
    "Natu",
]

# under12 — bottom of 30s/40s cards
KIDS_30S = ["Abesha", "Helah", "Kayla", "Layla", "Soliana"]

# 65&over — order used for 50s/60s cards
ELDERS_50S = [
    "Hailelul",
    "Etalem",
    "Solomon",
    "Belle",
    "Tony",
    "Martha",
    "Chief",
    "Ken",
    "Joseph",
    "Loreta",
    "Vero",
    "Senny",
    "Membe",
]

# 30s&40s — left side of 50s/60s cards
THIRTIES_FOR_50S = [
    "Mickey",
    "Elias",
    "Eskender",
    "Sal",
    "Josh A",
    "Romeo",
    "Daweet",
    "Kristopher",
    "Matti",
    "Betu",
    "Macki",
    "Veronica",
    "Neb",
    "Nadeen",
]

# 50s&60s — card holders
FIFTIES = [
    "Mesfin",
    "Fubu",
    "Zaren",
    "Jay",
    "Gilu",
    "Mimi",
    "Tutu",
    "Mamiye",
    "Sammy",
    "Nany",
    "Garae",
]

# under12 — bottom of 50s/60s cards
KIDS_50S = ["Layla", "Soliana", "Kayla", "Helah", "Abesha"]


def rotate(names, year):
    """Keep 2026 lists as-is; each later year shifts the list by one."""
    names = list(names)
    if not names or year <= BASE_YEAR:
        return names
    offset = (year - BASE_YEAR) % len(names)
    return names[offset:] + names[:offset]


def format_value(value):
    if value in [1, 3, 7, 9]:
        return ""
    return str(value).center(12)


def make_cards(centers, right_group, left_group, elders, kids):
    grids = []
    for i, name in enumerate(centers):
        grid = [[1, 2, 3], [4, name, None], [7, 8, 9]]
        grid[1][2] = right_group[(i + 1) % len(right_group)]
        grid[1][0] = left_group[i % len(left_group)]
        grid[2][1] = kids[i % len(kids)]
        grid[0][1] = elders[i % len(elders)]
        grids.append([[format_value(value) for value in row] for row in grid])
    return grids


def build_grids(year=None):
    if year is None:
        year = datetime.now().year

    twenties = rotate(TWENTIES, year)
    thirties_for_20s = rotate(THIRTIES_FOR_20S, year)
    elders_20s = rotate(ELDERS_20S, year)
    kids_20s = rotate(KIDS_20S, year)

    thirties = rotate(THIRTIES, year)
    twenties_for_30s = rotate(TWENTIES_FOR_30S, year)
    elders_30s = rotate(ELDERS_30S, year)
    kids_30s = rotate(KIDS_30S, year)

    fifties = rotate(FIFTIES, year)
    thirties_for_50s = rotate(THIRTIES_FOR_50S, year)
    elders_50s = rotate(ELDERS_50S, year)
    kids_50s = rotate(KIDS_50S, year)

    grids = []
    # Center = 20s/30s, right = next same group, left = 30s/40s
    grids.extend(make_cards(twenties, twenties, thirties_for_20s, elders_20s, kids_20s))
    # Center = 30s/40s, right = next same group, left = 20s/30s
    grids.extend(make_cards(thirties, thirties, twenties_for_30s, elders_30s, kids_30s))
    # Center = 50s/60s, right = next same group, left = 30s/40s
    grids.extend(make_cards(fifties, fifties, thirties_for_50s, elders_50s, kids_50s))
    return grids
