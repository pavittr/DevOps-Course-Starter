class List:

    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    @staticmethod
    def fromJson(list_json):
        return List( list_json['id'], list_json['name'])