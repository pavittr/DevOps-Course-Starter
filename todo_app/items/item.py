import json

class Item:
    
    def __init__(self, id, title, status) -> None:
        self.id = id
        self.title = title
        self.status = status

class ItemEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Item):
            return dict(
            id=obj.id,
            title=obj.title,
            status=obj.status
        )
        return json.JSONEncoder.default(self, obj)