key = "your_secret_key"
class secret:
    def __init__(self, value):
        self._storage = {}
        self._storage[key] = value

    def __str__(self):
        return "[Access Denied]"

    def __repr__(self):
        return "[Access Denied]"

    def reveal(self):
        return "[Access Denied]"

    def __eq__(self, other):
        if isinstance(other, secret):
            return self._storage[key] == other._storage[key]
        if isinstance(other, str):
            return self._storage[key] == other
        return False
