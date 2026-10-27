from flask import Flask, render_template, request, jsonify
from menu import menu
from search import sequential_search
from order import Order
from circular_queue import CircularQueue
from hash_table import HashTable

app = Flask(__name__)

# ---------------- INITIALIZATION ----------------

# Create Hash Table and insert only available food items
food_hash_table = HashTable(10)

for item in menu:
    if item["quantity"] > 0 and item["is_available"]:
        food_hash_table.insert(item["id"], item)

# Create Circular Queue
order_queue = CircularQueue(10)

# Generate order IDs
next_order_id = 1


# ---------------- HELPER FUNCTIONS ----------------

def get_pending_orders():
    """Return pending orders in FIFO order without removing them."""
    orders = []

    if order_queue.is_empty():
        return orders

    i = order_queue.front

    while True:
        orders.append(order_queue.queue[i])

        if i == order_queue.rear:
            break

        i = (i + 1) % order_queue.capacity

    return orders


def process_next_order():
    """Remove and complete the next order in FIFO order."""
    order = order_queue.dequeue()

    if order is None:
        return None

    order["status"] = "Completed"
    return order


def get_hash_table_data():
    """Return hash table buckets and their collision chains."""
    buckets = []

    for index in range(food_hash_table.capacity):
        items = []
        current = food_hash_table.buckets[index]

        while current is not None:
            items.append(current.value)
            current = current.next

        buckets.append({
            "index": index,
            "items": items
        })

    return {
        "capacity": food_hash_table.capacity,
        "total_items": food_hash_table.count,
        "buckets": buckets
    }


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- MENU PAGE ----------------

@app.route("/menu")
def display_menu():
    category = request.args.get("category", "").strip()

    if category:
        filtered_menu = sequential_search(menu, category)
    else:
        filtered_menu = menu

    return render_template("menu.html", menu=filtered_menu)


# ---------------- SEARCH PAGE ----------------

@app.route("/search", methods=["GET", "POST"])
def search_food():
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
        menu=menu,
        results=results,
        category=category,
        searched=searched
    )


# ---------------- PLACE ORDER ----------------

@app.route("/orders/new", methods=["GET", "POST"])
def place_order():
    global next_order_id

    message = ""
    order_details = None

    selected_item_id = request.args.get("item_id", "")

    if request.method == "POST":
        customer_name = request.form.get(
            "customer_name", ""
        ).strip()

        try:
            item_id = int(request.form.get("item_id", ""))
            quantity = int(request.form.get("quantity", ""))

            # Validate customer name
            if not customer_name:
                message = "Please enter the customer name."

            # Validate quantity
            elif quantity <= 0:
                message = "Quantity must be greater than zero."

            else:
                # Find item in the hash table
                item = food_hash_table.search(item_id)

                if item is None:
                    message = (
                        "Food item not found or out of stock. "
                        "Please check the menu."
                    )

                elif not item.get("is_available", True):
                    message = "This food item is currently unavailable."

                # Check stock before creating the order
                elif quantity > item["quantity"]:
                    message = (
                        f"Insufficient stock! Only "
                        f"{item['quantity']} unit(s) of "
                        f"{item['name']} available."
                    )

                else:
                    # Create the order
                    order = Order(
                        next_order_id,
                        customer_name,
                        item["name"],
                        quantity,
                        item["price"]
                    )

                    order_data = {
                        "order_id": order.order_id,
                        "customer_name": order.customer_name,
                        "item_name": order.item_name,
                        "quantity": order.quantity,
                        "total": order.total,
                        "status": order.status
                    }

                    # Add order to circular queue first
                    if order_queue.enqueue(order_data):

                        # Reserve stock only after successful enqueue
                        item["quantity"] -= quantity

                        if item["quantity"] == 0:
                            # Mark item as unavailable
                            item["is_available"] = False

                            # Remove sold-out item from hash table
                            food_hash_table.delete(item_id)

                            message = (
                                f"Order placed successfully! "
                                f"{item['name']} is now out of stock "
                                f"and has been removed from the hash table."
                            )

                        else:
                            message = (
                                f"Order placed successfully! "
                                f"Remaining stock of {item['name']}: "
                                f"{item['quantity']}."
                            )

                        order_details = order_data
                        next_order_id += 1

                    else:
                        message = (
                            "Order queue is full. "
                            "Please try again later."
                        )

        except ValueError:
            message = (
                "Enter a valid Food ID, customer name, "
                "and positive quantity."
            )

    return render_template(
        "place_order.html",
        message=message,
        order=order_details,
        selected_item_id=selected_item_id
    )


# ---------------- PENDING ORDERS PAGE ----------------

@app.route("/orders/pending")
def pending_orders_page():
    orders = get_pending_orders()

    return render_template(
        "orders.html",
        orders=orders,
        message=""
    )


# ---------------- PROCESS NEXT ORDER (PAGE) ----------------

@app.route("/orders/process-next", methods=["POST"])
def process_next_order_page():
    order = process_next_order()

    if order is None:
        message = "No pending orders to process."
    else:
        message = f"Order #{order['order_id']} processed successfully."

    orders = get_pending_orders()

    return render_template(
        "orders.html",
        orders=orders,
        message=message
    )


# ---------------- HASH TABLE PAGE ----------------

@app.route("/hash-table")
def hash_table_page():
    data = get_hash_table_data()

    collision_count = sum(
        1 for bucket in data["buckets"]
        if len(bucket["items"]) > 1
    )

    return render_template(
        "hash_table.html",
        data=data,
        collision_count=collision_count
    )


# ---------------- API: PENDING ORDERS ----------------

@app.route("/api/orders", methods=["GET"])
def api_orders():
    return jsonify({
        "orders": get_pending_orders()
    })


# ---------------- API: PROCESS NEXT ORDER ----------------

@app.route("/api/orders/process", methods=["POST"])
def api_process_order():
    order = process_next_order()

    if order is None:
        return jsonify({
            "message": "No pending orders to process."
        }), 404

    return jsonify({
        "message": "Order processed successfully.",
        "order": order
    })


# ---------------- API: HASH TABLE ----------------

@app.route("/api/hash-table", methods=["GET"])
def api_hash_table():
    return jsonify(get_hash_table_data())


# ---------------- API: MENU STOCK ----------------

@app.route("/api/menu", methods=["GET"])
def api_menu():
    return jsonify({
        "menu": menu,
        "hash_table_items": food_hash_table.count
    })


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)