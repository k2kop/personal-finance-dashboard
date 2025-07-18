import tkinter as tk
from tkinter import messagebox
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from decouple import config
from budget import Budget 
from pathlib import Path

BUDGET_FILE = "data/budgets.json"
TRANSACTION_FILE = "data/transactions.json"
SENDER_EMAIL = config("MY_EMAIL")
SENDER_PASSWORD = config("MY_PASSWORD")

class BudgetAlertFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Budget Alerts", font=("Arial", 25, "bold")).pack(pady=10)
        tk.Button(self, text="Refresh Budgets", command=self.load_budgets).pack(pady=(0, 10))

        self.budget_vars = {}
        self.budget_frame = tk.Frame(self)
        self.budget_frame.pack(pady=5)

        tk.Label(self, text="Recipient Email:").pack()
        self.email_entry = tk.Entry(self, width=40)
        self.email_entry.pack(pady=5)

        tk.Button(self, text="Send Selected Alerts", command=self.check_and_send_alert).pack(pady=10)

        self.load_budgets()

    def load_budgets(self):
        for widget in self.budget_frame.winfo_children():
            widget.destroy()
        self.budget_vars.clear()

        # Load budgets
        if not Path(BUDGET_FILE).exists():
            tk.Label(self.budget_frame, text="No budgets found.").pack()
            return

        with open(BUDGET_FILE, "r") as f:
            raw_data = json.load(f)
            budgets = {cat: Budget.from_dict(cat, b) for cat, b in raw_data.items()}

        # Load transactions
        if Path(TRANSACTION_FILE).exists():
            with open(TRANSACTION_FILE, "r") as f:
                content = f.read().strip()
                if content:
                    tx_data = json.loads(content)
                    df = pd.DataFrame(tx_data)
                else:
                    df = pd.DataFrame()
        else:
            df = pd.DataFrame()

        # Update spending
        if not df.empty and {"type", "category", "amount"}.issubset(df.columns):
            df = df[df["type"] == "expense"]
            for cat, b in budgets.items():
                b.current_spending = df[df["category"] == cat]["amount"].sum()
        else:
            for b in budgets.values():
                b.current_spending = 0

        # Display
        for category, b in budgets.items():
            label = f"{category}: ₦{b.current_spending:.2f} spent / ₦{b.limit:.2f} limit"
            var = tk.BooleanVar()
            self.budget_vars[category] = var
            tk.Checkbutton(self.budget_frame, text=label, variable=var).pack(anchor="w")

        # Cache it for sending alerts
        self.latest_budgets = budgets

    def check_and_send_alert(self):
        receiver_email = self.email_entry.get().strip()
        if not receiver_email:
            messagebox.showerror("Missing Info", "Please enter recipient email.")
            return

        if not hasattr(self, "latest_budgets"):
            messagebox.showerror("Error", "Budgets not loaded.")
            return

        selected = []
        for category, var in self.budget_vars.items():
            if var.get():
                b = self.latest_budgets[category]
                if b.current_spending >= b.limit:
                    selected.append((category, b.current_spending, b.limit))

        if not selected:
            messagebox.showinfo("Nothing to Send", "No selected budgets exceeded their limit.")
            return

        success = self.send_email(receiver_email, selected)
        if success:
            messagebox.showinfo("Success", "Alert email sent successfully!")
        else:
            messagebox.showerror("Error", "Failed to send email. Check your credentials or internet.")

    def send_email(self, to_email, exceeded_list):
        subject = "Budget Alert: Limit Exceeded"
        body = "The following selected budgets have been exceeded:\n\n"
        for cat, spent, limit in exceeded_list:
            body += f"{cat}: ₦{spent:.2f} spent / ₦{limit:.2f} limit\n"
        body += "\nPlease review your finances."

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        print("=== EMAIL DEBUG INFO ===")
        print("Sender:", SENDER_EMAIL)
        print("Receiver:", to_email)
        print("Subject:", subject)
        print("Body:\n", body)
        print("========================")

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                print("Connecting to Gmail...")
                server.starttls()
                print("Logging in...")
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                print("Sending message...")
                server.send_message(msg)
            print("Email sent successfully.")
            return True
        except Exception as e:
            print("Email failed:", e)
            return False
