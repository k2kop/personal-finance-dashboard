from datetime import datetime

class Transaction:
    def __init__(self, date, amount, category, t_type, description):
        self.date = self._parse_date(date)
        self.amount = amount
        self.category = category
        self.type = t_type.lower()
        self.description = description

    def _parse_date(self, date_str):
        """Convert string to datetime object."""
        try:
            return datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Date must be in DD-MM-YYYY format.")

    def is_valid(self):
        """Validate transaction data."""
        if self.amount <= 0:
            return False
        if self.type not in ["income", "expense"]:
            return False
        return True

    def to_dict(self):
        """Convert transaction to a dictionary (for saving)."""
        return {
            "date": self.date.strftime("%d-%m-%Y"),
            "amount": self.amount,
            "category": self.category,
            "type": self.type,
            "description": self.description
        }
