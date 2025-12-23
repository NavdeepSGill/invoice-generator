from src.models.service import Service


class ServiceList:
    def __init__(self):
        self._services = []

    def add(self, service: Service):
        if service.name in self.get_names():
            raise ValueError(f"{service} already exists.")
        self._services.append(service)

    def get(self, service_name: str) -> Service:
        for service in self._services:
            if service_name == service.name:
                return service

    def get_price(self, service_name: str) -> float:
        for service in self._services:
            if service_name == service.name:
                return service.price
        raise ValueError(f"{service_name} not found.")

    def get_names(self) -> list[str]:
        return [service.name for service in self._services]
