from flask import Flask, render_template

app = Flask(__name__)

# Define the lists of names for each age group
# 65&over
names_file1 = [
    "Ken",
    "Etalem",
    "Solomon",
    "Belle",
    "Tony",
    "Chief",
    "Martha",
    "Hailelul",
    "Joseph",
    "Loreta",
    "Vero",
    "Senny",
    "Membe",
]
# 30s&40s
names_file3 = [
    "Elias",
    "Eskender",
    "Sal",
    "Josh",
    "Romeo",
    "Daweet",
    "Betu",
    "Kristopher",
    "Matti",
    "Nadeen",
    "Mickey",
    "Veronica",
    "Macki",
    "Neb",
]
# 20s&30s
names_file4 = [
    "Amanu",
    "Maya",
    "Liyu",
    "Bethel",
    "Abel",
    "Faven",
    "Josh",
    "Amara",
    "Hosanna",
    "Emu",
    "Danu",
    "Menna",
    "Jano",
    "Natu",
]
# under12
names_file5 = ["Abesha", "Helah", "Kayla", "Layla", "Soliana"]


# Define a function to format and center each value in a cell
def format_value(value):
    # Convert the value to a string and pad it with spaces to a fixed width
    padded_value = str(value).center(12)
    # Return the padded value
    return padded_value


# Define a function to format and center each value in a cell
def format_value(value):
    # Check if the value is 1, 3, 7, or 9
    if value in [1, 3, 7, 9]:
        # Return an empty string to remove the label from the grid
        return ""
    else:
        # Convert the value to a string and pad it with spaces to a fixed width
        padded_value = str(value).center(12)
        # Return the padded value
        return padded_value


# Iterate over each name and create a separate 3x3 grid for each
grids = []
for i, name in enumerate(names_file4):
    # Create the grid with the current name from file3
    grid = [[1, 2, 3], [4, name, None], [7, 8, 9]]
    # Calculate the index of the next name using modulo
    next_index = (i + 1) % len(names_file4)
    next_name = names_file4[next_index]
    grid[1][2] = next_name

    # Replace the value in grid spot 4 with the name from file4
    name_file3_index = i % len(names_file3)
    name_file3 = names_file3[name_file3_index]
    grid[1][0] = name_file3

    # Replace the value in grid spot 8 with the name from file5
    name_file5_index = i % len(names_file5)
    name_file5 = names_file5[name_file5_index]
    grid[2][1] = name_file5

    # Replace the value in grid spot 2 with the name from file1
    name_file1_index = i % len(names_file1)
    name_file1 = names_file1[name_file1_index]
    grid[0][1] = name_file1

    # Convert each value in the grid to a formatted string
    formatted_grid = [[format_value(value) for value in row] for row in grid]
    # Add the formatted grid to the list of grids
    grids.append(formatted_grid)


@app.route("/")
def index():
    # Render the template and pass in the list of grids as a context variable
    return render_template("index3.html", grids=grids)


@app.route("/grid/<int:index>")
def grid(index):
    # Render the grid.html template with the appropriate grid
    grid = grids[index]
    return render_template(
        "grid3.html",
        grid=grid,
        grid_id=index + 1,
        formatted_grid="\n".join(["".join(row) for row in grid]),
    )


if __name__ == "__main__":
    app.run(port=8080)
    app.run(debug=True)
