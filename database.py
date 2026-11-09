import ujson

class Database:

    def __init__(self, filename="database.json"):
        self.filename = filename
        self.data = self.load()

    def load(self):
        try:
            with open(self.filename, "r") as f:
                return ujson.load(f)
        except:
            return {}

    def save(self):
        with open(self.filename, "w") as f:
            ujson.dump(self.data, f)

    def insert(self, table, record):
        if table not in self.data:
            self.data[table] = []

        self.data[table].append(record)
        self.save()

    def select(self, table):
        return self.data.get(table, [])

    def delete(self, table, index):
        if table in self.data:
            if 0 <= index < len(self.data[table]):
                del self.data[table][index]
                self.save()
