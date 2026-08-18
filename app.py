from flask import Flask, abort, render_template

from family import build_grids

app = Flask(__name__)
grids = build_grids()


@app.route("/")
def index():
    return render_template("index.html", grids=grids)


@app.route("/grid/<int:index>")
def grid(index):
    if index < 0 or index >= len(grids):
        abort(404)
    card = grids[index]
    return render_template(
        "grid.html",
        grid=card,
        grid_id=index + 1,
        formatted_grid="\n".join(["".join(row) for row in card]),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
