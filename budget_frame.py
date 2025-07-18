import tkinter as tk
from tkinter import messagebox
import json
import os
import pandas as pd

BUDGET_FILE = "data/budgets.json"
TRANSACTION_FILE = "data/transactions.json"

class BudgetFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="📊 Budget Overview", font=("Arial", 14)).pack(pady=(10, 5))

        # 🔼 Top input row: category, limit, add
        input_frame = tk.Frame(self)
        input_frame.pack(pady=(5, 10))

        tk.Label(input_frame, text="Category:").grid(row=0, column=0, padx=2)
        self.category_entry = tk.Entry(input_frame, width=15)
        self.category_entry.grid(row=0, column=1, padx=2)

        tk.Label(input_frame, text="Limit (₦):").grid(row=0, column=2, padx=2)
        self.limit_entry = tk.Entry(input_frame, width=10)
        self.limit_entry.grid(row=0, column=3, padx=2)

        tk.Button(input_frame, text="➕ Add Budget", command=self.add_budget).grid(row=0, column=4, padx=5)

        # 📋 Listbox in the middle
        self.listbox = tk.Listbox(
            self, height=10, width=60, font=("Consolas", 11),
            selectmode=tk.SINGLE, selectbackground="blue", activestyle="none"
        )
        self.listbox.pack(pady=5)

        # 🔽 Bottom action row
        action_frame = tk.Frame(self)
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="🗑 Delete Selected", command=self.delete_selected_budget).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="🔄 Refresh", command=self.load_budgets).pack(side=tk.LEFT, padx=5)

        self.budgets = {}
        self.load_budgets()

    def calculate_spending(self):
        if not os.path.exists(TRANSACTION_FILE):
            return {}

        try:
            with open(TRANSACTION_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return {}
                data = json.loads(content)
        except Exception:
            return {}

        df = pd.DataFrame(data)
        if "type" not in df.columns or "category" not in df.columns or "amount" not in df.columns:
            return {}

        expenses = df[df["type"] == "expense"]
        spending = expenses.groupby("category")["amount"].sum().to_dict()
        return spending

    def load_budgets(self):
        self.listbox.delete(0, tk.END)
        self.budgets.clear()

        if os.path.exists(BUDGET_FILE):
            with open(BUDGET_FILE, "r") as f:
                self.budgets = json.load(f)

        spending = self.calculate_spending()

        for category in self.budgets:
            spent = spending.get(category, 0)
            self.budgets[category]["current_spending"] = spent

        for cat, data in self.budgets.items():
            label = f"{cat}: ₦{data['current_spending']:.2f} spent / ₦{data['limit']:.2f} limit"
            self.listbox.insert(tk.END, label)

        with open(BUDGET_FILE, "w") as f:
            json.dump(self.budgets, f, indent=4)

    def add_budget(self):
        category = self.category_entry.get().strip()
        limit = self.limit_entry.get().strip()

        if not category or not limit:
            messagebox.showerror("Missing Info", "Please provide both category and limit.")
            return

        try:
            limit = float(limit)
        except ValueError:
            messagebox.showerror("Invalid Input", "Limit must be a number.")
            return

        if os.path.exists(BUDGET_FILE):
            with open(BUDGET_FILE, "r") as f:
                budgets = json.load(f)
        else:
            budgets = {}

        if category in budgets:
            messagebox.showerror("Duplicate", "This category already exists.")
            return

        budgets[category] = {"limit": limit, "current_spending": 0}

        with open(BUDGET_FILE, "w") as f:
            json.dump(budgets, f, indent=4)

        self.category_entry.delete(0, tk.END)
        self.limit_entry.delete(0, tk.END)
        self.load_budgets()

    def delete_selected_budget(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a budget to delete.")
            return

        selected_text = self.listbox.get(selection[0])
        category = selected_text.split(":")[0].strip()

        confirm = messagebox.askyesno("Confirm", f"Delete budget for '{category}'?")
        if not confirm:
            return

        if category in self.budgets:
            del self.budgets[category]

        with open(BUDGET_FILE, "w") as f:
            json.dump(self.budgets, f, indent=4)

        self.load_budgets()
