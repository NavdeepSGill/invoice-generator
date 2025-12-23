from scr.models.client import Client


class ClientList:
    def __init__(self):
        self._clients = []

    def add(self, client: Client):
        self._clients.append(client)

    def remove(self, other: Client):
        for client in self._clients:
            if client == other:
                self._clients.remove(client)

    def get_all(self) -> list[Client]:
        return self._clients

    def get_attribute(self, attribute: str) -> list[str]:
        if attribute not in {attr for attr, _ in Client.FIELDS}:
            raise ValueError(f"Client has no attribute '{attribute}'")

        return [getattr(client, attribute) for client in self._clients]

    def get_client(self, attribute, attr_value) -> Client:
        for client in self._clients:
            if getattr(client, attribute) == attr_value:
                return client

        raise ValueError(f"Client with '{attribute}': '{attr_value}' does not exist")
