# Invoice Generator

A lightweight desktop application for creating invoices with saved clients, services, and business settings.  
Built with **Python and Tkinter**, and packaged as a standalone executable so it can be run without installing Python or an IDE.

---

## How to Run

### Run the executable

1. Go to the **Releases** section on GitHub
2. Download the latest `.exe`
3. Double-click to run
4. Enter business information on first installation 

---

## Features

- **Client management**
  - Add, edit, and delete clients
  - Auto-fill client details when searching for an existing client
- **Service management**
  - Maintain a reusable list of services with prices
  - Add services to an invoice with quantity controls
- **Invoice creation**
  - Create formatted invoice PDF
  - Automatic subtotal, tax, and total calculation
  - Incrementing invoice numbers
- **Business settings**
  - Store business information, tax rate, logo, and default download location
- **PDF export**
  - Generate invoices as PDFs and save them to a chosen folder
- **Standalone executable**
  - Runs without requiring Python to be installed

---

## Pages Overview

- **Main Page**
  - Select a client
  - Add services to the invoice
  - View totals and export to PDF
- **Client Page**
  - Scrollable table of clients
  - Add, edit, and remove clients
- **Service Page**
  - Manage available services and prices
- **Settings Page**
  - Configure business information and invoice defaults
  - File and folder selection for logos and downloads

---

## How It Works (Technical Overview)

### Architecture

The application is structured to keep responsibilities clearly separated:

- **Models** - Plain Python objects (Client, Service, Settings) that represent data and contain no UI logic.
- **Repositories** - Handle loading and saving data using JSON files.
- **UI Pages** - Tkinter frames responsible for layout and user interaction.
- **App Controller** - Manages page navigation and shared state.

This structure keeps the UI independent from persistence and business logic.

---

## Dynamic Forms Using Field Definitions

Models define their fields using metadata:

```python
FIELDS = [
    ("business_name", "Business Name", "entry"),
    ("logo_path", "Logo Path", "file"),
    ...
]
```

This allows:

- Easy flexibility in model attributes
- Automatic form generation
- Consistent validation
- Less duplicated UI code

---

## Invoice PDF Generation

Invoices are generated programmatically using:

- Selected client data
- Selected services and quantities
- Stored business settings

Invoice numbers are automatically incremented after each save.

---

## Data Storage

All data is stored locally in C:\Users\\<username\>\AppData\Local\InvoiceGenerator\ using JSON and CSV files:

- client_list.csv
- service_list.csv
- settings.json

This makes the application portable and easy to update.

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.


---

## Windows Defender Warning

When running the executable for the first time, Windows may display a "Windows protected your PC" warning.

This happens because the application is not code-signed and is distributed as a standalone executable.

To run the application:
1. Click **More info**
2. Click **Run anyway**

The source code is fully available in this repository.

---

## Limitations

- Designed for single-user, local use
- No database or cloud synchronization
- No concurrent editing support

---

## Notes

This project focuses on:

- Clean separation of UI, data, and persistence
- Managing non-trivial Tkinter layouts
- Building reusable UI components
- Packaging Python desktop applications for end users
