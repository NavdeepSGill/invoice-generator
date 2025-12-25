class Service:
    FIELDS = [
        ("name", "Service"),
        ("price", "Price"),
    ]

    def __init__(self, name: str, price: str):
        self.name = name
        self.price = float(price)


class ServiceItem:
    FIELDS = Service.FIELDS + [
        ("quantity", "Amount"),
    ]
    COLUMN_MINSIZES = {
        "name": 370,
        "price": 80,
        "quantity": 99,
    }

    def __init__(self, service: Service, quantity: int = 1):
        self.service = service
        self.quantity = quantity
        self.quantity_label = None
        self.widgets = None
