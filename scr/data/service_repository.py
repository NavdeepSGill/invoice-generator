import csv


def load_services(path="../data/service_list.csv") -> dict[str, float]:
    """Return a dictionary with the name of the service as the key,
    and its price as the value, read from the service_list.csv.
    If there is no service list, creates an empty file instead."""
    try:
        with open(path, "r", newline="") as file:
            return {row[0]: float(row[1]) for row in csv.reader(file)}
    except FileNotFoundError:
        open(path, "w").close()
        return {}
