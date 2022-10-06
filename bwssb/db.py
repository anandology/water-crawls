import web
import yaml

db = web.database("sqlite:///bwssb.db")

class STP:
    def __init__(self, row):
        self.name = row.name
        self.title = row.title
        self.capacity = row.capacity
        self.section = row.section

    @classmethod
    def all(cls):
        return [cls(row) for row in db.select("stp", order="name")]

    @classmethod
    def find(cls, name):
        result = db.where("stp", name=name)
        return cls(result[0]) if result else None

