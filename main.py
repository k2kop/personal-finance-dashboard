import tkinter as tk
from tkinter import ttk
from dashboard_frame import ReportFrame
from transaction_entry_frame import TransactionEntryFrame 
from budget_frame import BudgetFrame  
from exchange_rate_frame import ExchangeRateFrame
from budget_alert_frame import BudgetAlertFrame
from transaction_history_frame import TransactionHistoryFrame

class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Dashboard")
        self.geometry("1200x800")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # === MENU BAR ===
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        nav_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=nav_menu)
        nav_menu.add_command(label="Dashboard", command=lambda: self.show_frame("report"))
        nav_menu.add_command(label="Add Transaction", command=lambda: self.show_frame("transaction"))
        nav_menu.add_command(label="Transaction History", command=lambda: self.show_frame("history"))
        nav_menu.add_command(label="Set Budget", command=lambda: self.show_frame("budget"))
        nav_menu.add_command(label="Send Alert", command=lambda: self.show_frame("alert"))
        nav_menu.add_command(label="Exchange Rate", command=lambda: self.show_frame("exchange"))
        nav_menu.add_separator()
        nav_menu.add_command(label="Exit", command=self.quit)

        # === MAIN CONTAINER FOR FRAMES ===
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {
            "report": ReportFrame(self.container),
            "transaction": TransactionEntryFrame(self.container, controller=self),
            "budget": BudgetFrame(self.container),
            "exchange": ExchangeRateFrame(self.container),
            "alert": BudgetAlertFrame(self.container),
            "history": TransactionHistoryFrame(self.container),
        }

        for frame in self.frames.values():
            frame.pack_forget()

        self.show_frame("report")  # Show default frame

    def show_frame(self, name):
        for f in self.frames.values():
            f.pack_forget()
            
        frame = self.frames[name]
        frame.pack(fill="both", expand=True)
        if hasattr(frame, 'on_show'):
            frame.on_show()
            
        if name == "budget" and hasattr(self.frames[name], "load_budgets"):
            self.frames[name].load_budgets()
            
        frame.pack(fill="both", expand=True)
        
    def on_close(self):
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()
