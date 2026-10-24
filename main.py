from menu import menu
from search import sequential_search, display_search_results
from order import Order
from circular_queue import CircularQueue
from hash_table import HashTable


# ---------------------------------------------------------
# DATA STRUCTURES INITIALIZATION
# ---------------------------------------------------------
# 1. Circular Queue for kitchen order handling (capacity: 10)
order_queue = CircularQueue(10)

# 2. Hash Table with Separate Chaining for fast menu lookup (capacity: 10)
# With 20 menu items, each bucket stores chains of ~2 items on average
menu_table = HashTable(capacity=10)
for item in menu:
    menu_table.insert(item["id"], item)

# Starting order ID sequence
next_order_id = 1001


def display_menu():
    """
    Display the restaurant menu with ID, Name, Category, Price, and Availability.
    """
    print("\n========================= RESTAURANT MENU =========================")
    print(f"{'ID':<6} | {'Item Name':<20} | {'Category':<14} | {'Price':<10} | {'Status'}")
    print("-" * 67)

    for item in menu:
        status = "Available" if item.get("is_available", True) else "Out of Stock"
        print(
            f"{item['id']:<6} | "
            f"{item['name']:<20} | "
            f"{item['category']:<14} | "
            f"Rs. {item['price']:<6} | "
            f"{status}"
        )

    print("===================================================================\n")


def search_category():
    """
    Browse menu items by category using SEQUENTIAL (LINEAR) SEARCH.
    """
    category = input("\nEnter category to search (e.g. Pizza, Burger, Dessert): ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    results = sequential_search(menu, category)

    print()
    display_search_results(results)


def lookup_item_hash():
    """
    Quick price and availability lookup using the HASH TABLE with Separate Chaining.
    Average Time Complexity: O(1).
    """
    print("\n--- QUICK PRICE / AVAILABILITY LOOKUP (HASH TABLE) ---")
    try:
        item_id = int(input("Enter food item ID to look up: "))
    except ValueError:
        print("Invalid item ID. Please enter a valid number.")
        return

    # Direct O(1) average lookup via Hash Table
    item = menu_table.search(item_id)

    if item is None:
        print(f"\nItem with ID {item_id} not found in the menu.")
        return

    status = "Available" if item.get("is_available", True) else "Out of Stock"
    print("\n---------------- ITEM DETAILS ----------------")
    print(f"Item ID     : {item['id']}")
    print(f"Name        : {item['name']}")
    print(f"Category    : {item['category']}")
    print(f"Price       : Rs. {item['price']}")
    print(f"Status      : {status}")
    print("----------------------------------------------")


def place_order():
    """
    Place a new food order.
    Uses HASH TABLE to quickly lookup item details and check availability.
    Adds valid orders to the CIRCULAR QUEUE.
    """
    global next_order_id

    display_menu()

    try:
        item_id = int(input("Enter food item ID: "))
    except ValueError:
        print("Invalid item ID.")
        return

    # Look up item in O(1) average time using Hash Table (replaced mock linear scan)
    selected_item = menu_table.search(item_id)

    if selected_item is None:
        print("Food item not found.")
        return

    # Check availability before placing order
    if not selected_item.get("is_available", True):
        print(f"\nSorry, '{selected_item['name']}' is currently OUT OF STOCK and cannot be ordered.")
        return

    customer_name = input("Enter customer name: ").strip()
    if not customer_name:
        print("Customer name cannot be empty.")
        return

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

        # Convert Order object into dictionary format for CircularQueue
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
    """
    Dequeue and process the next order from the CIRCULAR QUEUE (FIFO kitchen simulation).
    """
    order = order_queue.dequeue()

    if order is not None:
        print("\n========== PROCESSING ORDER ==========")
        print("Order ID    :", order["order_id"])
        print("Customer    :", order["customer_name"])
        print("Item        :", order["item_name"])
        print("Quantity    :", order["quantity"])
        print("Total       : Rs.", order["total"])
        print("Status      : Completed")
        print("======================================")


def view_next_order():
    """
    Peek at the next order in the circular queue without removing it.
    """
    order = order_queue.peek()

    if order is not None:
        print("\n========== NEXT ORDER ==========")
        print("Order ID    :", order["order_id"])
        print("Customer    :", order["customer_name"])
        print("Item        :", order["item_name"])
        print("Quantity    :", order["quantity"])
        print("Total       : Rs.", order["total"])
        print("================================")


def toggle_item_availability():
    """
    Admin utility: Toggle whether a menu item is available or out of stock.
    Demonstrates updating node values in the Hash Table.
    """
    print("\n--- UPDATE ITEM AVAILABILITY ---")
    try:
        item_id = int(input("Enter food item ID to toggle: "))
    except ValueError:
        print("Invalid item ID.")
        return

    item = menu_table.search(item_id)
    if item is None:
        print(f"Item ID {item_id} not found.")
        return

    new_status = not item.get("is_available", True)
    menu_table.update_availability(item_id, new_status)

    # Keep menu list in sync
    for m in menu:
        if m["id"] == item_id:
            m["is_available"] = new_status
            break

    status_str = "Available" if new_status else "Out of Stock"
    print(f"\nStatus of '{item['name']}' (ID: {item_id}) updated to: {status_str}")


def view_hash_table_structure():
    """
    Display internal Hash Table buckets and linked list chains (Separate Chaining).
    Useful for demonstration and viva presentation.
    """
    menu_table.display_table()


def main():
    while True:
        print("\n========================================")
        print("       ONLINE FOOD ORDER SYSTEM")
        print("========================================")
        print("1. Display Menu")
        print("2. Search Food by Category (Sequential Search)")
        print("3. Quick Price/Availability Lookup (Hash Table)")
        print("4. Place Order")
        print("5. View Pending Orders (Circular Queue)")
        print("6. Process Next Order")
        print("7. View Next Order")
        print("8. View Hash Table Structure (Separate Chaining)")
        print("9. Toggle Item Availability (Admin)")
        print("10. Exit")
        print("========================================")

        choice = input("Enter your choice (1-10): ").strip()

        if choice == "1":
            display_menu()

        elif choice == "2":
            search_category()

        elif choice == "3":
            lookup_item_hash()

        elif choice == "4":
            place_order()

        elif choice == "5":
            order_queue.display()

        elif choice == "6":
            process_order()

        elif choice == "7":
            view_next_order()

        elif choice == "8":
            view_hash_table_structure()

        elif choice == "9":
            toggle_item_availability()

        elif choice == "10":
            print("\nThank you for using the Online Food Order System!")
            break

        else:
            print("\nInvalid choice. Enter a number from 1 to 10.")


if __name__ == "__main__":
    main()
