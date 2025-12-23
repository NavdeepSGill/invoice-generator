class Client:
    FIELDS = [
        ("phone", "Phone Number"),
        ("name", "Name"),
        ("street", "Street"),
        ("city", "City"),
        ("province", "Province"),
        ("postal_code", "Postal Code"),
        ("email", "Email"),
    ]
    COLUMN_MINSIZES = {
        "phone": 10,
        "name": 10,
        "street": 10,
        "city": 10,
        "province": 10,
        "postal_code": 10,
        "email": 10,
    }

    def __init__(self,
                 phone: str,
                 name: str,
                 street: str,
                 city: str,
                 province: str,
                 postal_code: str,
                 email: str,):
        self.phone = phone
        self.name = name
        self.street = street
        self.city = city
        self.province = province
        self.postal_code = postal_code
        self.email = email

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return self.__dict__ == other.__dict__
