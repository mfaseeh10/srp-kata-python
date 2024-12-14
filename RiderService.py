class RiderService:
    def __init__(self):
        self.riders = []  # List of available riders

    def add_rider(self, rider_id):
        self.riders.append(rider_id)

    def get_riders(self):
        return self.riders
    