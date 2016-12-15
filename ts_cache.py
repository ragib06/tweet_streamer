
class TSCache():
    def __init__(self, capacity=50):
        self.capacity = capacity
        self.cache = [''] * self.capacity
        self.at = 0

    def put(self, item):
        self.cache[self.at] = item
        self.at = (self.at + 1) % self.capacity

    def contains(self, item):
        return item in self.cache
