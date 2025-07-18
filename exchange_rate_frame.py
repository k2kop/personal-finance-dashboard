import tkinter as tk
from tkinter import ttk, messagebox
from exchange_rate import scrape_exchange_rate

CURRENCIES = [
    "USD", "NGN", "EUR", "GBP", "CAD", "AUD", "JPY", "CNY", "INR", "ZAR", "BRL",
    "KES", "GHS", "UGX", "TND", "EGP", "MAD", "XAF", "XOF"
]

class ExchangeRateFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        label_font = ("Segoe UI", 12)
        entry_font = ("Segoe UI", 12)

        ttk.Label(self, text="Currency Converter", font=("Arial", 20, "bold")).pack(pady=10)

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10)

        # From Currency
        ttk.Label(form_frame, text="From Currency", font=label_font).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.from_currency = ttk.Combobox(form_frame, values=CURRENCIES, font=entry_font, width=15, state="readonly")
        self.from_currency.set("USD")
        self.from_currency.grid(row=0, column=1, padx=10, pady=5)

        # To Currency
        ttk.Label(form_frame, text="To Currency", font=label_font).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.to_currency = ttk.Combobox(form_frame, values=CURRENCIES, font=entry_font, width=15, state="readonly")
        self.to_currency.set("NGN")
        self.to_currency.grid(row=1, column=1, padx=10, pady=5)

        # Amount
        ttk.Label(form_frame, text="Amount", font=label_font).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.amount_entry = ttk.Entry(form_frame, font=entry_font, width=20)
        self.amount_entry.insert(0, "1")
        self.amount_entry.grid(row=2, column=1, padx=10, pady=5)

        # Convert Button
        ttk.Button(self, text="Convert", command=self.convert).pack(pady=10)

        # Result Display
        self.result_label = ttk.Label(self, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

    def convert(self):
        base = self.from_currency.get()
        target = self.to_currency.get()
        try:
            amount = float(self.amount_entry.get())
            rate = scrape_exchange_rate(base, target)
            total = amount * rate
            self.result_label.config(text=f"{amount:.2f} {base} = {total:.2f} {target}")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {e}")
