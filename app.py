import hmac
import os
import secrets
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from family import (
    GROUPS,
    GROUP_HELP,
    GROUP_LABELS,
    add_person,
    build_grids,
    group_counts,
    grouped_people,
    load_data,
    move_person,
    new_year,
    remove_person,
    rename_person,
    update_settings,
)

ROOT = Path(__file__).resolve().parent


def _load_env():
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


_load_env()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(16)
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "CrossConnect2026")


def rebuild_site():
    from build_static import main as build_site

    build_site()


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)

    return wrapped


def public_context():
    data = load_data()
    return {
        "grids": build_grids(data),
        "welcome": data.get("welcome", "Welcome to Cousin's CrossConnect!"),
        "intro": data.get("intro", "This is some text on my page."),
        "site_title": data.get("site_title", "My Webpage"),
        "assignment_year": data.get("assignment_year", 2026),
    }


@app.route("/")
def index():
    return render_template("index.html", **public_context())


@app.route("/grid/<int:index>")
def grid(index):
    ctx = public_context()
    grids = ctx["grids"]
    if index < 0 or index >= len(grids):
        abort(404)
    card = grids[index]
    return render_template(
        "grid.html",
        grid=card,
        grid_id=index + 1,
        formatted_grid="\n".join(["".join(row) for row in card]),
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        if hmac.compare_digest(password, ADMIN_PASSWORD):
            session["admin"] = True
            session.permanent = True
            return redirect(url_for("admin_home"))
        error = "That password did not match."
    return render_template("admin_login.html", error=error)


@app.route("/admin/logout", methods=["POST"])
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin")
@admin_required
def admin_home():
    data = load_data()
    return render_template(
        "admin.html",
        data=data,
        groups=GROUPS,
        group_labels=GROUP_LABELS,
        group_help=GROUP_HELP,
        grouped=grouped_people(data),
        counts=group_counts(data),
        card_count=len(build_grids(data)),
    )


@app.route("/admin/add", methods=["POST"])
@admin_required
def admin_add():
    try:
        name = add_person(request.form.get("name", ""), request.form.get("group", ""))
        rebuild_site()
        flash(f"Added {name}.")
    except ValueError as exc:
        flash(str(exc))
    return redirect(url_for("admin_home"))


@app.route("/admin/remove", methods=["POST"])
@admin_required
def admin_remove():
    try:
        name = remove_person(request.form.get("name", ""))
        rebuild_site()
        flash(f"Removed {name}.")
    except ValueError as exc:
        flash(str(exc))
    return redirect(url_for("admin_home"))


@app.route("/admin/move", methods=["POST"])
@admin_required
def admin_move():
    try:
        name = move_person(request.form.get("name", ""), request.form.get("group", ""))
        rebuild_site()
        flash(f"Updated age group for {name}.")
    except ValueError as exc:
        flash(str(exc))
    return redirect(url_for("admin_home"))


@app.route("/admin/rename", methods=["POST"])
@admin_required
def admin_rename():
    try:
        name = rename_person(
            request.form.get("old_name", ""), request.form.get("new_name", "")
        )
        rebuild_site()
        flash(f"Renamed to {name}.")
    except ValueError as exc:
        flash(str(exc))
    return redirect(url_for("admin_home"))


@app.route("/admin/year", methods=["POST"])
@admin_required
def admin_year():
    year = new_year()
    rebuild_site()
    flash(f"New year started. Pairings for {year} are ready.")
    return redirect(url_for("admin_home"))


@app.route("/admin/settings", methods=["POST"])
@admin_required
def admin_settings():
    update_settings(
        request.form.get("welcome", ""),
        request.form.get("intro", ""),
        request.form.get("site_title", ""),
    )
    rebuild_site()
    flash("Page text saved.")
    return redirect(url_for("admin_home"))


@app.route("/admin/rebuild", methods=["POST"])
@admin_required
def admin_rebuild():
    rebuild_site()
    flash("Netlify files in site/ were rebuilt. Push to GitHub when you want the public site updated.")
    return redirect(url_for("admin_home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
