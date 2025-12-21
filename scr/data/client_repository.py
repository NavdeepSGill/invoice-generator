import csv

from scr.models.client import Client


def load_clients(path="../data/client_list.csv") -> list[Client]:
    """Return a List with the name of the client as the key,
    and a list of their information as the value, read from the client_list.csv.
    If there is no client list, creates an empty file instead."""
    clients = []
    try:
        with open(path, "r", newline="") as file:
            for row in csv.reader(file):
                clients.append(Client(*row))
        return clients
    except FileNotFoundError:
        open(path, "w").close()
        return clients
