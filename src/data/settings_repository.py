import json
import os

from src.models.settings import Settings


class SettingsRepository:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> Settings | None:
        if not os.path.exists(self.path):
            return None

        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return Settings(
            business_name=data.get("business_name", ""),
            business_owner=data.get("business_owner", ""),
            business_street=data.get("business_street", ""),
            business_city=data.get("business_city", ""),
            business_province=data.get("business_province", ""),
            business_postal_code=data.get("business_postal_code", ""),
            business_email=data.get("business_email", ""),
            hst_number=data.get("hst_number", ""),
            license_id=data.get("license_id", ""),
            tax_rate=data.get("tax_rate", 0),
            invoice_number=data.get("invoice_number", 1),
            logo_path=data.get("logo_path"),
            download_path=data.get("download_path"),
        )

    def save(self, settings: Settings) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        data = {
            "business_name": settings.business_name,
            "business_owner": settings.business_owner,
            "business_street": settings.business_street,
            "business_city": settings.business_city,
            "business_province": settings.business_province,
            "business_postal_code": settings.business_postal_code,
            "business_email": settings.business_email,
            "hst_number": settings.hst_number,
            "license_id": settings.license_id,
            "tax_rate": settings.tax_rate,
            "invoice_number": settings.invoice_number,
            "logo_path": settings.logo_path,
            "download_path": settings.download_path,
        }

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def increment_invoice_number(self) -> None:
        settings = self.load()
        if settings is None:
            return

        settings.invoice_number += 1
        self.save(settings)
