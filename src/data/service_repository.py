import csv

from src.models.service import Service
from src.models.service_list import ServiceList


class ServiceRepository:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> ServiceList:
        service_list = ServiceList()
        try:
            with open(self.path, "r", newline="") as file:
                for row in csv.reader(file):
                    service_list.add(Service(*row))
        except FileNotFoundError:
            open(self.path, "w").close()

        return service_list

    def save(self, services: ServiceList) -> None:
        with open(self.path, "w", newline="") as file:
            writer = csv.writer(file)
            for service in services.get_all():
                writer.writerow(
                    [getattr(service, attr) for attr, _ in Service.FIELDS]
                )
