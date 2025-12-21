class Service:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class ServiceItem:
    def __init__(self, service: Service, quantity: int):
        self.service = service
        self.quantity = quantity
