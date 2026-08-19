# Cousin's CrossConnect — project context

Last updated: 19 August 2026

This file is the running memory for the project: why it exists, how the original PythonAnywhere app worked, what was rebuilt for Netlify, and how to manage people and pairings.

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

Original PythonAnywhere site (can be shut down once Netlify is verified): [https://jaklilu.pythonanywhere.com/](https://jaklilu.pythonanywhere.com/)

GitHub repo: [https://github.com/jaklilu/Cross-Connect](https://github.com/jaklilu/Cross-Connect)

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
- **Top:** elder at same index in the 65+ list for that section
- **Bottom:** kid at same index in the under-12 list for that section

Empty corner cells stay empty (grid spots 1, 3, 7, and 9).

### Yearly rotation (not random)

Pairings do **not** shuffle randomly. Name lists stay in a fixed order. Each time you click **Refresh Pairing**, the app:

1. Increments `assignment_year` (used internally for rotation math)
2. Records `last_refreshed` (today's date, shown in admin)

The rotation offset is `assignment_year - 2026`. Each refresh shifts left, right, top, and bottom partners by one step:

- **2026** → offset 0 (starting pairings)
- **2027** → offset 1 (everyone gets new partners)
- **2028** → offset 2, and so on

Over a full cycle, each person connects with everyone in their group. No partner repeats from the year before.

Example for Amanu:

- Before refresh: Ken (top), Elias (left), Danu (right), Abesha (bottom)
- After one refresh: Etalem, Eskender, Maya, Helah — all different

## What happened in this work

### 1. Inspected the live PythonAnywhere site

- Public routes were `/` (all cards) and `/grid/0` … `/grid/38`.
- No public admin URL. Assignment logic lived in Python only.
- `/static/` accidentally exposed Jinja templates.

### 2. Found the original source on this PC

Flask source was in **Downloads**, copied locally to `Copied from PythonAnywhere/` (gitignored backup). The live app matched `CrossConnectAll_V2.py`.

### 3. Rebuilt for Netlify

- Public site lives in `site/` and deploys to Netlify.
- Pages load roster data from JSON and render cards with JavaScript (same colors as original).
- Flask still runs locally at port 8000 for optional local preview.

### 4. GitHub

Repo: [https://github.com/jaklilu/Cross-Connect](https://github.com/jaklilu/Cross-Connect)

`Copied from PythonAnywhere/` is kept on disk only — not on GitHub.

### 5. Live admin on Netlify

- Yellow **Admin** button on the home page → `/admin.html`
- Password-protected login (Netlify Functions + Netlify Blobs for saved data)
- Same features as local Flask admin: add/remove, fix ages, rename, refresh pairings, edit page text
- Enter key submits the login form

## Current architecture

```
Netlify (live — what the family uses)
  ├── /                     home page (JS renders all cards)
  ├── /grid.html?index=N    one personal card
  ├── /admin.html           admin dashboard
  ├── /data/family.json     fallback roster (from git)
  └── /.netlify/functions/
        family.mjs          GET roster / PUT saved roster (auth required)
        login.mjs           verify admin password

Local Flask (optional — http://127.0.0.1:8000)
  ├── / and /grid/<n>       server-rendered family site
  └── /admin                same admin features, writes data/family.json

data/family.json            source of truth in git (people, lists, page text, dates)
family.py                   Python: load/save, build cards, roster ops, rotation
site/js/family.js           JavaScript: same logic for Netlify
build_static.py             copies data/family.json → site/data/family.json
netlify.toml                publish = site; npm install + build on deploy
```

On Netlify, admin saves go to **Netlify Blobs** (live data). If no blob exists yet, the site reads `site/data/family.json` from the deploy.

## Key files

| Path | Role |
|---|---|
| `site/index.html` | Live home page + Admin button |
| `site/grid.html` | Live personal card page |
| `site/admin.html` | Live admin login + dashboard |
| `site/js/family.js` | Card logic, rotation, roster operations (JS) |
| `site/js/api.js` | Fetch/save family data via Netlify Functions |
| `site/js/admin.js` | Live admin UI |
| `site/data/family.json` | Roster bundled with each deploy |
| `netlify/functions/family.mjs` | API: read/write roster (password on write) |
| `netlify/functions/login.mjs` | API: verify admin password |
| `data/family.json` | Master roster in git |
| `family.py` | Same logic in Python for Flask |
| `app.py` | Local Flask app |
| `templates/` | Flask HTML templates (local dev) |
| `build_static.py` | Syncs `data/family.json` into `site/data/` |
| `netlify.toml` | Netlify build and redirect config |
| `package.json` | Netlify Functions dependency (`@netlify/blobs`) |
| `.env` | Local `ADMIN_PASSWORD` and `SECRET_KEY` (gitignored) |
| `Copied from PythonAnywhere/` | Local backup only (gitignored) |

## URLs

| Where | Family site | Admin |
|---|---|---|
| **Netlify (live)** | `https://YOUR-SITE.netlify.app/` | `https://YOUR-SITE.netlify.app/admin.html` |
| **Local Flask** | [http://127.0.0.1:8000](http://127.0.0.1:8000) | [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) |

Grid links: `/grid.html?index=0` (also `/grid/0` redirects on Netlify).

## Admin password

Default: **`CrossConnect2026`**

- **Local:** set in `.env` as `ADMIN_PASSWORD`
- **Netlify:** set the same in **Site configuration → Environment variables** as `ADMIN_PASSWORD`, then redeploy

## Admin operations

- **Add person:** adds to `people` and the assignment lists for that age group.
- **Save age:** moves person to another group (updates all related lists).
- **Rename:** updates name everywhere in lists.
- **Remove:** deletes person from roster and all lists.
- **Refresh Pairing:** rotates everyone to new partners; saves `last_refreshed` date. Button always says "Refresh Pairing" (no year in the label). Admin shows **Last refreshed** so you know when pairings were last changed.
- **Save text:** welcome heading, intro line, browser title.

Duplicate names are rejected (case-insensitive).

## Recommended yearly workflow

1. Open admin (live Netlify admin or local Flask).
2. Fix ages — move people who aged into a new group.
3. Click **Refresh Pairing**.
4. Check **Last refreshed** date and skim a few cards on the family site.
5. If using local Flask, run `python build_static.py` and push to git so the fallback JSON matches.

## Local run (optional)

```
python app.py
```

Flask serves at [http://127.0.0.1:8000](http://127.0.0.1:8000). Sync JSON to site folder:

```
python build_static.py
```

## Netlify deploy

1. Connect GitHub repo to Netlify (or drag `site/` folder).
2. Set `ADMIN_PASSWORD` in Netlify environment variables.
3. Push to `main` — Netlify runs `npm install && python build_static.py` then publishes `site/`.

## 2026 roster snapshot

**65 & over:** Ken, Etalem, Solomon, Vero, Tony, Chief, Hailelul, Martha, Joseph, Loreta, Senny, Belle, Membe

**Under 12:** Abesha, Helah, Kayla, Layla, Soliana

**20s & 30s:** Amanu, Danu, Maya, Abel, Natu, Bethel, Liyu, Menna, Josh M, Faven, Hosanna, Amara, Emu, Jano

**30s & 40s:** Elias, Veronica, Eskender, Sal, Josh A, Romeo, Kristopher, Daweet, Nadeen, Betu, Matti, Macki, Mickey, Neb

**50s & 60s:** Mesfin, Fubu, Zaren, Jay, Gilu, Mimi, Tutu, Mamiye, Sammy, Nany, Garae

List orders are in `data/family.json` under `lists`.

## Git notes

- Remote: `https://github.com/jaklilu/Cross-Connect.git`
- Branch: `main`
- Ignored: `.env`, `Copied from PythonAnywhere/`, `node_modules/`, `__pycache__/`, `data/*.tmp`
- Commit `data/family.json` and `site/data/family.json` when roster changes on the Flask/local side.

## What is intentionally not in this project

- No database — roster is JSON; Netlify live saves use Blobs.
- No public family login — only admin password.
- No automatic calendar refresh — admin clicks **Refresh Pairing** when ready.
- No random shuffle — rotation ensures everyone meets everyone over time.

## Next steps

1. Confirm Netlify site works and admin saves persist.
2. Set `ADMIN_PASSWORD` on Netlify if not already done.
3. Shut down PythonAnywhere once satisfied.
4. Each year: fix ages → **Refresh Pairing** → verify cards.
