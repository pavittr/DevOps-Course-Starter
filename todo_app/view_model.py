class ViewModel:
    def __init__(self, items) -> None:
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def to_do_items(self):
        return self.get_items(["To Do"])

    @property
    def doing_items(self):
        return self.get_items(["Doing"])

    @property
    def done_items(self):
        return self.get_items(["Done"])

    def get_items(self, status_constraints=[]):
        return list(filter(lambda item: item.status in status_constraints, self._items))