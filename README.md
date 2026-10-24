# Online Food Order Processing System (DSA Micro Project 12)

A Python implementation of an Online Food Order Processing System demonstrating core Data Structures and Algorithms (DSA) concepts: **Circular Queue**, **Hash Table with Separate Chaining**, and **Sequential Search**.

---

## 🎯 Project Scope & Course Outcome (CO) Mapping

| Component | Data Structure / Algorithm | Purpose | Time Complexity |
| :--- | :--- | :--- | :--- |
| **Kitchen Order Handling** | **Circular Queue** (Array-based, FIFO) | Simulates order intake, FIFO kitchen processing, and pending order tracking without memory shifting. | Enqueue: $O(1)$<br>Dequeue: $O(1)$ |
| **Menu Storage & Lookup** | **Hash Table with Separate Chaining** | Fast menu price and availability lookup by Food Item ID. Handles collisions using singly-linked lists. | Average: $O(1)$<br>Worst: $O(n)$ |
| **Category Browsing** | **Sequential Search** (Linear Search) | Allows customers to browse and filter menu items by category (e.g., Pizza, Burger, Dessert). | $O(n)$ |

---

## 📂 Project Architecture

```
MicroProject/
├── hash_table.py       # Custom Hash Table using Separate Chaining (HashNode + HashTable)
├── circular_queue.py   # Fixed-capacity Circular Queue for order management
├── menu.py             # 20-item restaurant menu dataset with availability flags
├── order.py            # Order class containing customer details, calculations & validation
├── search.py           # Sequential search implementation for category filtering
└── main.py             # Interactive CLI application coordinating all DSA modules
```

---

## ⚙️ How Hashing with Separate Chaining Works

1. **Hash Function**:
   $$\text{index} = \text{item\_id} \pmod{\text{capacity}}$$
   With a capacity of 10 buckets and 20 menu items (IDs 101 to 120), collisions naturally occur (e.g., IDs 101 and 111 both map to bucket 1).

2. **Separate Chaining (Singly-Linked List)**:
   Each bucket in the hash table stores a pointer to the head of a linked list of `HashNode` objects.
   ```
   Bucket [01]: [ID: 111 | Chicken Wrap] -> [ID: 101 | Margherita Pizza] -> None
   Bucket [02]: [ID: 112 | Veg Wrap]      -> [ID: 102 | Chicken Burger]   -> None
   ```

3. **Collision Resolution**:
   New items that hash to an occupied slot are chained at the head of that bucket in $O(1)$ time. Lookups traverse only the short chain at that specific bucket.

---

## 🚀 How to Run

Run the interactive CLI application:
```bash
python main.py
```

### Main Menu Options:
1. **Display Menu**: Displays all 20 menu items, prices, and stock statuses.
2. **Search Food by Category**: Demonstrates **Sequential Search**.
3. **Quick Price/Availability Lookup**: Demonstrates $O(1)$ **Hash Table Lookup**.
4. **Place Order**: Validates availability via Hash Table and enqueues to the **Circular Queue**.
5. **View Pending Orders**: Displays queue contents circularly from front to rear.
6. **Process Next Order**: Dequeues the next order (FIFO kitchen processing).
7. **View Next Order**: Peeks at the front of the queue.
8. **View Hash Table Structure**: Visually displays all 10 buckets and their linked list chains (Separate Chaining).
9. **Toggle Item Availability**: Admin toggle for stock status.
10. **Exit**.