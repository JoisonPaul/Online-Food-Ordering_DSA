from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("search.html")

@app.route("/place-order")
def place_order():
    return render_template("place_order.html")

if __name__ == "__main__":
    app.run(debug=True)