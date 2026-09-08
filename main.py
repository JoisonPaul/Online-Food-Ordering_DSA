from menu import menu
from search import sequential_search, display_search_results
from order import Order
from circular_queue import CircularQueue


# Create the circular queue
order_queue = CircularQueue(10)

# Starting order ID
next_order_id = 1001


def display_menu():
    print("\n========== MENU ==========")

    for item in menu:
        print(
            f"ID: {item['id']} | "
            f"{item['name']} | "
            f"{item['category']} | "
            f"₹{item['price']}"
        )

    print("===========================")


def search_category():
    category = input("\nEnter category to search: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    results = sequential_search(menu, category)

    print()
    display_search_results(results)


def place_order():
    global next_order_id

    display_menu()

    try:
        item_id = int(input("\nEnter food item ID: "))
    except ValueError:
        print("Invalid item ID.")
        return

    # Find the selected item
    selected_item = None

    for item in menu:
        if item["id"] == item_id:
            selected_item = item
            break

    if selected_item is None:
        print("Food item not found.")
        return

    customer_name = input("Enter customer name: ").strip()

    try:
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Invalid quantity.")
        return

    try:
        # Create Order object
        order = Order(
            next_order_id,
            customer_name,
            selected_item["name"],
            quantity,
            selected_item["price"]
        )

        # Convert Order object into dictionary format
        # required by CircularQueue
        queue_order = {
            "order_id": order.order_id,
            "customer_name": order.customer_name,
            "item_name": order.item_name,
            "quantity": order.quantity,
            "total": order.total
        }

        # Add order to circular queue
        if order_queue.enqueue(queue_order):
            print("\nOrder placed successfully!")
            order.display_order()
            next_order_id += 1

    except ValueError as e:
        print("Error:", e)


def process_order():
    order = order_queue.dequeue()

    if order is not None:
        print("\n========== PROCESSING ORDER ==========")
        print("Order ID    :", order["order_id"])
        print("Customer    :", order["customer_name"])
        print("Item        :", order["item_name"])
        print("Quantity    :", order["quantity"])
        print("Total       : ₹", order["total"])
        print("Status      : Completed")
        print("======================================")


def view_next_order():
    order = order_queue.peek()

    if order is not None:
        print("\n========== NEXT ORDER ==========")
        print("Order ID    :", order["order_id"])
        print("Customer    :", order["customer_name"])
        print("Item        :", order["item_name"])
        print("Quantity    :", order["quantity"])
        print("Total       : ₹", order["total"])
        print("===============================")


def main():
    while True:

        print("\n========================================")
        print("       ONLINE FOOD ORDER SYSTEM")
        print("========================================")
        print("1. Display Menu")
        print("2. Search Food by Category")
        print("3. Place Order")
        print("4. View Pending Orders")
        print("5. Process Next Order")
        print("6. View Next Order")
        print("7. Exit")
        print("========================================")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            display_menu()

        elif choice == "2":
            search_category()

        elif choice == "3":
            place_order()

        elif choice == "4":
            order_queue.display()

        elif choice == "5":
            process_order()

        elif choice == "6":
            view_next_order()

        elif choice == "7":
            print("\nThank you for using the Online Food Order System!")
            break

        else:
            print("\nInvalid choice. Enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
