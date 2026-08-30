class Order:
    def __init__(self, order_id, customer_name, item_name, quantity, price):
        # Validate order ID
        if order_id <= 0:
            raise ValueError("Order ID must be positive.")

        # Validate customer name
        if not customer_name.strip():
            raise ValueError("Customer name cannot be empty.")

        # Validate item name
        if not item_name.strip():
            raise ValueError("Item name cannot be empty.")

        # Validate quantity
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        # Validate price
        if price < 0:
            raise ValueError("Price cannot be negative.")

        self.order_id = order_id
        self.customer_name = customer_name
        self.item_name = item_name
        self.quantity = quantity
        self.price = price
        self.total = self.calculate_total()
        self.status = "Pending"

    def calculate_total(self):
        return self.quantity * self.price

    def update_quantity(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        self.quantity = quantity
        self.total = self.calculate_total()

    def complete_order(self):
        self.status = "Completed"

    def display_order(self):
        print("\n----- ORDER DETAILS -----")
        print("Order ID    :", self.order_id)
        print("Customer    :", self.customer_name)
        print("Item        :", self.item_name)
        print("Quantity    :", self.quantity)
        print("Unit Price  : ₹", self.price)
        print("Total       : ₹", self.total)
        print("Status      :", self.status)

    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name} - {self.item_name} x{self.quantity} - Rs. {self.total} - {self.status}"