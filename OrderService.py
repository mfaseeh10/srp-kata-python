import uuid


class OrderService:
    def __init__(self, menuService, userService, riderService, notificationService):

        self.orders = {}  # orderId -> { details }
        self.menuService = menuService
        self.userService = userService
        self.riderService = riderService
        self.notificationService = notificationService

    def create_order(self, user_id, item_ids, discount_code=None):
        if user_id not in self.userService.user_balances:
            raise RuntimeError("User not found.")
        if not item_ids:
            raise RuntimeError("Order must have at least one item.")

        total = 0.0
        items_with_insufficient_inventory = []

        for item_id in item_ids:
            item = self.menuService.get_menu()[item_id]
            if not item:
                raise RuntimeError(f"Menu item {item_id} not found.")
            if item[2] <= 0:
                items_with_insufficient_inventory.append(item_id)
            total += item[1]

        if items_with_insufficient_inventory:
            raise RuntimeError(f"Insufficient inventory for items: {items_with_insufficient_inventory}")

        # Apply discount
        discount = self.calculate_discount(total, discount_code)
        total -= discount

        # Check user balance
        if self.user_balances[user_id] < total:
            raise RuntimeError("Insufficient balance.")

        # Deplete inventory
        for item_id in item_ids:
            name, price, inventory = self.menuService.menu[item_id]
            self.menuService.get_menu()[item_id] = (name, price, inventory - 1)

        # Assign a rider
        if not self.riderService.get_riders():
            raise RuntimeError("No riders available.")
        assigned_rider = self.riderService.get_riders().pop(0)

        # Create order
        order_id = str(uuid.uuid4())
        self.orders[order_id] = {
            "user_id": user_id,
            "item_ids": item_ids,
            "total": total,
            "status": "Pending",
            "rider": assigned_rider,
        }

        # Notify customer and restaurant
        self.notificationService.notification(user_id, f"Your order {order_id} has been placed successfully.")
        self.notificationService.send_notification("restaurant", f"A new order {order_id} has been received.")

        return order_id

    def calculate_discount(self, total, discount_code):
        if discount_code == "DISCOUNT10":
            return total * 0.10
        elif discount_code == "DISCOUNT20":
            return total * 0.20
        else:
            return 0.0

    def get_delivery_status(self, order_id):
        order = self.order.get(order_id)
        if not order:
            raise RuntimeError(f"Order {order_id} not found.")
        return order["status"]

    def update_delivery_status(self, order_id, status):
        order = self.orders.get(order_id)
        if not order:
            raise RuntimeError(f"Order {order_id} not found.")
        order["status"] = status
