import tkinter as tk
from tkinter import ttk
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

TRANSACTION_FILE = "data/transactions.json"

class ReportFrame(ttk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True)
        
        heading_font = ("Arial", 30, "bold")
        value_font = ("Segoe UI", 14, "bold")

        title = ttk.Label(self, text="Dashboard", font=heading_font)
        title.pack(pady=15)
        
        summary_frame = ttk.Frame(self)
        summary_frame.pack(pady=10)
        
        self.income_var = tk.StringVar()
        self.expense_var = tk.StringVar()
        self.balance_var = tk.StringVar()
        
        self._build_card(summary_frame, "Balance", self.balance_var, 0, value_font, "#e0f7fa")
        self._build_card(summary_frame, "Income", self.income_var, 1, value_font, "#e8f5e9")
        self._build_card(summary_frame, "Expenses", self.expense_var, 2, value_font, "#ffebee")

        self.summary_label = ttk.Label(self, text="", font=("Arial", 12))
        self.summary_label.pack(pady=5)

        self.chart_canvas = None  # Store reference to chart canvas
        self.refresh_button = None  # Store reference to refresh button

        self.refresh_dashboard()  # Initial load

    def refresh_dashboard(self):
        self.calculate_totals()
        self.build_chart()

    def build_chart(self):
        if not os.path.exists(TRANSACTION_FILE):
            self.summary_label.config(text="No transaction data available.")
            return

        with open(TRANSACTION_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

        income = sum(txn["amount"] for txn in data if txn["type"] == "income")
        expenses = sum(txn["amount"] for txn in data if txn["type"] == "expense")

        self.summary_label.config(
            text=f"Total Income: ₦{income:,.2f}   |   Total Expenses: ₦{expenses:,.2f}"
        )

        # Remove old chart if it exists
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
        if self.refresh_button:
            self.refresh_button.destroy()

        if income == 0 and expenses == 0:
            self.summary_label.config(text="No financial data to display yet.")
            return

        # Create pie chart
        labels = ["Income", "Expenses"]
        values = [income, expenses]
        colors = ["#90ee90", "#ff6b6b"]

        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
        ax.axis("equal")

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(pady=(10, 20))

        # Centered Refresh Button BELOW chart
        self.refresh_button = ttk.Button(self, text="Refresh Dashboard", command=self.refresh_dashboard)
        self.refresh_button.pack(pady=(0, 20))

    def _build_card(self, parent, title, var, column, value_font, bg_color):
        card = tk.Frame(parent, bg=bg_color, width=200, height=100, highlightbackground="#ccc", highlightthickness=1)
        card.grid(row=0, column=column, padx=10, ipadx=10, ipady=10)
        card.pack_propagate(False)

        tk.Label(card, text=title, bg=bg_color, font=("Arial", 12)).pack(anchor="n")
        tk.Label(card, textvariable=var, bg=bg_color, font=value_font).pack(anchor="center", expand=True)

    def calculate_totals(self):
        if not os.path.exists(TRANSACTION_FILE):
            self.income_var.set("₦0.00")
            self.expense_var.set("₦0.00")
            self.balance_var.set("₦0.00")
            return

        with open(TRANSACTION_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

        income = sum(txn["amount"] for txn in data if txn["type"] == "income")
        expenses = sum(txn["amount"] for txn in data if txn["type"] == "expense")
        balance = income - expenses

        self.income_var.set(f"₦{income:,.2f}")
        self.expense_var.set(f"₦{expenses:,.2f}")
        self.balance_var.set(f"₦{balance:,.2f}")
