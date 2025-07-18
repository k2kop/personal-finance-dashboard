import time
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

BUDGET_FILE = "data/budgets.json"
SENDER_EMAIL = config("MY_EMAIL")
SENDER_PASSWORD = config("MY_PASSWORD")

def load_budgets():
    if not os.path.exists(BUDGET_FILE):
        print("Budget file not found.")
        return {}
    with open(BUDGET_FILE, "r") as f:
        return json.load(f)

def select_budgets(budgets):
    print("\nAvailable Budgets:")
    keys = list(budgets.keys())
    for i, key in enumerate(keys, start=1):
        print(f"  {i}. {key}")

    selection = input("\nEnter the numbers of budgets to check (comma-separated): ")
    try:
        indices = [int(i.strip()) - 1 for i in selection.split(",")]
        selected = [keys[i] for i in indices if 0 <= i < len(keys)]
        return selected
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return []

def check_and_send_alerts():
    budgets = load_budgets()
    if not budgets:
        return

    selected = select_budgets(budgets)
    if not selected:
        print("No budgets selected.")
        return

    receiver_email = input("Enter recipient email address: ").strip()
    if not receiver_email:
        print("No recipient email entered.")
        return

    exceeded = []
    for category in selected:
        data = budgets.get(category)
        spent = data.get("current_spending", 0)
        limit = data.get("limit", 0)
        if spent >= limit:
            exceeded.append((category, spent, limit))

    if exceeded:
        send_email(receiver_email, exceeded)
    else:
        print("No selected budgets exceeded. No email sent.")

def send_email(to_email, exceeded_list):
    subject = "Budget Alert: Limit Exceeded"
    body = "The following budget categories have exceeded their limits:\n\n"
    for cat, spent, limit in exceeded_list:
        body += f"- {cat}: ₦{spent:.2f} spent / ₦{limit:.2f} limit\n"
    body += "\nPlease review your spending."

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    print("Attempting to send email...")
    time.sleep(3)
    print(f"To: {to_email}, From: {SENDER_EMAIL}")


    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("\nBudget alert email sent successfully!")
    except Exception as e:
        print(f"\nFailed to send email: {e}")

if __name__ == "__main__":
    check_and_send_alerts()
