import tkinter as tk
from tkinter import ttk, messagebox
from transaction import Transaction
import json
import os

DATA_FILE = "data/transactions.json"

class TransactionEntryFrame(ttk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True)
        self.build_form()

    def build_form(self):
        default_font = ("Segoe UI", 11)
        heading_font = ("Arial", 25, "bold")

        ttk.Label(self, text="Add New Transaction", font=heading_font).grid(row=0, column=0, columnspan=2, pady=10)

        # Type (income/expense) — dropdown
        ttk.Label(self, text="Type:", font=default_font).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(self, textvariable=self.type_var, state="readonly", font=default_font)
        self.type_dropdown["values"] = ("income", "expense")
        self.type_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.type_dropdown.set("expense")  # default

        # Fields (excluding type)
        fields = ["Date (DD-MM-YYYY)", "Amount", "Category", "Description"]
        self.entries = {}

        for i, field in enumerate(fields):
            label = ttk.Label(self, text=field, font=default_font)
            label.grid(row=i + 2, column=0, padx=10, pady=5, sticky="e")

            entry = ttk.Entry(self, width=30, font=default_font)
            entry.grid(row=i + 2, column=1, padx=10, pady=5, sticky="w")
            self.entries[field] = entry

        # Save button
        save_btn = ttk.Button(self, text="Save Transaction", command=self.save_transaction)
        save_btn.grid(row=len(fields) + 2, column=0, columnspan=2, pady=20, padx=10)

    def save_transaction(self):
        try:
            t = Transaction(
                date=self.entries["Date (DD-MM-YYYY)"].get(),
                amount=float(self.entries["Amount"].get()),
                category=self.entries["Category"].get(),
                t_type=self.type_var.get(),  # from dropdown
                description=self.entries["Description"].get()
            )
            if not t.is_valid():
                raise ValueError("Invalid transaction data.")

            self._save_to_file(t.to_dict())

            
            if self.controller:
                self.controller.frames["budget"].update_spending_from_transactions()

            messagebox.showinfo("Success", "Transaction saved successfully.")

            # Clear fields
            for entry in self.entries.values():
                entry.delete(0, tk.END)
            self.type_dropdown.set("expense")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save transaction:\n{e}")

    def _save_to_file(self, data):
        if not os.path.exists("data"):
            os.makedirs("data")

        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = []
        else:
            existing = []

        existing.append(data)
        with open(DATA_FILE, "w") as f:
            json.dump(existing, f, indent=4)
