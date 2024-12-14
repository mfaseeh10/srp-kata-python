class MenuService:
    def __init__(self):
        self.menu = {}  # itemId -> (name, price, inventory)

    def add_menu_item(self, item_id, name, price, inventory):
        self.menu[item_id] = (name, price, inventory)

    def remove_menu_item(self, item_id):
        self.menu.pop(item_id, None)

    def get_menu(self, item_id):
        return self.menu
