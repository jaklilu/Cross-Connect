# Cousin's CrossConnect — project context

Last updated: 18 August 2026

This file is the running memory for the project: why it exists, how the original PythonAnywhere app worked, what was rebuilt for Netlify, and how to manage people and yearly pairings.

## Purpose

CrossConnect is a family connection app. Each person who is not a young child and not 65+ gets a plus-shaped card:

| | **Top: 65 & over** Call and check on them (Appreciate) | |
|---|---|---|
| **Left: neighboring adult group** Share / chat | **You** | **Right: same age group** Share / chat |
| | **Bottom: under 12** Encourage and mentor (Love) | |

Public tooltip text on the personal card page:

- The person on top, Appreciate them!
- The person on the bottom, Love them!
- The person on each side, Share something with them!

Colors (keep these on the public pages):

- Page background: **black**
- Heading: **green**
- Middle column (top / you / bottom): **green**
- Middle row (left / you / right): **yellow**
- Center cell (you): **red**, bold

Original live site (still on PythonAnywhere until shut down): [https://jaklilu.pythonanywhere.com/](https://jaklilu.pythonanywhere.com/)

## Age groups

There are five groups. Names are stored without last names, as the family uses them.

| Group key | Label | Count (2026 roster) | Role |
|---|---|---|---|
| `under12` | Under 12 | 5 | Bottom of every card only. No personal card. |
| `20s30s` | 20s & 30s | 14 | Gets a personal card. |
| `30s40s` | 30s & 40s | 14 | Gets a personal card. |
| `50s60s` | 50s & 60s | 11 | Gets a personal card. |
| `65plus` | 65 & over | 13 | Top of every card only. No personal card. |

**57 people total. 39 personal cards.** Kids and elders never sit in the center.

The owner's original memory was kids / 20s / 30s / 40s / 50s / 60s. The code that actually ran used the five groups above (20s&30s combined, 30s&40s combined, 50s&60s combined, then 65+).

## How a card is built (assignment logic)

Recovered from `CrossConnectAll_V2.py` on PythonAnywhere.

For each card-holder group (20s&30s, then 30s&40s, then 50s&60s):

- **Center:** that person
- **Right:** the next person in the **same** group (list wraps in a circle)
- **Left:** a person from the **neighboring** adult group, same index (modulo)
  - 20s&30s cards: left is 30s&40s
  - 30s&40s cards: left is 20s&30s
  - 50s&60s cards: left is 30s&40s
- **Top:** next name in the 65+ list (cycled; each card-holder section has its own order of the same 13 elders)
- **Bottom:** next name in the under-12 list (cycled; each section has its own kid order)

There is no login or public “new year” button on the family site. A new year originally meant reordering the name lists by hand and reloading Flask. The admin page now does that with a shuffle.

Empty corner cells stay empty (the old code blanked grid spots 1, 3, 7, and 9).

## What happened in this work

### 1. Inspected the live PythonAnywhere site

- Public routes are `/` (all 39 cards) and `/grid/0` … `/grid/38` (one zoomed card).
- No public admin, assign, or yearly-refresh URL.
- `/static/` was accidentally serving Jinja templates (`index.html`, `grid.html`, plus leftover `index2.html` / `index3.html` / `grid2.html` / `grid3.html`).
- The Python assignment file was **not** on the public site.

### 2. Found the original source on this PC

The Cross-Connect workspace started empty. The Flask source was already in **Downloads**, then copied into `Copied from PythonAnywhere/`:

- `CrossConnectAll_V2.py` — the combined app that matches the live site
- `CrossConnect20s30sFlaskV4.py`, `CrossConnet30s40sFlaskV4.py` (typo in filename), `CrossConnect50s60sFlaskV4.py` — older split apps
- Templates: `index (1).html` (live home), `grid.html` (live card), plus older index2/3 and grid2/3
- `requirements.txt` from PythonAnywhere is a full environment dump (Flask plus unrelated packages). CrossConnect only needs Flask.

### 3. Rebuilt the app for Netlify

PythonAnywhere runs Flask. Netlify hosts static files. The family site is generated as HTML in `site/` and can be deployed to Netlify. Flask still runs locally for preview and admin.

Public look matches the original index/grid colors and copy.

### 4. GitHub

Repo: [https://github.com/jaklilu/Cross-Connect](https://github.com/jaklilu/Cross-Connect)

- Initialized local git, committed, pushed `main`.
- Then **removed** `Copied from PythonAnywhere/` from GitHub. It remains on disk as a local backup and is gitignored. The running app does not use that folder.

### 5. Admin

Password-protected Flask admin at `/admin` to add/remove people, change age group, rename, start a new year (reshuffle), edit page text, and rebuild the Netlify `site/` folder.

Admin is **not** included in the static Netlify site, so the public family site cannot change the roster.

## Current architecture

```
Local Flask (http://127.0.0.1:8000)
  ├── / and /grid/<n>     family site (same colors as original)
  └── /admin              manage roster, ages, yearly refresh

data/family.json          source of truth (people, groups, list orders, page text)
family.py                 load/save JSON, build 3x3 cards, add/remove/move/year
app.py                    Flask routes
templates/                index.html, grid.html, admin.html, admin_login.html
build_static.py           writes site/index.html and site/grid/0.html … 38.html
site/                     Netlify publish folder
netlify.toml              publish = site; /grid/:index → /grid/:index.html
```

Yearly refresh and roster edits update `data/family.json` and rebuild `site/`. The local Flask site updates immediately. The public Netlify site updates only after a git push (or a manual deploy of `site/`).

## Key files

| Path | Role |
|---|---|
| `app.py` | Flask app: public pages + admin |
| `family.py` | Assignment logic and roster operations |
| `data/family.json` | Current people, age groups, shuffled list orders, welcome text |
| `templates/index.html` | Home: all cards, original colors |
| `templates/grid.html` | Personal card + tooltip |
| `templates/admin.html` | Management dashboard |
| `templates/admin_login.html` | Admin password page |
| `build_static.py` | Generate Netlify files; deletes leftover grid HTML if the card count shrinks |
| `site/` | Static output for Netlify |
| `netlify.toml` | Publish directory and grid URL redirects |
| `requirements.txt` | Flask, Jinja2, Werkzeug only |
| `.env` | `ADMIN_PASSWORD` and `SECRET_KEY` (gitignored) |
| `Copied from PythonAnywhere/` | Local backup of original files (not on GitHub, not used at runtime) |

## Local run

Flask should stay running:

```
python app.py
```

- Family site: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Admin: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

Default admin password (change in `.env`): `familyadmin`

Rebuild static files without the admin UI:

```
python build_static.py
```

## Netlify deploy

1. Manage people locally in admin (optional).
2. Confirm `site/` was rebuilt (admin does this after each change).
3. Push `main` to GitHub, **or** drag the `site` folder onto Netlify (Deploy manually).

`netlify.toml` already sets `publish = "site"`. Connecting the GitHub repo in Netlify is the long-term path.

Do not deploy Flask to Netlify. Do not put `/admin` in the static site.

## Admin operations (what each button does)

- **Add person:** appends to `people` and to the assignment lists for that age group.
- **Save age:** moves the person to another group (updates all related lists). Use this when someone ages into 20s, 30s/40s, 50s/60s, or 65+.
- **Rename:** changes the name everywhere it appears in lists.
- **Remove:** deletes the person from the roster and all lists.
- **Refresh pairings for next year:** shuffles every assignment list and increments `assignment_year`. Do this after ages are corrected.
- **Save text:** welcome heading, intro line, browser title.
- **Rebuild Netlify files:** regenerates `site/` without changing people.

Duplicate names are rejected (case-insensitive).

## 2026 roster snapshot (from the live site / All_V2)

**65 & over:** Ken, Etalem, Solomon, Vero, Tony, Chief, Hailelul, Martha, Joseph, Loreta, Senny, Belle, Membe

**Under 12:** Abesha, Helah, Kayla, Layla, Soliana

**20s & 30s:** Amanu, Danu, Maya, Abel, Natu, Bethel, Liyu, Menna, Josh M, Faven, Hosanna, Amara, Emu, Jano

**30s & 40s:** Elias, Veronica, Eskender, Sal, Josh A, Romeo, Kristopher, Daweet, Nadeen, Betu, Matti, Macki, Mickey, Neb

**50s & 60s:** Mesfin, Fubu, Zaren, Jay, Gilu, Mimi, Tutu, Mamiye, Sammy, Nany, Garae

The 2026 **list orders** (who is next to whom) are stored in `data/family.json` under `lists`. They match the live PythonAnywhere assignment until someone clicks “new year.”

## Git notes

- Remote: `https://github.com/jaklilu/Cross-Connect.git`
- Branch: `main`
- Ignored: `.env`, `Copied from PythonAnywhere/`, `__pycache__/`, `data/*.tmp`
- `data/family.json` **should** be committed so pairings and roster survive and Netlify builds from the same source after `build_static.py`.

As of this writing, admin + `family.json` may still be local-only if they have not been pushed yet. Push when the family site on Netlify should include the latest roster and when others need this context.

## What is intentionally not in this project

- No database. Roster is JSON. Writes are atomic (temp file then replace).
- No public accounts or family login.
- No automatic calendar-year shuffle. A new year is an admin action so pairings stay stable until someone chooses to refresh.
- The old PythonAnywhere `requirements.txt` packages (PayPal, Twilio, Pulumi, Azure, etc.) are unrelated and were not carried into the new `requirements.txt`.

## Next steps (when returning to this project)

1. Confirm Flask is running on port 8000.
2. Use `/admin` to correct ages before the family starts using cards.
3. Deploy `site/` to Netlify (GitHub connect or drag-and-drop).
4. After Netlify is verified, the PythonAnywhere site can be shut down.
5. Each year: update ages in admin, then click the new-year reshuffle, then push to GitHub.
