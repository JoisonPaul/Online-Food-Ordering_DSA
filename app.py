from flask import Flask, render_template, request
from menu import menu
from search import sequential_search

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    category = ""
    searched = False

    if request.method == "POST":
        category = request.form.get("category", "").strip()
        searched = True

        if category:
            results = sequential_search(menu, category)

    return render_template(
        "search.html",
        results=results,
        category=category,
        searched=searched
    )


@app.route("/menu")
def display_menu():
    return render_template("menu.html", menu=menu)


@app.route("/place-order")
def place_order():
    return render_template("place_order.html")


if __name__ == "__main__":
    app.run(debug=True)
