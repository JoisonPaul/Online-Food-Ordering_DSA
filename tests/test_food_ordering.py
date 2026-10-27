import app
from search import sequential_search
from circular_queue import CircularQueue


def test_01_menu_all_items(client):
    """Case 1: GET /menu shows all 20 items."""
    response = client.get("/menu")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert len(app.menu) == 20
    for item in app.menu:
        assert item["name"] in html
        assert f"Food ID: {item['id']}" in html

    # Exactly 20 food item cards are rendered
    assert html.count('class="food-card"') == 20


def test_02_sequential_search(client):
    """Case 2: sequential_search: 'Pizza' returns 2 items; 'burger' works (case-insensitive); an unknown category returns []."""
    pizza_results = sequential_search(app.menu, "Pizza")
    assert len(pizza_results) == 2
    assert [i["name"] for i in pizza_results] == ["Margherita Pizza", "Farmhouse Pizza"]
    assert all(i["category"].lower() == "pizza" for i in pizza_results)

    burger_results = sequential_search(app.menu, "burger")
    assert len(burger_results) == 2
    assert [i["name"] for i in burger_results] == ["Chicken Burger", "Veg Burger"]
    assert all(i["category"].lower() == "burger" for i in burger_results)

    unknown_results = sequential_search(app.menu, "NonExistentCategory")
    assert unknown_results == []


def test_03_hash_table_lookup(client):
    """Case 3: Hash table: search(106) returns Veg Biryani; search(999) is None; the hash table starts with 19 items (item 114 has quantity 0)."""
    assert app.food_hash_table.count == 19

    item_106 = app.food_hash_table.search(106)
    assert item_106 is not None
    assert item_106["name"] == "Veg Biryani"
    assert item_106["category"] == "Biryani"

    item_999 = app.food_hash_table.search(999)
    assert item_999 is None

    # Item 114 has quantity 0 and is unavailable, so it is omitted from the hash table initially
    item_114 = app.food_hash_table.search(114)
    assert item_114 is None

    menu_114 = [i for i in app.menu if i["id"] == 114][0]
    assert menu_114["quantity"] == 0
    assert menu_114["is_available"] is False


def test_04_hash_table_collisions(client):
    """Case 4: Collisions: 101 and 111 share a bucket and both can be found."""
    bucket_101 = app.food_hash_table._hash(101)
    bucket_111 = app.food_hash_table._hash(111)
    assert bucket_101 == bucket_111 == 1

    item_101 = app.food_hash_table.search(101)
    item_111 = app.food_hash_table.search(111)
    assert item_101 is not None and item_101["name"] == "Margherita Pizza"
    assert item_111 is not None and item_111["name"] == "Chicken Wrap"

    # Verify both nodes exist in the separate chaining linked list for bucket 1
    current = app.food_hash_table.buckets[bucket_101]
    bucket_keys = []
    while current is not None:
        bucket_keys.append(current.key)
        current = current.next

    assert 101 in bucket_keys
    assert 111 in bucket_keys


def test_05_valid_order(client):
    """Case 5: Valid order: ID 101, qty 2 gives total 398, stock 10 -> 8, queue size 1."""
    initial_stock = app.food_hash_table.search(101)["quantity"]
    assert initial_stock == 10
    assert app.order_queue.size() == 0

    response = client.post("/orders/new", data={
        "customer_name": "Alice",
        "item_id": "101",
        "quantity": "2"
    })
    assert response.status_code == 200

    assert app.order_queue.size() == 1
    order = app.order_queue.peek()
    assert order["order_id"] == 1
    assert order["customer_name"] == "Alice"
    assert order["item_name"] == "Margherita Pizza"
    assert order["quantity"] == 2
    assert order["total"] == 398

    # Stock reduced from 10 to 8
    assert app.food_hash_table.search(101)["quantity"] == 8
    menu_item_101 = [i for i in app.menu if i["id"] == 101][0]
    assert menu_item_101["quantity"] == 8


def test_06_stock_validation(client):
    """Case 6: Stock validation: qty greater than stock is rejected and stock is unchanged.
    Also test qty 0, empty name, non-numeric ID, unknown ID, and sold-out ID 114.
    """
    # 1. Quantity greater than stock
    stock_before = app.food_hash_table.search(101)["quantity"]
    res1 = client.post("/orders/new", data={
        "customer_name": "Bob",
        "item_id": "101",
        "quantity": "15"
    })
    assert res1.status_code == 200
    assert "Insufficient stock!" in res1.get_data(as_text=True)
    assert app.food_hash_table.search(101)["quantity"] == stock_before == 10
    assert app.order_queue.size() == 0

    # 2. Quantity 0
    res2 = client.post("/orders/new", data={
        "customer_name": "Bob",
        "item_id": "101",
        "quantity": "0"
    })
    assert res2.status_code == 200
    assert "Quantity must be greater than zero." in res2.get_data(as_text=True)
    assert app.food_hash_table.search(101)["quantity"] == 10
    assert app.order_queue.size() == 0

    # 3. Empty customer name
    res3 = client.post("/orders/new", data={
        "customer_name": "   ",
        "item_id": "101",
        "quantity": "1"
    })
    assert res3.status_code == 200
    assert "Please enter the customer name." in res3.get_data(as_text=True)
    assert app.food_hash_table.search(101)["quantity"] == 10
    assert app.order_queue.size() == 0

    # 4. Non-numeric ID
    res4 = client.post("/orders/new", data={
        "customer_name": "Bob",
        "item_id": "abc",
        "quantity": "1"
    })
    assert res4.status_code == 200
    assert "Enter a valid Food ID" in res4.get_data(as_text=True)
    assert app.food_hash_table.search(101)["quantity"] == 10
    assert app.order_queue.size() == 0

    # 5. Unknown ID
    res5 = client.post("/orders/new", data={
        "customer_name": "Bob",
        "item_id": "999",
        "quantity": "1"
    })
    assert res5.status_code == 200
    assert "Food item not found or out of stock" in res5.get_data(as_text=True)
    assert app.order_queue.size() == 0

    # 6. Sold-out ID 114
    menu_114 = [i for i in app.menu if i["id"] == 114][0]
    assert menu_114["quantity"] == 0
    res6 = client.post("/orders/new", data={
        "customer_name": "Bob",
        "item_id": "114",
        "quantity": "1"
    })
    assert res6.status_code == 200
    assert "Food item not found or out of stock" in res6.get_data(as_text=True)
    assert menu_114["quantity"] == 0
    assert app.order_queue.size() == 0


def test_07_stock_depletion(client):
    """Case 7: Stock depletion: ordering all 10 of ID 120 sets quantity 0 and is_available False,
    removes it from the hash table, and keeps it in /menu.
    """
    initial_item = app.food_hash_table.search(120)
    assert initial_item is not None
    assert initial_item["quantity"] == 10
    assert initial_item["is_available"] is True
    initial_count = app.food_hash_table.count

    response = client.post("/orders/new", data={
        "customer_name": "Charlie",
        "item_id": "120",
        "quantity": "10"
    })
    assert response.status_code == 200
    assert "is now out of stock and has been removed from the hash table" in response.get_data(as_text=True)

    # Item in menu list has quantity 0 and is_available False
    item_120 = [i for i in app.menu if i["id"] == 120][0]
    assert item_120["quantity"] == 0
    assert item_120["is_available"] is False

    # Removed from hash table
    assert app.food_hash_table.search(120) is None
    assert app.food_hash_table.count == initial_count - 1

    # Still appears in /menu
    res_menu = client.get("/menu")
    assert res_menu.status_code == 200
    html = res_menu.get_data(as_text=True)
    assert "Paneer Tikka" in html
    assert "Food ID: 120" in html
    assert "Out of Stock" in html


def test_08_fifo_order_processing(client):
    """Case 8: FIFO: place orders 1-3, call POST /orders/process-next, and check order 1 is processed first."""
    client.post("/orders/new", data={"customer_name": "Cust1", "item_id": "101", "quantity": "1"})
    client.post("/orders/new", data={"customer_name": "Cust2", "item_id": "102", "quantity": "1"})
    client.post("/orders/new", data={"customer_name": "Cust3", "item_id": "103", "quantity": "1"})
    assert app.order_queue.size() == 3

    response = client.post("/orders/process-next")
    assert response.status_code == 200
    assert "Order #1 processed successfully." in response.get_data(as_text=True)

    # Remaining in queue: Order #2 and Order #3
    assert app.order_queue.size() == 2
    assert app.order_queue.peek()["order_id"] == 2


def test_09_queue_overflow(client):
    """Case 9: Queue overflow: fill 10 orders, the 11th is rejected and stock is not deducted."""
    # Place 10 orders using items 101 to 110 (stock 10 each, so stock is not exhausted)
    for i in range(101, 111):
        res = client.post("/orders/new", data={
            "customer_name": f"User{i}",
            "item_id": str(i),
            "quantity": "1"
        })
        assert res.status_code == 200

    assert app.order_queue.size() == 10
    assert app.order_queue.is_full() is True

    # Stock of item 101 is now 9
    stock_101_before = app.food_hash_table.search(101)["quantity"]
    assert stock_101_before == 9

    # 11th order should be rejected
    res_11 = client.post("/orders/new", data={
        "customer_name": "User11",
        "item_id": "101",
        "quantity": "1"
    })
    assert res_11.status_code == 200
    assert "Order queue is full. Please try again later." in res_11.get_data(as_text=True)

    # Stock is not deducted
    stock_101_after = app.food_hash_table.search(101)["quantity"]
    assert stock_101_after == stock_101_before == 9

    # Queue size remains 10
    assert app.order_queue.size() == 10


def test_10_empty_queue(client):
    """Case 10: Empty queue: processing with no orders shows 'No pending orders to process.'"""
    assert app.order_queue.is_empty() is True

    response = client.post("/orders/process-next")
    assert response.status_code == 200
    assert "No pending orders to process." in response.get_data(as_text=True)
    assert app.order_queue.size() == 0


def test_11_circular_wraparound(client):
    """Case 11: Circular wrap-around: enqueue 10, dequeue 3, enqueue 2, and check the dequeue order."""
    q = CircularQueue(capacity=10)

    # Enqueue 10 orders (fill queue)
    for i in range(1, 11):
        success = q.enqueue({"order_id": i})
        assert success is True
    assert q.is_full() is True
    assert q.size() == 10

    # Dequeue 3 orders
    dequeued_first_3 = [q.dequeue()["order_id"] for _ in range(3)]
    assert dequeued_first_3 == [1, 2, 3]
    assert q.size() == 7

    # Enqueue 2 orders (wraps rear pointer around to indices 0 and 1)
    assert q.enqueue({"order_id": 11}) is True
    assert q.enqueue({"order_id": 12}) is True
    assert q.size() == 9
    assert q.rear < q.front  # rear wrapped around

    # Check dequeue order of all remaining orders
    dequeued_remaining = []
    while not q.is_empty():
        dequeued_remaining.append(q.dequeue()["order_id"])

    assert dequeued_remaining == [4, 5, 6, 7, 8, 9, 10, 11, 12]


def test_12_get_all_page_routes_and_api_endpoints(client):
    """Case 12: GET on all page routes and /api/* endpoints returns 200."""
    page_routes = [
        "/",
        "/menu",
        "/search",
        "/orders/new",
        "/orders/pending",
        "/hash-table",
    ]
    api_endpoints = [
        "/api/orders",
        "/api/hash-table",
        "/api/menu",
    ]

    for route in page_routes + api_endpoints:
        response = client.get(route)
        assert response.status_code == 200, f"Expected 200 for GET {route}, got {response.status_code}"
