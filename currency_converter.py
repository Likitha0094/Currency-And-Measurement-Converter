import tkinter as tk
from tkinter import ttk
import requests

class CurrencyConverter:
    def __init__(self, url):
        self.data = self.get_data(url)
        self.currencies = self.data['rates']

    def get_data(self, url):
        response = requests.get(url)
        return response.json()

    def convert(self, from_currency, to_currency, amount):
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]
        amount = round(amount * self.currencies[to_currency], 4)
        return amount

class MeasurementConverter:
    def __init__(self):
        self.units = {
            'Length': {'meter': 1.0, 'kilometer': 1000.0, 'centimeter': 0.01, 'millimeter': 0.001, 'mile': 1609.34, 'yard': 0.9144, 'foot': 0.3048, 'inch': 0.0254},
            'Weight': {'kilogram': 1.0, 'gram': 0.001, 'milligram': 0.000001, 'pound': 0.453592, 'ounce': 0.0283495},
            'Volume': {'liter': 1.0, 'milliliter': 0.001, 'cubic meter': 1000.0, 'gallon': 3.78541, 'quart': 0.946353, 'pint': 0.473176, 'cup': 0.24, 'fluid ounce': 0.0295735}
        }
    
    def convert(self, category, from_unit, to_unit, amount):
        amount_in_base = amount * self.units[category][from_unit]
        converted_amount = amount_in_base / self.units[category][to_unit]
        return round(converted_amount, 4)

class ConverterApp:
    def __init__(self, currency_converter, measurement_converter):
        self.currency_converter = currency_converter
        self.measurement_converter = measurement_converter
        
        self.window = tk.Tk()
        self.window.title("Converter")
        self.window.geometry("700x600")
        self.tab_control = ttk.Notebook(self.window)
        
        self.currency_tab = ttk.Frame(self.tab_control)
        self.measurement_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.currency_tab, text="Currency Converter")
        self.tab_control.add(self.measurement_tab, text="Measurement Converter")
        self.tab_control.pack(expand=1, fill="both")
        
        self.create_currency_tab()
        self.create_measurement_tab()
        
    def create_currency_tab(self):
        intro_label = tk.Label(self.currency_tab, text="Currency Converter", fg="blue", relief=tk.RAISED, borderwidth=3)
        intro_label.config(font=('Courier', 24, 'bold'))
        intro_label.pack(pady=20)
        
        date_label = tk.Label(self.currency_tab, text=f"Date: {self.currency_converter.data['date']}", relief=tk.GROOVE, borderwidth=5)
        date_label.config(font=('Courier', 14))
        date_label.pack(pady=10)
        
        from_currency_variable = tk.StringVar(self.currency_tab)
        from_currency_variable.set("USD")
        to_currency_variable = tk.StringVar(self.currency_tab)
        to_currency_variable.set("INR")
        
        amount_field = tk.Entry(self.currency_tab, bd=3, relief=tk.RIDGE, justify=tk.CENTER, font=('Courier', 18))
        converted_amount_field_label = tk.Label(self.currency_tab, text='', fg='black', bg='white', relief=tk.RIDGE, justify=tk.CENTER, width=25, borderwidth=3, font=('Courier', 18))
        
        from_currency_dropdown = ttk.Combobox(self.currency_tab, textvariable=from_currency_variable, values=list(self.currency_converter.currencies.keys()), state='readonly', width=25, justify=tk.CENTER, font=('Courier', 14))
        to_currency_dropdown = ttk.Combobox(self.currency_tab, textvariable=to_currency_variable, values=list(self.currency_converter.currencies.keys()), state='readonly', width=25, justify=tk.CENTER, font=('Courier', 14))
        
        from_currency_dropdown.pack(pady=15)
        amount_field.pack(pady=15)
        to_currency_dropdown.pack(pady=15)
        converted_amount_field_label.pack(pady=15)
        
        convert_button = tk.Button(self.currency_tab, text="Convert", fg="black", command=lambda: self.perform_currency_conversion(from_currency_variable, to_currency_variable, amount_field, converted_amount_field_label), font=('Courier', 18))
        convert_button.pack(pady=15)
    
    def perform_currency_conversion(self, from_currency_variable, to_currency_variable, amount_field, converted_amount_field_label):
        try:
            amount = float(amount_field.get())
            from_curr = from_currency_variable.get()
            to_curr = to_currency_variable.get()
        
            converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
            converted_amount_field_label.config(text=str(converted_amount))
        except ValueError:
            converted_amount_field_label.config(text="Invalid input")
    
    def create_measurement_tab(self):
        intro_label = tk.Label(self.measurement_tab, text="Measurement Converter", fg="blue", relief=tk.RAISED, borderwidth=3)
        intro_label.config(font=('Courier', 24, 'bold'))
        intro_label.pack(pady=20)
        
        categories = list(self.measurement_converter.units.keys())
        category_variable = tk.StringVar(self.measurement_tab)
        category_variable.set(categories[0])
        
        from_unit_variable = tk.StringVar(self.measurement_tab)
        from_unit_variable.set(list(self.measurement_converter.units[categories[0]].keys())[0])
        to_unit_variable = tk.StringVar(self.measurement_tab)
        to_unit_variable.set(list(self.measurement_converter.units[categories[0]].keys())[1])
        
        amount_field = tk.Entry(self.measurement_tab, bd=3, relief=tk.RIDGE, justify=tk.CENTER, font=('Courier', 18))
        converted_amount_field_label = tk.Label(self.measurement_tab, text='', fg='black', bg='white', relief=tk.RIDGE, justify=tk.CENTER, width=25, borderwidth=3, font=('Courier', 18))
        
        category_dropdown = ttk.Combobox(self.measurement_tab, textvariable=category_variable, values=categories, state='readonly', width=25, justify=tk.CENTER, font=('Courier', 14))
        from_unit_dropdown = ttk.Combobox(self.measurement_tab, textvariable=from_unit_variable, values=list(self.measurement_converter.units[categories[0]].keys()), state='readonly', width=25, justify=tk.CENTER, font=('Courier', 14))
        to_unit_dropdown = ttk.Combobox(self.measurement_tab, textvariable=to_unit_variable, values=list(self.measurement_converter.units[categories[0]].keys()), state='readonly', width=25, justify=tk.CENTER, font=('Courier', 14))
        
        category_dropdown.pack(pady=15)
        from_unit_dropdown.pack(pady=15)
        amount_field.pack(pady=15)
        to_unit_dropdown.pack(pady=15)
        converted_amount_field_label.pack(pady=15)
        
        convert_button = tk.Button(self.measurement_tab, text="Convert", fg="black", command=lambda: self.perform_measurement_conversion(category_variable, from_unit_variable, to_unit_variable, amount_field, converted_amount_field_label), font=('Courier', 18))
        convert_button.pack(pady=15)
        
        category_variable.trace('w', lambda *args: self.update_units(category_variable, from_unit_variable, to_unit_variable, from_unit_dropdown, to_unit_dropdown))
    
    def update_units(self, category_variable, from_unit_variable, to_unit_variable, from_unit_dropdown, to_unit_dropdown):
        category = category_variable.get()
        units = list(self.measurement_converter.units[category].keys())
        from_unit_variable.set(units[0])
        to_unit_variable.set(units[1] if len(units) > 1 else units[0])
        from_unit_dropdown['values'] = units
        to_unit_dropdown['values'] = units
    
    def perform_measurement_conversion(self, category_variable, from_unit_variable, to_unit_variable, amount_field, converted_amount_field_label):
        try:
            amount = float(amount_field.get())
            category = category_variable.get()
            from_unit = from_unit_variable.get()
            to_unit = to_unit_variable.get()
        
            converted_amount = self.measurement_converter.convert(category, from_unit, to_unit, amount)
            converted_amount_field_label.config(text=str(converted_amount))
        except ValueError:
            converted_amount_field_label.config(text="Invalid input")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    currency_url = 'https://api.exchangerate-api.com/v4/latest/USD'
    currency_converter = CurrencyConverter(currency_url)
    measurement_converter = MeasurementConverter()
    app = ConverterApp(currency_converter, measurement_converter)
    app.run()