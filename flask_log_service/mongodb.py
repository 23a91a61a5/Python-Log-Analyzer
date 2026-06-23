class DummyResult:
    inserted_id = "demo-id"


class DummyReports:

    def insert_one(self, data):
        return DummyResult()

    def find(self):
        return []


reports = DummyReports()
