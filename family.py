"""Cousin's CrossConnect family roster and card assignment."""

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "family.json"

GROUPS = [
    ("under12", "Under 12", "Bottom of each card — encourage and mentor"),
    ("20s30s", "20s & 30s", "Gets a personal card; chats with the same age group on the right"),
    ("30s40s", "30s & 40s", "Gets a personal card; chats with the same age group on the right"),
    ("50s60s", "50s & 60s", "Gets a personal card; chats with the same age group on the right"),
    ("65plus", "65 & over", "Top of each card — call and check on"),
]

GROUP_LABELS = {key: label for key, label, _ in GROUPS}
GROUP_HELP = {key: help_text for key, _, help_text in GROUPS}

# Which assignment lists a person belongs to, by age group.
GROUP_LISTS = {
    "under12": ["kids_20s", "kids_30s", "kids_50s"],
    "20s30s": ["twenties", "twenties_for_30s"],
    "30s40s": ["thirties", "thirties_for_20s", "thirties_for_50s"],
    "50s60s": ["fifties"],
    "65plus": ["elders_20s", "elders_30s", "elders_50s"],
}

INITIAL = {
    "assignment_year": 2026,
    "site_title": "My Webpage",
    "welcome": "Welcome to Cousin's CrossConnect!",
    "intro": "This is some text on my page.",
    "people": [
        {"name": "Ken", "group": "65plus"},
        {"name": "Etalem", "group": "65plus"},
        {"name": "Solomon", "group": "65plus"},
        {"name": "Vero", "group": "65plus"},
        {"name": "Tony", "group": "65plus"},
        {"name": "Chief", "group": "65plus"},
        {"name": "Hailelul", "group": "65plus"},
        {"name": "Martha", "group": "65plus"},
        {"name": "Joseph", "group": "65plus"},
        {"name": "Loreta", "group": "65plus"},
        {"name": "Senny", "group": "65plus"},
        {"name": "Belle", "group": "65plus"},
        {"name": "Membe", "group": "65plus"},
        {"name": "Abesha", "group": "under12"},
        {"name": "Helah", "group": "under12"},
        {"name": "Kayla", "group": "under12"},
        {"name": "Layla", "group": "under12"},
        {"name": "Soliana", "group": "under12"},
        {"name": "Amanu", "group": "20s30s"},
        {"name": "Danu", "group": "20s30s"},
        {"name": "Maya", "group": "20s30s"},
        {"name": "Abel", "group": "20s30s"},
        {"name": "Natu", "group": "20s30s"},
        {"name": "Bethel", "group": "20s30s"},
        {"name": "Liyu", "group": "20s30s"},
        {"name": "Menna", "group": "20s30s"},
        {"name": "Josh M", "group": "20s30s"},
        {"name": "Faven", "group": "20s30s"},
        {"name": "Hosanna", "group": "20s30s"},
        {"name": "Amara", "group": "20s30s"},
        {"name": "Emu", "group": "20s30s"},
        {"name": "Jano", "group": "20s30s"},
        {"name": "Elias", "group": "30s40s"},
        {"name": "Veronica", "group": "30s40s"},
        {"name": "Eskender", "group": "30s40s"},
        {"name": "Sal", "group": "30s40s"},
        {"name": "Josh A", "group": "30s40s"},
        {"name": "Romeo", "group": "30s40s"},
        {"name": "Kristopher", "group": "30s40s"},
        {"name": "Daweet", "group": "30s40s"},
        {"name": "Nadeen", "group": "30s40s"},
        {"name": "Betu", "group": "30s40s"},
        {"name": "Matti", "group": "30s40s"},
        {"name": "Macki", "group": "30s40s"},
        {"name": "Mickey", "group": "30s40s"},
        {"name": "Neb", "group": "30s40s"},
        {"name": "Mesfin", "group": "50s60s"},
        {"name": "Fubu", "group": "50s60s"},
        {"name": "Zaren", "group": "50s60s"},
        {"name": "Jay", "group": "50s60s"},
        {"name": "Gilu", "group": "50s60s"},
        {"name": "Mimi", "group": "50s60s"},
        {"name": "Tutu", "group": "50s60s"},
        {"name": "Mamiye", "group": "50s60s"},
        {"name": "Sammy", "group": "50s60s"},
        {"name": "Nany", "group": "50s60s"},
        {"name": "Garae", "group": "50s60s"},
    ],
    "lists": {
        "elders_20s": [
            "Ken", "Etalem", "Solomon", "Vero", "Tony", "Chief", "Hailelul",
            "Martha", "Joseph", "Loreta", "Senny", "Belle", "Membe",
        ],
        "thirties_for_20s": [
            "Elias", "Eskender", "Veronica", "Sal", "Josh A", "Romeo", "Daweet",
            "Kristopher", "Betu", "Matti", "Macki", "Nadeen", "Mickey", "Neb",
        ],
        "twenties": [
            "Amanu", "Danu", "Maya", "Abel", "Natu", "Bethel", "Liyu", "Menna",
            "Josh M", "Faven", "Hosanna", "Amara", "Emu", "Jano",
        ],
        "kids_20s": ["Abesha", "Helah", "Kayla", "Layla", "Soliana"],
        "elders_30s": [
            "Membe", "Etalem", "Belle", "Solomon", "Tony", "Chief", "Martha",
            "Vero", "Joseph", "Loreta", "Hailelul", "Senny", "Ken",
        ],
        "thirties": [
            "Elias", "Veronica", "Eskender", "Sal", "Josh A", "Romeo",
            "Kristopher", "Daweet", "Nadeen", "Betu", "Matti", "Macki",
            "Mickey", "Neb",
        ],
        "twenties_for_30s": [
            "Amanu", "Maya", "Liyu", "Bethel", "Abel", "Faven", "Josh M",
            "Amara", "Hosanna", "Emu", "Danu", "Menna", "Jano", "Natu",
        ],
        "kids_30s": ["Abesha", "Helah", "Kayla", "Layla", "Soliana"],
        "elders_50s": [
            "Hailelul", "Etalem", "Solomon", "Belle", "Tony", "Martha", "Chief",
            "Ken", "Joseph", "Loreta", "Vero", "Senny", "Membe",
        ],
        "thirties_for_50s": [
            "Mickey", "Elias", "Eskender", "Sal", "Josh A", "Romeo", "Daweet",
            "Kristopher", "Matti", "Betu", "Macki", "Veronica", "Neb", "Nadeen",
        ],
        "fifties": [
            "Mesfin", "Fubu", "Zaren", "Jay", "Gilu", "Mimi", "Tutu",
            "Mamiye", "Sammy", "Nany", "Garae",
        ],
        "kids_50s": ["Layla", "Soliana", "Kayla", "Helah", "Abesha"],
    },
}


def _copy(data):
    return json.loads(json.dumps(data))


def load_data():
    if not DATA_PATH.exists():
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        save_data(_copy(INITIAL))
    with DATA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_data(data):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = DATA_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(DATA_PATH)


def people_in_group(data, group):
    return [person["name"] for person in data["people"] if person["group"] == group]


def find_person(data, name):
    name_key = name.strip().casefold()
    for person in data["people"]:
        if person["name"].casefold() == name_key:
            return person
    return None


def group_counts(data):
    counts = {key: 0 for key, _, _ in GROUPS}
    for person in data["people"]:
        counts[person["group"]] = counts.get(person["group"], 0) + 1
    return counts


def _remove_from_lists(data, name):
    for names in data["lists"].values():
        while name in names:
            names.remove(name)


def _add_to_group_lists(data, name, group):
    for list_name in GROUP_LISTS[group]:
        names = data["lists"].setdefault(list_name, [])
        if name not in names:
            names.append(name)


def add_person(name, group):
    name = " ".join(name.split())
    if not name:
        raise ValueError("Name is required.")
    if group not in GROUP_LISTS:
        raise ValueError("Choose a valid age group.")
    data = load_data()
    if find_person(data, name):
        raise ValueError(f"{name} is already in the family list.")
    data["people"].append({"name": name, "group": group})
    _add_to_group_lists(data, name, group)
    save_data(data)
    return name


def remove_person(name):
    data = load_data()
    person = find_person(data, name)
    if person is None:
        raise ValueError(f"{name} was not found.")
    data["people"] = [item for item in data["people"] if item["name"] != person["name"]]
    _remove_from_lists(data, person["name"])
    save_data(data)
    return person["name"]


def move_person(name, new_group):
    if new_group not in GROUP_LISTS:
        raise ValueError("Choose a valid age group.")
    data = load_data()
    person = find_person(data, name)
    if person is None:
        raise ValueError(f"{name} was not found.")
    if person["group"] == new_group:
        return person["name"]
    _remove_from_lists(data, person["name"])
    person["group"] = new_group
    _add_to_group_lists(data, person["name"], new_group)
    save_data(data)
    return person["name"]


def rename_person(old_name, new_name):
    new_name = " ".join(new_name.split())
    if not new_name:
        raise ValueError("New name is required.")
    data = load_data()
    person = find_person(data, old_name)
    if person is None:
        raise ValueError(f"{old_name} was not found.")
    other = find_person(data, new_name)
    if other and other["name"] != person["name"]:
        raise ValueError(f"{new_name} is already in the family list.")
    old = person["name"]
    person["name"] = new_name
    for names in data["lists"].values():
        for index, value in enumerate(names):
            if value == old:
                names[index] = new_name
    save_data(data)
    return new_name


def update_settings(welcome, intro, site_title):
    data = load_data()
    data["welcome"] = welcome.strip() or data["welcome"]
    data["intro"] = intro.strip()
    data["site_title"] = site_title.strip() or data["site_title"]
    save_data(data)


def new_year():
    """Reshuffle pairings and bump the assignment year."""
    data = load_data()
    rng = random.Random()
    for names in data["lists"].values():
        rng.shuffle(names)
    data["assignment_year"] = int(data.get("assignment_year", 2026)) + 1
    save_data(data)
    return data["assignment_year"]


def format_value(value):
    if value in [1, 3, 7, 9] or value in (None, ""):
        return ""
    return str(value).center(12)


def _pick(names, index):
    if not names:
        return ""
    return names[index % len(names)]


def make_cards(centers, right_group, left_group, elders, kids):
    grids = []
    for i, name in enumerate(centers):
        grid = [[1, 2, 3], [4, name, None], [7, 8, 9]]
        grid[1][2] = _pick(right_group, i + 1)
        grid[1][0] = _pick(left_group, i)
        grid[2][1] = _pick(kids, i)
        grid[0][1] = _pick(elders, i)
        grids.append([[format_value(value) for value in row] for row in grid])
    return grids


def build_grids(data=None):
    if data is None:
        data = load_data()
    lists = data["lists"]
    grids = []
    grids.extend(
        make_cards(
            lists.get("twenties", []),
            lists.get("twenties", []),
            lists.get("thirties_for_20s", []),
            lists.get("elders_20s", []),
            lists.get("kids_20s", []),
        )
    )
    grids.extend(
        make_cards(
            lists.get("thirties", []),
            lists.get("thirties", []),
            lists.get("twenties_for_30s", []),
            lists.get("elders_30s", []),
            lists.get("kids_30s", []),
        )
    )
    grids.extend(
        make_cards(
            lists.get("fifties", []),
            lists.get("fifties", []),
            lists.get("thirties_for_50s", []),
            lists.get("elders_50s", []),
            lists.get("kids_50s", []),
        )
    )
    return grids


def grouped_people(data=None):
    if data is None:
        data = load_data()
    grouped = {key: [] for key, _, _ in GROUPS}
    for person in data["people"]:
        grouped.setdefault(person["group"], []).append(person)
    for names in grouped.values():
        names.sort(key=lambda item: item["name"].casefold())
    return grouped
