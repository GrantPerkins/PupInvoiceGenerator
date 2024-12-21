import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.metrics import dp

from invoice_generator import InvoiceGenerator
from pup_invoice_data import PupInvoiceData


class InvoiceAppGUI(App):
    def build(self):
        self.title = "Kylee's K9s Invoice Generator"
        # Root layout
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add Heading at the top
        heading_label = Label(text="Invoice Generator", font_size=dp(24), bold=True, size_hint_y=None, height=dp(40))
        self.root.add_widget(heading_label)

        # Top form for Full Name and Address
        top_form = GridLayout(cols=2, spacing=10, size_hint_y=None, height=dp(250))
        top_form.add_widget(Label(text="Full Name:", size_hint_x=None, width=dp(100)))
        self.full_name_input = TextInput(hint_text="Enter full name", multiline=False)
        top_form.add_widget(self.full_name_input)
        top_form.add_widget(Label(text="Address:", size_hint_x=None, width=dp(100)))
        self.address_input = TextInput(hint_text="Enter address (can be multiple lines)", multiline=True, size_hint_y=None, height=dp(80))
        top_form.add_widget(self.address_input)
        top_form.add_widget(Label(text="Invoice Number:", size_hint_x=None, width=dp(100)))
        self.invoice_no_input = TextInput(hint_text="Enter invoice number", multiline=False)
        top_form.add_widget(self.invoice_no_input)
        top_form.add_widget(Label(text="Discount:", size_hint_x=None, width=dp(100)))
        self.discount_input = TextInput(hint_text="Enter discount (leave blank if none)", multiline=False, input_filter='float')
        top_form.add_widget(self.discount_input)

        self.root.add_widget(top_form)

        # Header layout
        header_layout = GridLayout(cols=5, spacing=5, size_hint_y=None, height=dp(40))
        headers = ['Description', 'Date', 'Hours', 'Total', 'Actions']
        for header in headers:
            header_layout.add_widget(Label(text=header, bold=True))
        self.root.add_widget(header_layout)

        # Scrollable table layout
        scroll_view = ScrollView(size_hint=(1, 1))
        self.table = GridLayout(cols=5, spacing=5, size_hint_y=None)
        self.table.bind(minimum_height=self.table.setter('height'))
        scroll_view.add_widget(self.table)

        # Add scrollable table to root layout
        self.root.add_widget(scroll_view)

        # Track rows
        self.rows = []
        self.add_row()  # Add an initial row

        # Bottom control layout
        control_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        add_button = Button(text="Add Row", size_hint=(None, None), size=(dp(150), dp(50)))
        add_button.bind(on_press=lambda x: self.add_row())
        submit_button = Button(text="Submit", size_hint=(None, None), size=(dp(150), dp(50)))
        submit_button.bind(on_press=lambda x: self.on_submit())

        control_layout.add_widget(add_button)
        control_layout.add_widget(submit_button)
        self.root.add_widget(control_layout)

        return self.root

    def add_row(self):
        # Add a new row of inputs
        row = {}
        row['description'] = TextInput(hint_text="Description", multiline=False)
        row['date'] = TextInput(hint_text="Date (YYYY-MM-DD)", multiline=False)
        row['hours'] = TextInput(hint_text="Hours", multiline=False, input_filter='float')
        row['total'] = TextInput(hint_text="Total", multiline=False, input_filter='float')

        for key in ['description', 'date', 'hours', 'total']:
            self.table.add_widget(row[key])

        # Add delete button for the row
        delete_button = Button(text="X", size_hint=(None, None), size=(dp(40), dp(40)))
        delete_button.bind(on_press=lambda instance: self.delete_row(row))
        self.table.add_widget(delete_button)
        row['delete_button'] = delete_button

        self.rows.append(row)
        self.table.height += dp(40)  # Adjust height for new row

    def delete_row(self, row):
        # Remove the row widgets
        for key in ['description', 'date', 'hours', 'total', 'delete_button']:
            self.table.remove_widget(row[key])
        self.rows.remove(row)
        self.table.height -= dp(40)  # Adjust height for deleted row

    def on_submit(self):
        # Print the full name and address
        full_name = self.full_name_input.text
        address = self.address_input.text
        discount = self.discount_input.text
        invoice_no = self.invoice_no_input.text
        try:
            data = PupInvoiceData(full_name, address, discount, invoice_no, self.rows)
            self.show_file_chooser(data)
        except:
            import traceback
            traceback.print_exc()
            self.show_error_popup()



    def show_error_popup(self):
        # Create a popup to show the saved file path
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="There is likely an empty box. Please review.", font_size=dp(16)))

        close_button = Button(text="Close", size_hint=(1, None), height=dp(50))
        content.add_widget(close_button)

        popup = Popup(title="Error",
                      content=content,
                      size_hint=(0.8, 0.4))

        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def show_file_chooser(self, data):
        # Get the path to the user's Downloads folder
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Create a popup for file saving
        content = BoxLayout(orientation='vertical', spacing=10)

        # Text input for file name
        self.file_name_input = TextInput(hint_text="Enter file name", multiline=False, size_hint_y=None, height=40)
        content.add_widget(self.file_name_input)

        # File chooser
        file_chooser = FileChooserListView(path=downloads_folder)
        content.add_widget(file_chooser)

        save_button = Button(text="Save", size_hint=(1, None), height=dp(50))
        cancel_button = Button(text="Cancel", size_hint=(1, None), height=dp(50))

        button_layout = BoxLayout(size_hint=(1, None), height=dp(50))
        button_layout.add_widget(save_button)
        button_layout.add_widget(cancel_button)

        content.add_widget(button_layout)

        popup = Popup(title="Select a file to save the PDF",
                      content=content,
                      size_hint=(0.9, 0.9))

        def save_file(instance):
            # Get the file name from the input field and use it
            file_name = self.file_name_input.text.strip() or "invoice"
            selected_path = file_chooser.path
            filename = os.path.join(selected_path, f"{file_name}.pdf")
            InvoiceGenerator(data, filename).build()
            self.show_file_path_popup(filename)  # Show the file path pop-up
            popup.dismiss()

        save_button.bind(on_press=save_file)
        cancel_button.bind(on_press=popup.dismiss)

        popup.open()

    def show_file_path_popup(self, file_path):
        # Create a popup to show the saved file path
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=f"File saved to:\n{file_path}", font_size=dp(16)))

        close_button = Button(text="Close", size_hint=(1, None), height=dp(50))
        content.add_widget(close_button)

        popup = Popup(title="File Saved",
                      content=content,
                      size_hint=(0.8, 0.4))

        close_button.bind(on_press=popup.dismiss)
        popup.open()


# Run the app
if __name__ == '__main__':
    InvoiceAppGUI().run()
