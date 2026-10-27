"""
hash_table.py
-------------
Responsibility: Implement a HASH TABLE with SEPARATE CHAINING
collision resolution for fast (O(1) average time) price and
availability lookup of menu items.

Data Structure Details:
    - Array of Buckets: Fixed-capacity list storing head nodes of linked lists.
    - Separate Chaining: When two keys hash to the same bucket index (collision),
      they are stored in a singly-linked list (chain) at that index.
    - Hash Function: Division method (key % capacity).
"""


class HashNode:
    """
    Represents a single node in the separate chaining linked list.
    """
    def __init__(self, key, value):
        self.key = key          # Menu Item ID (int)
        self.value = value      # Item details dict (name, category, price, is_available)
        self.next = None        # Pointer to the next node in the chain


class HashTable:
    """
    A Hash Table that stores food menu items by their item ID as key.
    Uses Separate Chaining (singly-linked list) for collision resolution.
    """
    def __init__(self, capacity=10):
        """
        Initialize the hash table with a fixed capacity.
        With 20 menu items and capacity=10, each bucket will hold ~2 items,
        clearly demonstrating separate chaining collisions and traversals.
        """
        self.capacity = capacity
        self.buckets = [None] * capacity
        self.count = 0

    def _hash(self, key):
        """
        Hash function using modulo arithmetic.
        Formula: index = key % capacity
        """
        return abs(hash(key)) % self.capacity

    def insert(self, key, value):
        """
        Insert a key-value pair into the hash table.
        If the key already exists, updates its value.
        If collision occurs, appends/chains the new node at the bucket's head.

        Time Complexity:
            - Average Case: O(1)
            - Worst Case: O(n) (when all keys collide into the same bucket)
        """
        index = self._hash(key)
        current = self.buckets[index]

        # Check if the key already exists in this chain to update it
        while current is not None:
            if current.key == key:
                current.value = value
                return
            current = current.next

        # Key is not present: create new node and insert at head of chain (O(1))
        new_node = HashNode(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.count += 1

    def search(self, key):
        """
        Look up a menu item by its key (item ID).

        Returns:
            dict or None: The item details if found, or None if not found.

        Time Complexity:
            - Average Case: O(1)
            - Worst Case: O(n)
        """
        index = self._hash(key)
        current = self.buckets[index]

        # Traverse the linked list chain at this bucket index
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return None

    
    def delete(self, key):
        """
        Remove a menu item from the hash table using its key.

        Returns:
            bool: True if deleted, False if key not found.

        Time Complexity:
            Average Case: O(1)
            Worst Case: O(n)
        """
        index = self._hash(key)
        current = self.buckets[index]
        previous = None

        while current is not None:
            if current.key == key:

                # Case 1: Node is at the beginning of the chain
                if previous is None:
                    self.buckets[index] = current.next

                # Case 2: Node is in the middle or at the end
                else:
                    previous.next = current.next

                self.count -= 1
                return True

            previous = current
            current = current.next

        return False


    def update_availability(self, key, is_available):
        """
        Update the availability status of a menu item.

        Returns:
            bool: True if updated successfully, False if key not found.
        """
        item = self.search(key)
        if item is not None:
            item["is_available"] = bool(is_available)
            return True
        return False

    def display_table(self):
        """
        Print the entire hash table structure including buckets and chains.
        Demonstrates the separate chaining collision resolution visually.
        """
        print("\n================== HASH TABLE (SEPARATE CHAINING) ==================")
        print(f"Capacity: {self.capacity} buckets | Total Items: {self.count}")
        print("--------------------------------------------------------------------")

        for index in range(self.capacity):
            current = self.buckets[index]
            chain_str = f"Bucket [{index:02d}]: "

            if current is None:
                chain_str += "(empty)"
            else:
                nodes = []
                while current is not None:
                    status = "Available" if current.value.get("is_available", True) else "Out of Stock"
                    nodes.append(f"[ID: {current.key} | {current.value['name']} | Rs. {current.value['price']} | {status}]")
                    current = current.next
                chain_str += " -> ".join(nodes) + " -> None"

            print(chain_str)

        print("====================================================================\n")

    def get_all_items(self):
        """
        Return a flat list of all menu item dictionaries stored across all buckets.
        """
        items = []
        for index in range(self.capacity):
            current = self.buckets[index]
            while current is not None:
                items.append(current.value)
                current = current.next
        return items


# ---------------------------------------------------------
# TEST SECTION
# Run with "python hash_table.py" to verify functionality independently.
# ---------------------------------------------------------
if __name__ == "__main__":
    ht = HashTable(capacity=5)

    print("--- Inserting Sample Items ---")
    ht.insert(101, {"name": "Margherita Pizza", "category": "Pizza", "price": 199, "is_available": True})
    ht.insert(106, {"name": "Veg Biryani", "category": "Biryani", "price": 169, "is_available": True})
    ht.insert(111, {"name": "Chicken Wrap", "category": "Wraps", "price": 139, "is_available": False})
    ht.insert(102, {"name": "Chicken Burger", "category": "Burger", "price": 149, "is_available": True})

    print("\n--- Displaying Hash Table with Chains ---")
    ht.display_table()

    print("--- Lookup Test ---")
    item = ht.search(106)
    print("Found ID 106:", item)

    print("\n--- Availability Update Test ---")
    ht.update_availability(101, False)
    print("Updated ID 101 availability to False:", ht.search(101))

    
    print("\n--- Deletion Test ---")

    print("Before deletion:", ht.search(106))

    deleted = ht.delete(106)

    print("Deletion successful:", deleted)
    print("After deletion:", ht.search(106))
    print("Total items remaining:", ht.count)

    ht.display_table()

