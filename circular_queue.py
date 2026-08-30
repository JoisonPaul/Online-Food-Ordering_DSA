class CircularQueue:

    def __init__(self, capacity=10):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = -1
        self.rear = -1

    # Check if the queue is empty
    def is_empty(self):
        return self.front == -1

    # Check if the queue is full
    def is_full(self):
        return (self.rear + 1) % self.capacity == self.front

    # Add an order to the queue
    def enqueue(self, order):

        if self.is_full():
            print("Queue is full. Cannot place the order.")
            return False

        # If queue is empty
        if self.is_empty():
            self.front = 0
            self.rear = 0

        # Otherwise move rear circularly
        else:
            self.rear = (self.rear + 1) % self.capacity

        self.queue[self.rear] = order

        print(f"Order #{order['order_id']} added to the queue.")
        return True

    # Remove and process the first order
    def dequeue(self):

        if self.is_empty():
            print("Queue is empty. No orders to process.")
            return None

        order = self.queue[self.front]

        # Remove the order
        self.queue[self.front] = None

        # If this was the last order
        if self.front == self.rear:
            self.front = -1
            self.rear = -1

        # Otherwise move front circularly
        else:
            self.front = (self.front + 1) % self.capacity

        return order

    # View the first order without removing it
    def peek(self):

        if self.is_empty():
            print("Queue is empty.")
            return None

        return self.queue[self.front]

    # Display all pending orders
    def display(self):

        if self.is_empty():
            print("\nNo pending orders.")
            return

        print("\n========== PENDING ORDERS ==========")

        i = self.front

        while True:

            order = self.queue[i]

            print(
                f"Order #{order['order_id']} | "
                f"Customer: {order['customer_name']} | "
                f"Item: {order['item_name']} | "
                f"Quantity: {order['quantity']} | "
                f"Total: ₹{order['total']}"
            )

            if i == self.rear:
                break

            i = (i + 1) % self.capacity

        print("====================================")

    # Return number of orders currently in queue
    def size(self):

        if self.is_empty():
            return 0

        if self.rear >= self.front:
            return self.rear - self.front + 1

        return self.capacity - self.front + self.rear + 1