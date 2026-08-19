"""Render the Flask templates into a static Netlify site/ folder."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from family import build_grids, load_data

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
TEMPLATES = ROOT / "templates"


def main():
    data = load_data()
    grids = build_grids(data)
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)
    index_tmpl = env.get_template("index.html")
    grid_tmpl = env.get_template("grid.html")

    SITE.mkdir(exist_ok=True)
    grid_dir = SITE / "grid"
    grid_dir.mkdir(exist_ok=True)

    (SITE / "index.html").write_text(
        index_tmpl.render(
            grids=grids,
            welcome=data.get("welcome", "Welcome to Cousin's CrossConnect!"),
            intro=data.get("intro", "This is some text on my page."),
            site_title=data.get("site_title", "My Webpage"),
            assignment_year=data.get("assignment_year", 2026),
        ),
        encoding="utf-8",
    )

    written = set()
    for index, card in enumerate(grids):
        html = grid_tmpl.render(
            grid=card,
            grid_id=index + 1,
            formatted_grid="\n".join(["".join(row) for row in card]),
        )
        path = grid_dir / f"{index}.html"
        path.write_text(html, encoding="utf-8")
        written.add(path)

    for stale in grid_dir.glob("*.html"):
        if stale not in written:
            stale.unlink()

    (SITE / "_redirects").write_text(
        "/grid/:index /grid/:index.html 200\n", encoding="utf-8"
    )
    print(f"Wrote {len(grids)} grid pages to {SITE}")


if __name__ == "__main__":
    main()
