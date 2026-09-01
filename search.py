"""
search.py
----------
Responsibility: Implement SEQUENTIAL (LINEAR) SEARCH to browse
food menu items by category.

This file does NOT create the menu data (menu.py does that) and
does NOT handle orders, billing, or the circular queue. It only
contains the search algorithm and a helper to display results.
"""


def sequential_search(menu, category):
    """
    Perform a sequential (linear) search on the menu list to find
    all items that belong to the given category.

    How sequential search works:
        - We start at the FIRST item in the menu list.
        - We compare its category with the category we are
          looking for.
        - If it matches, we add it to our results list.
        - We move to the NEXT item and repeat.
        - We keep doing this until we have checked EVERY item
          in the menu (there is no "jumping around" - we go
          one by one, in order, which is why it is called
          "sequential" or "linear" search).

    Parameters:
        menu (list of dict): The menu data, e.g.
            [{"id": 101, "name": "Margherita Pizza",
              "category": "Pizza", "price": 199}, ...]
        category (str): The category the user wants to browse,
            e.g. "pizza", "Pizza", "PIZZA" (case does not matter).

    Returns:
        list: A list of menu item dictionaries whose category
              matches the requested category. Returns an empty
              list if no items match.
    """

    # This list will hold every matching item we find.
    matching_items = []

    # Make the search term lowercase ONCE, outside the loop,
    # so the comparison is case-insensitive
    # (e.g. "Pizza" == "pizza" == "PIZZA").
    target_category = category.lower()

    # --- Sequential Search Loop ---
    # We look at each menu item ONE BY ONE, from the first
    # item to the last item, in order.
    for item in menu:

        # Compare the current item's category (also lowercased)
        # with the target category.
        item_category = item["category"].lower()

        if item_category == target_category:
            # Found a match! Add this item to our results.
            matching_items.append(item)

        # If it doesn't match, we simply move on to the next
        # item in the next loop iteration. We never skip items
        # and we never stop early - we check all of them.

    # After checking every item, return whatever we found.
    # If nothing matched, matching_items will simply be [].
    return matching_items


def display_search_results(results):
    """
    Neatly display the list of menu items returned by
    sequential_search().

    Parameters:
        results (list of dict): The list of matching menu items.
    """

    # Case 1: No items were found.
    if len(results) == 0:
        print("No items found in this category.")
        return

    # Case 2: Show a simple, readable list of matches.
    print(f"Found {len(results)} item(s):")
    print("-" * 40)

    for item in results:
        print(f"ID      : {item['id']}")
        print(f"Name    : {item['name']}")
        print(f"Category: {item['category']}")
        print(f"Price   : Rs. {item['price']}")
        print("-" * 40)


# ---------------------------------------------------------
# TEST SECTION
# This code only runs when search.py is executed directly,
# e.g. "python search.py". It will NOT run when search.py is
# imported by main.py. This lets you test this file on its own.
# ---------------------------------------------------------
if __name__ == "__main__":

    # Import the real menu data from menu.py
    from menu import menu

    print("Test 1: Searching for 'Pizza'")
    results = sequential_search(menu, "Pizza")
    display_search_results(results)

    print("\nTest 2: Searching for lowercase 'burger' (case-insensitive check)")
    results = sequential_search(menu, "burger")
    display_search_results(results)

    print("\nTest 3: Searching for a category that does not exist")
    results = sequential_search(menu, "Dessert")
    display_search_results(results)
