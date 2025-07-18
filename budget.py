class Budget:
    def __init__(self, category, limit):
        self.category = category
        self.limit = limit
        self.current_spending = 0.0

    def update_spending(self, amount):
        self.current_spending += amount

    def is_exceeded(self):
        return self.current_spending > self.limit

    def remaining(self):
        return self.limit - self.current_spending

    def to_dict(self):
        return {
            "category": self.category,
            "limit": self.limit,
            "current_spending": self.current_spending
        }

    @classmethod
    def from_dict(cls,category, data):
        b = cls(category, data["limit"])
        b.current_spending = data.get("current_spending", 0.0)
        return b
