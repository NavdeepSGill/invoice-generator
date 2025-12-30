class Settings:
    FIELDS = [
        ("business_name", "Business Name", "entry"),
        ("business_owner", "Owner Name", "entry"),
        ("business_street", "Street", "entry"),
        ("business_city", "City", "entry"),
        ("business_province", "Province", "entry"),
        ("business_postal_code", "Postal Code", "entry"),
        ("business_email", "Email", "entry"),
        ("hst_number", "HST Number", "entry"),
        ("license_id", "License ID", "entry"),
        ("tax_rate", "Tax Rate", "entry"),
        ("invoice_number", "Invoice Number", "entry"),
        ("logo_path", "Logo Path", "file"),
        ("download_path", "Download Path", "folder"),
    ]

    def __init__(self,
                 business_name: str,
                 business_owner: str,
                 business_street: str,
                 business_city: str,
                 business_province: str,
                 business_postal_code: str,
                 business_email: str,
                 hst_number: str,
                 license_id: str,
                 tax_rate: str,
                 invoice_number: str,
                 logo_path: str = None,
                 download_path: str = None
                 ):
        self.business_name = business_name
        self.business_owner = business_owner
        self.business_street = business_street
        self.business_city = business_city
        self.business_province = business_province
        self.business_postal_code = business_postal_code
        self.business_email = business_email
        self.hst_number = hst_number
        self.license_id = license_id
        self.tax_rate = float(tax_rate)
        self.invoice_number = int(invoice_number)
        self.logo_path = logo_path
        self.download_path = download_path
