from flask import Flask, render_template, request
from menu import menu
from search import sequential_search
from order import Order
from circular_queue import CircularQueue
from hash_table import HashTable

app = Flask(__name__)

# Initialize Hash Table and insert menu items
food_hash_table = HashTable(10)

for item in menu:
    food_hash_table.insert(item["id"], item)

# Initialize Circular Queue
order_queue = CircularQueue(10)

# Generate order IDs
next_order_id = 1


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


@app.route("/place-order", methods=["GET", "POST"])
def place_order():
    global next_order_id

    message = ""
    order_details = None

    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()

        try:
            item_id = int(request.form.get("item_id", ""))
            quantity = int(request.form.get("quantity", ""))

            # Find food item using Hash Table
            item = food_hash_table.search(item_id)

            if item is None:
                message = "Invalid Food ID. Please check the menu."
            elif not item.get("is_available", True):
                message = "Sorry, this food item is currently unavailable."
            else:
                # Create Order object
                order = Order(
                    next_order_id,
                    customer_name,
                    item["name"],
                    quantity,
                    item["price"]
                )

                # Convert Order object into a dictionary for the queue
                order_data = {
                    "order_id": order.order_id,
                    "customer_name": order.customer_name,
                    "item_name": order.item_name,
                    "quantity": order.quantity,
                    "total": order.total,
                    "status": order.status
                }

                # Add order to Circular Queue
                if order_queue.enqueue(order_data):
                    order_details = order_data
                    next_order_id += 1
                    message = "Order placed successfully!"
                else:
                    message = "The order queue is full. Please try again later."

        except ValueError as error:
            message = str(error) if str(error) else "Enter valid numbers for Food ID and quantity."

    return render_template(
        "place_order.html",
        message=message,
        order=order_details
    )


if __name__ == "__main__":
    app.run(debug=True)
