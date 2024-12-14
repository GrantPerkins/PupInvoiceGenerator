from reportlab.lib.pagesizes import letter
from reportlab.lib import colors, utils
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from pup_invoice_data import PupInvoiceData


class InvoiceGenerator:
    def __init__(self, invoice_data: PupInvoiceData, filename: str):
        self.invoice_data = invoice_data
        self.invoice_issue_headers = ['Issued To:', 'Invoice No:', "#"+self.invoice_data.invoice_no]
        self.invoice_table_headers = ['Description', 'Date', 'Hours', 'Price']
        self.total_table_headers = ['Total', '', '', 'Price']
        self.document = SimpleDocTemplate(filename, pagesize=letter, author="Kylee Rutkiewicz",
                                          title="Kylee's K9s Invoice")

        self.invoice_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # No grid, only borders under header
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # Border only under the header
        ])

        self.styles = getSampleStyleSheet()

    def make_heading(self):
        heading = Paragraph("Kylee's K9s Invoice", self.styles['Title'])
        return heading

    def make_invoice_issue_table(self):
        info_data = [
            self.invoice_issue_headers,
            [self.invoice_data.name, 'Date:', self.invoice_data.date],
            [self.invoice_data.address, 'Due date:', self.invoice_data.due_date]
        ]

        page_width = letter[0] * 0.85
        num_columns_main_table = len(info_data[0])  # Number of columns in the main table
        column_width = page_width / num_columns_main_table  # Divide total width by number of columns

        # Create the main table with full width columns
        table = Table(info_data, colWidths=[column_width] * num_columns_main_table)
        table.setStyle(self.invoice_table_style)
        return table

    def make_kylee_table(self):
        info_data = [
            ['Pay To:', 'Venmo:', self.make_venmo_message()],
            ['Kylee Rutkiewicz', '', ''],
            ["Kylee's K9s LLC", '', ''],
        ]

        page_width = letter[0] * 0.85
        num_columns_main_table = len(info_data[0])  # Number of columns in the main table
        column_width = page_width / num_columns_main_table  # Divide total width by number of columns

        # Create the main table with full width columns
        table = Table(info_data, colWidths=[column_width] * num_columns_main_table)
        table.setStyle(self.invoice_table_style)
        return table

    def make_invoice_table(self):
        data = [
            self.invoice_table_headers
        ]
        for row in self.invoice_data.items:
            data.append(row.row_list)

        page_width = letter[0] * 0.85
        num_columns_main_table = len(data[0])  # Number of columns in the main table
        column_width = page_width / num_columns_main_table  # Divide total width by number of columns

        # Create the main table with full width columns
        table = Table(data, colWidths=[column_width] * num_columns_main_table)
        table.setStyle(self.invoice_table_style)
        return table

    def make_total_table(self):
        data = [
            self.total_table_headers
        ]
        total = 0
        for row in self.invoice_data.items:
            total += float(row.total)

        if self.invoice_data.discount is not None and float(self.invoice_data.discount) > 0:
            data.append(["", "", "Subtotal:", f"{total:.2f}"])
            data.append(["", "", "Discount:", f"-{float(self.invoice_data.discount):.2f}"])
            total -= float(self.invoice_data.discount)

        data.append(['', '', 'Grand Total:', f'${total:.2f}'])

        page_width = letter[0] * 0.85
        num_columns_main_table = len(data[0])  # Number of columns in the main table
        column_width = page_width / num_columns_main_table  # Divide total width by number of columns

        # Create the main table with full width columns
        table = Table(data, colWidths=[column_width] * num_columns_main_table)
        table.setStyle(self.invoice_table_style)
        return table

    def make_space(self):
        return Paragraph("<br/><br/>", self.styles['Normal'])

    def make_venmo_message(self):
        text = '<link href="https://www.venmo.com/u/Kylee-Rutkiewicz">@Kylee-Rutkiewicz</link>'
        link_style = ParagraphStyle(
            'LinkStyle',
            parent=self.styles['Normal'],
            textColor=colors.blue,  # Set text color to blue
            underline=True,  # Underline the text
            alignment=1
        )

        # Create the paragraph with the link
        return Paragraph(text, style=link_style)

    def make_venmo(self):
        width = int(letter[0] * 1 / 3)
        img = utils.ImageReader("venmo.png")
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return Image("venmo.png", width=width, height=(width * aspect))

    def build(self):

        # Build the document with the table
        elements = [
            self.make_heading(),
            self.make_space(),
            self.make_invoice_issue_table(),
            self.make_space(),
            self.make_kylee_table(),
            self.make_space(),
            self.make_invoice_table(),
            self.make_space(),
            self.make_total_table(),
            self.make_space(),
            self.make_venmo_message(),
            self.make_space(),
            self.make_venmo()
        ]
        self.document.build(elements)

        print("Invoice PDF generated successfully.")
