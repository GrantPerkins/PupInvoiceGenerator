from datetime import datetime, timedelta


class PupInvoiceData:
    def __init__(self, name, address, discount, invoice_no, rows):
        self.name = name
        self.address = address.strip()
        self.discount = discount.strip()
        self.invoice_no = invoice_no.strip()
        self.date = datetime.today()
        self.due_date = (self.date + timedelta(days=5)).strftime('%m-%d-%Y')
        self.date = self.date.strftime('%m-%d-%Y')
        self.items = []
        for row in rows:
            self.items.append(PupInvoiceItem(row))

class PupInvoiceItem:
    def __init__(self, row):
        self.description = row['description'].text.strip()
        self.date = row['date'].text.strip()
        self.hours = row['hours'].text.strip()
        self.total = row['total'].text.strip()
        self.row_list = [self.description, self.date, self.hours, f"{float(self.total):.2f}"]


if __name__ == '__main__':
    from collections import namedtuple
    from invoice_generator import InvoiceGenerator

    MockItem = namedtuple('mockItem', 'text')
    mock_row = {"description": MockItem("Description"), "date": MockItem("12/1/24"), "hours": MockItem("5"),
                "total": MockItem("6")}
    test_data = PupInvoiceData('Grant 2 Perkins', "4455 Interlake Ave N, Seattle WA\n98103", 30, "001", [mock_row for i in range(10)])
    inv = InvoiceGenerator(test_data, "test.pdf")
    inv.build()
