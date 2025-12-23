import csv

from scr.models.client import Client
from scr.models.client_list import ClientList


class ClientRepository:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> ClientList:
        client_list = ClientList()
        try:
            with open(self.path, "r", newline="") as file:
                for row in csv.reader(file):
                    client_list.add(Client(*row))
        except FileNotFoundError:
            open(self.path, "w").close()

        return client_list

    def save(self, clients: ClientList) -> None:
        with open(self.path, "w", newline="") as file:
            writer = csv.writer(file)
            for client in clients.get_all():
                writer.writerow(
                    [getattr(client, attr) for attr, _ in Client.FIELDS]
                )
