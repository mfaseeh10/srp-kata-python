class UserService:

    def __init__(self):
        self.user_balances = {}  # userId -> balance

    def add_user(self, user_id, balance):
        self.user_balances[user_id] = balance