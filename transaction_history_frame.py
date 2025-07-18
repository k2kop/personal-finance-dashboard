import tkinter as tk
from tkinter import ttk
import json
import os

TRANSACTION_FILE = "data/transactions.json"

class TransactionHistoryFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Title
        ttk.Label(self, text="Transaction History", font=("Arial", 25, "bold")).pack(pady=10)
        
        button_row = ttk.Frame(self)
        button_row.pack(pady=10)
        
        ttk.Button(self, text="Download as CSV", command=self.export_csv).pack(pady=10)
        ttk.Button(button_row, text="Refresh", command=self.load_transactions).pack(side="left", padx=5)
        

        # Treeview table
        self.tree = ttk.Treeview(self, columns=("Date", "Amount", "Category", "Type", "Description"), show="headings", height=15)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.load_transactions()

    def load_transactions(self):
        self.tree.delete(*self.tree.get_children())

        if not os.path.exists(TRANSACTION_FILE):
            return

        with open(TRANSACTION_FILE, "r") as f:
            try:
                transactions = json.load(f)
            except json.JSONDecodeError:
                transactions = []

        for txn in transactions:
            self.tree.insert("", "end", values=(
                txn.get("date", ""),
                f"₦{txn.get('amount', 0):,.2f}",
                txn.get("category", ""),
                txn.get("type", ""),
                txn.get("description", "")
            ))
            
    def export_csv(self):
        import csv
        from tkinter import filedialog

        if not os.path.exists(TRANSACTION_FILE):
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title="Save as CSV")
        if not file_path:
            return

        with open(TRANSACTION_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date", "Amount", "Category", "Type", "Description"])
            for txn in data:
                writer.writerow([
                    txn.get("date", ""),
                    txn.get("amount", ""),
                    txn.get("category", ""),
                    txn.get("type", ""),
                    txn.get("description", "")
                ])

