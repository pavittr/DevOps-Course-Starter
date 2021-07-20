class Boards:

    def __init__(self, trello_transport) -> None:
        self.trello_transport = trello_transport
    
    def create_trello_board(self, org_id, board_name = "test"):
        reponse = self.trello_transport.call_trello("POST", f"/1/boards/", {'name':board_name, "idOrganization": org_id})
        if reponse.status_code != 200:
            raise Exception(f"Failed to make request, got back {reponse.status_code}:{reponse.json()}")
        json_output = reponse.json()
        return json_output['id']

    def delete_trello_board(self, board_id):
        response = self.trello_transport.call_trello("DELETE", f"/1/boards/{board_id}")
        response.raise_for_status()