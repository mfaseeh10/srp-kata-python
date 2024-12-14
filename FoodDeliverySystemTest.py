import unittest
class TestFoodDeliverySystem(unittest.TestCase):
    def setUp(self):
        """Set up a fresh instance of the FoodDeliverySystem before each test."""


    def test_add_menu_item(self):
        self.system.add_menu_item("item1", "Burger", 5.99, 10)
        menu = self.system.get_menu()
        self.assertIn("item1", menu)
        self.assertEqual("Burger", menu["item1"][0])

    def test_remove_menu_item(self):
        self.system.add_menu_item("item1", "Burger", 5.99, 10)
        self.system.remove_menu_item("item1")
        menu = self.system.get_menu()
        self.assertNotIn("item1", menu)

    def test_add_user(self):
        self.system.add_user("user1", 20.0)
        # Test is successful if no exceptions are thrown

    def test_create_order_success(self):
        self.system.add_menu_item("item1", "Burger", 5.99, 10)
        self.system.add_user("user1", 20.0)
        self.system.add_rider("rider1")

        order_id = self.system.create_order("user1", ["item1"], None)
        delivery_status = self.system.get_delivery_status(order_id)

        self.assertIsNotNone(order_id)
        self.assertEqual("Pending", delivery_status)

    def test_create_order_insufficient_balance(self):
        self.system.add_menu_item("item1", "Burger", 5.99, 10)
        self.system.add_user("user1", 5.0)
        self.system.add_rider("rider1")

        with self.assertRaises(RuntimeError) as context:
            self.system.create_order("user1", ["item1"], None)
        self.assertEqual("Insufficient balance.", str(context.exception))

    def test_create_order_insufficient_inventory(self):
        self.system.add_menu_item("item1", "Burger", 5.99, 0)
        self.system.add_user("user1", 20.0)
        self.system.add_rider("rider1")

        with self.assertRaises(RuntimeError) as context:
            self.system.create_order("user1", ["item1"], None)
        self.assertIn("Insufficient inventory", str(context.exception))

    def test_create_order_no_riders_available(self):
        self.system.add_menu_item("item1", "Burger", 5.99, 10)
        self.system.add_user("user1", 20.0)

        with self.assertRaises(RuntimeError) as context:
            self.system.create_order("user1", ["item1"], None)
        self.assertEqual("No riders available.", str(context.exception))

    def test_create_order_with_discount(self):
        self.system.add_menu_item("item1", "Burger", 10.0, 10)
        self.system.add_user("user1", 20.0)
        self.system.add_rider("rider1")

        order_id = self.system.create_order("user1", ["item1"], "DISCOUNT10")
        order_details = self.system.get_delivery_status(order_id)

        self.assertIsNotNone(order_id)
        self.assertEqual("Pending", order_details)

    def test_update_delivery_status(self):
        self.system.add_menu_item("item1", "Burger", 5.99, 10)
        self.system.add_user("user1", 20.0)
        self.system.add_rider("rider1")

        order_id = self.system.create_order("user1", ["item1"], None)
        self.system.update_delivery_status(order_id, "Delivered")

        status = self.system.get_delivery_status(order_id)
        self.assertEqual("Delivered", status)

    def test_add_rider(self):
        self.system.add_rider("rider1")
        riders = self.system.get_riders()
        self.assertIn("rider1", riders)

    def test_rider_removed_after_assignment(self):
        self.system.add_menu_item("item1", "Burger", 5.99, 10)
        self.system.add_user("user1", 20.0)
        self.system.add_rider("rider1")

        self.system.create_order("user1", ["item1"], None)
        riders = self.system.get_riders()

        self.assertNotIn("rider1", riders)


if __name__ == "__main__":
    unittest.main()
