class Client:
    FIELDS = [
        ("name", "Name"),
        ("email", "Email"),
        ("street", "Street"),
        ("city", "City"),
        ("province", "Province"),
        ("postal_code", "Postal Code"),
    ]

    def __init__(self, name: str, email: str, street: str, city: str, province: str, postal_code: str):
        self.name = name
        self.email = email
        self.street = street
        self.city = city
        self.province = province
        self.postal_code = postal_code


class ClientList:
    def __init__(self):
        self.list = []
