from flask.json import jsonify

class Item:
    
    def __init__(self, id, title, status) -> None:
        self.id = id
        self.title = title
        self.status = status

    def toJSON(self):
        return jsonify(dict(
            id=self.id,
            title=self.title,
            status=self.status
        ))