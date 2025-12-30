import os
import webbrowser
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import date

from src.models.client import Client
from src.models.service import ServiceItem
from src.models.settings import Settings


FONT_PDF = "Helvetica"
TITLE_FONT_SIZE = 24
HEADER_FONT_SIZE = 15
FONT_SIZE = 11
IMAGE_LENGTH = 1.3 * inch


def create_invoice_pdf(path, settings: Settings, client: Client, services: list[ServiceItem]):
    business_info = [
        settings.business_owner,
        settings.business_street,
        f"{settings.business_city}, {settings.business_province}, {settings.business_postal_code}",
        settings.business_email,
    ]
    client_info = [
        client.name,
        client.street,
        f"{client.city}, {client.province}, {client.postal_code}",
        client.email,
    ]
    meta_data = {
        "HST Number": settings.hst_number,
        "License ID": settings.license_id,
    }

    items = []
    for service in services:
        items.append((service.service.name, service.quantity, service.service.price))

    c = canvas.Canvas(path, pagesize=LETTER)
    width, height = LETTER

    c.setTitle(f"Invoice - {settings.invoice_number} {client.name}.pdf")

    x_left = 1 * inch
    x_right = width - 2.5 * inch
    y = height - 1 * inch

    # Title
    c.setFont(f"{FONT_PDF}-Bold", TITLE_FONT_SIZE)
    c.drawString(x_left, y, settings.business_name)

    # Business info
    y -= TITLE_FONT_SIZE + HEADER_FONT_SIZE

    c.setFont(FONT_PDF, HEADER_FONT_SIZE)
    c.setFillColorRGB(0.7, 0.7, 0.7)
    c.drawString(x_left, y, "INVOICE")
    c.setFillColorRGB(0, 0, 0)
    c.setFont(FONT_PDF, FONT_SIZE)

    for line in business_info:
        y -= FONT_SIZE + 5
        c.drawString(x_left, y, line)

    # Issued to
    y -= (FONT_SIZE + 5) * 2
    c.setFont(f"{FONT_PDF}-Bold", FONT_SIZE)
    c.drawString(x_left, y, "Issued to")
    c.setFont(FONT_PDF, FONT_SIZE)

    for line in client_info:
        y -= FONT_SIZE + 5
        c.drawString(x_left, y, line)

    # Logo
    y_meta = height - 1 * inch
    if os.path.exists(settings.logo_path):
        y_meta -= IMAGE_LENGTH - TITLE_FONT_SIZE
        c.drawImage(
            settings.logo_path,
            width - IMAGE_LENGTH - inch,
            y_meta,
            width=IMAGE_LENGTH,
            height=IMAGE_LENGTH,
            preserveAspectRatio=True
        )
    else:
        y_meta -= TITLE_FONT_SIZE + HEADER_FONT_SIZE

    # Invoice meta (right side)
    y_meta -= FONT_SIZE * 2
    c.setFont(f"{FONT_PDF}-Bold", FONT_SIZE)
    c.drawString(x_right, y_meta, "Date Issued")
    c.setFont(FONT_PDF, FONT_SIZE)
    y_meta -= FONT_SIZE + 5
    c.drawString(x_right, y_meta, f"{date.today().strftime("%d. %B %Y")}")

    y_meta -= (FONT_SIZE + 2) * 2
    c.setFont(f"{FONT_PDF}-Bold", FONT_SIZE)
    c.drawString(x_right, y_meta, "Invoice Number")
    c.setFont(FONT_PDF, FONT_SIZE)
    y_meta -= FONT_SIZE + 5
    c.drawString(x_right, y_meta, str(settings.invoice_number))

    for label in meta_data.keys():
        y_meta -= (FONT_SIZE + 2) * 2
        c.setFont(f"{FONT_PDF}-Bold", FONT_SIZE)
        c.drawString(x_right, y_meta, label)
        c.setFont(FONT_PDF, FONT_SIZE)
        y_meta -= FONT_SIZE + 5
        c.drawString(x_right, y_meta, meta_data[label])

    # Table header
    y = min(y, y_meta) - FONT_SIZE * 4
    table_header_height = y
    c.setFont(f"{FONT_PDF}-Bold", FONT_SIZE)
    c.drawString(x_left, y, "Description")
    c.drawString(x_left + 260, y, "Qty")
    c.drawString(x_left + 310, y, "Amount")
    c.drawString(x_left + 390, y, "Total")

    c.setStrokeColor(colors.lightgrey)
    c.line(x_left, y - 10, width - inch, y - 10)

    # Line item
    c.setFont(FONT_PDF, FONT_SIZE)
    y -= 20 + FONT_SIZE
    subtotal = 0
    for item in items:
        total = item[1] * item[2]
        subtotal += total
        c.drawString(x_left, y, item[0])
        c.drawString(x_left + 260, y, str(item[1]))
        c.drawString(x_left + 310, y, f"CA${item[2]:.2f}")
        c.drawString(x_left + 390, y, f"CA${total:.2f}")
        y -= FONT_SIZE * 2
    y += FONT_SIZE * 2

    y = min(y, max(table_header_height - 200, inch + FONT_SIZE * 5))

    # Totals
    c.line(x_left, y - 10, width - inch, y - 10)
    y -= 15 + FONT_SIZE
    tax = round(subtotal * settings.tax_rate, 2)
    grand_total = subtotal + tax

    c.drawString(x_left + 310, y, "Subtotal")
    c.drawString(x_left + 390, y, f"CA${subtotal:.2f}")

    y -= FONT_SIZE * 1.7
    c.drawString(x_left + 310, y, f"Tax ({int(settings.tax_rate * 100)}%)")
    c.drawString(x_left + 390, y, f"CA${tax:.2f}")

    y -= FONT_SIZE * 1.7
    c.setFont(f"{FONT_PDF}-Bold", FONT_SIZE)
    c.drawString(x_left + 310, y, "Grand Total")
    c.drawString(x_left + 390, y, f"CA${grand_total:.2f}")

    c.line(x_left + 255, table_header_height + FONT_SIZE, x_left + 255, y)
    c.line(x_left + 305, table_header_height + FONT_SIZE, x_left + 305, y)
    c.line(x_left + 385, table_header_height + FONT_SIZE, x_left + 385, y)

    c.showPage()
    c.save()


# def preview_pdf():
#     temp_path = os.path.join(tempfile.gettempdir(), f"Invoice - {INVOICE_NUMBER} {CLIENT_ADDRESS[0]}.pdf")
#     create_invoice_pdf(temp_path)
#     webbrowser.open(temp_path)


def download_pdf(settings: Settings, client: Client, services: list[ServiceItem]):
    if settings.download_path is None:
        settings.download_path = filedialog.askdirectory(title="Select download folder")
        if not settings.download_path:
            return

    filename = f"Invoice - {settings.invoice_number} {client.name}.pdf"
    path = os.path.join(settings.download_path, filename)

    create_invoice_pdf(path, settings, client, services)
    webbrowser.open(path)
    messagebox.showinfo(
        "Saved",
        f"Invoice saved as:\n{filename}"
    )


# if __name__ == "__main__":
#     preview_pdf()
