import tkinter as tk
from tkinter import ttk, messagebox
import sys
from datetime import datetime, timedelta
import threading
import time


class GCashSystem:
    def __init__(self, name, phone_number, password):
        self.name = name
        self.phone_number = phone_number
        self.password = password
        self.balance = 0.00
        self.transaction_history = []
        
        # Transaction limits
        self.max_balance = 100000.00  # Maximum account balance
        self.daily_transfer_limit = 50000.00
        self.daily_withdrawal_limit = 20000.00
        self.min_transaction_amount = 1.00
        self.max_transaction_count_per_day = 10
        
        # Track daily transactions
        self.daily_transactions = {}
        self.daily_transfer_amount = 0.00
        self.daily_withdrawal_amount = 0.00

    def get_today_key(self):
        return datetime.now().strftime("%Y-%m-%d")

    def get_daily_transaction_count(self):
        today = self.get_today_key()
        return self.daily_transactions.get(today, 0)

    def increment_daily_transaction_count(self):
        today = self.get_today_key()
        self.daily_transactions[today] = self.daily_transactions.get(today, 0) + 1

    def check_daily_transaction_limit(self):
        if self.get_daily_transaction_count() >= self.max_transaction_count_per_day:
            return False, f"Daily transaction limit reached ({self.max_transaction_count_per_day} transactions)"
        return True, ""

    def reset_daily_limits_if_new_day(self):
        today = self.get_today_key()
        # Reset daily amounts if it's a new day
        if not hasattr(self, 'last_reset_date') or self.last_reset_date != today:
            self.daily_transfer_amount = 0.00
            self.daily_withdrawal_amount = 0.00
            self.last_reset_date = today

    def add_transaction(self, transaction_type, amount, details=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = f"[{timestamp}] {transaction_type}: ₱{amount:.2f} {details}"
        self.transaction_history.append(transaction)
        self.increment_daily_transaction_count()

    def animate_balance_change(self, widget, start_value, end_value, duration=1000):
        """Animate balance change with smooth transition"""
        steps = 20
        step_duration = duration // steps
        step_value = (end_value - start_value) / steps
        
        def update_step(step):
            if step <= steps:
                current_value = start_value + (step_value * step)
                widget.config(text=f"₱{current_value:.2f}")
                widget.after(step_duration, lambda: update_step(step + 1))
        
        update_step(0)

    def show_status_message(self, widget, message, color, duration=3000):
        """Show status message with fade effect"""
        widget.config(text=message, fg=color)
        widget.after(duration, lambda: widget.config(text=""))

    def show_balance(self):
        window = tk.Toplevel()
        window.title("Account Balance")
        window.geometry("400x800")
        window.config(bg="#0f1419")
        window.resizable(False, False)

        center_window(window, 400, 300)

        # Header
        header_frame = tk.Frame(window, bg="#1e2328", height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="💰 Account Balance",
            font=("Poppins", 16, "bold"),
            bg="#1e2328",
            fg="#ffffff",
        ).pack(expand=True)

        # Balance display
        balance_frame = tk.Frame(window, bg="#0f1419")
        balance_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            balance_frame,
            text="Current Balance:",
            font=("Poppins", 12),
            bg="#0f1419",
            fg="#8b949e",
        ).pack(pady=(20, 5))

        balance_label = tk.Label(
            balance_frame,
            text=f"₱{self.balance:.2f}",
            font=("Poppins", 24, "bold"),
            bg="#0f1419",
            fg="#2ea043",
        )
        balance_label.pack(pady=10)

        # Limits info
        limits_frame = tk.Frame(window, bg="#21262d")
        limits_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            limits_frame,
            text=f"Daily Transactions: {self.get_daily_transaction_count()}/{self.max_transaction_count_per_day}",
            font=("Poppins", 10),
            bg="#21262d",
            fg="#8b949e",
        ).pack(pady=5)

        tk.Label(
            limits_frame,
            text=f"Max Balance: ₱{self.max_balance:,.2f}",
            font=("Poppins", 10),
            bg="#21262d",
            fg="#8b949e",
        ).pack(pady=5)

    def deposit_money(self):
        window = tk.Toplevel()
        window.title("Deposit Money")
        window.geometry("400x400")
        window.config(bg="#0f1419")
        window.resizable(False, False)
        center_window(window, 400, 400)

        # Header
        header_frame = tk.Frame(window, bg="#1e2328", height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="💵 Deposit Money",
            font=("Poppins", 16, "bold"),
            bg="#1e2328",
            fg="#ffffff",
        ).pack(expand=True)

        # Limits info
        info_frame = tk.Frame(window, bg="#21262d")
        info_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            info_frame,
            text=f"Daily Transactions: {self.get_daily_transaction_count()}/{self.max_transaction_count_per_day}",
            font=("Poppins", 10),
            bg="#21262d",
            fg="#8b949e",
        ).pack(pady=5)

        tk.Label(
            info_frame,
            text=f"Min Amount: ₱{self.min_transaction_amount:.2f} | Max Balance: ₱{self.max_balance:,.2f}",
            font=("Poppins", 10),
            bg="#21262d",
            fg="#8b949e",
        ).pack(pady=5)

        # Input section
        input_frame = tk.Frame(window, bg="#0f1419")
        input_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            input_frame,
            text="Enter deposit amount:",
            font=("Poppins", 12),
            bg="#0f1419",
            fg="#ffffff",
        ).pack(anchor="w", pady=(0, 5))

        amount_entry = tk.Entry(
            input_frame,
            font=("Poppins", 14),
            bg="#21262d",
            fg="#ffffff",
            relief="flat",
            bd=0,
            insertbackground="#ffffff",
        )
        amount_entry.pack(fill="x", pady=(0, 10), ipady=8)
        amount_entry.focus()

        status_label = tk.Label(
            input_frame, text="", font=("Poppins", 10), bg="#0f1419"
        )
        status_label.pack(pady=10)

        # Progress bar (hidden initially)
        progress_bar = ttk.Progressbar(
            input_frame, 
            mode='indeterminate',
            length=300
        )

        def process_deposit():
            try:
                # Check daily transaction limit
                can_transact, limit_message = self.check_daily_transaction_limit()
                if not can_transact:
                    self.show_status_message(status_label, limit_message, "#f85149")
                    return

                amount = float(amount_entry.get())
                
                # Validate amount
                if amount < self.min_transaction_amount:
                    self.show_status_message(
                        status_label, 
                        f"Minimum deposit amount is ₱{self.min_transaction_amount:.2f}!", 
                        "#f85149"
                    )
                    return
                
                if self.balance + amount > self.max_balance:
                    self.show_status_message(
                        status_label, 
                        f"Deposit would exceed maximum balance of ₱{self.max_balance:,.2f}!", 
                        "#f85149"
                    )
                    return

                # Show processing animation
                progress_bar.pack(pady=10)
                progress_bar.start(10)
                status_label.config(text="Processing deposit...", fg="#1f6feb")
                
                # Simulate processing delay
                def complete_deposit():
                    progress_bar.stop()
                    progress_bar.pack_forget()
                    
                    old_balance = self.balance
                    self.balance += amount
                    self.add_transaction("Deposit", amount)
                    
                    self.show_status_message(
                        status_label,
                        f"Successfully deposited ₱{amount:.2f}!",
                        "#2ea043"
                    )
                    amount_entry.delete(0, tk.END)
                
                window.after(2000, complete_deposit)  # 2 second delay
                
            except ValueError:
                self.show_status_message(status_label, "Please enter a valid number!", "#f85149")

        # Buttons
        button_frame = tk.Frame(input_frame, bg="#0f1419")
        button_frame.pack(fill="x", pady=20)

        deposit_btn = tk.Button(
            button_frame,
            text="Deposit",
            command=process_deposit,
            font=("Poppins", 11, "bold"),
            bg="#238636",
            fg="white",
            relief="flat",
            padx=30,
            pady=8,
            cursor="hand2",
        )
        deposit_btn.pack(side="right", padx=(10, 0))

        tk.Button(
            button_frame,
            text="Cancel",
            command=window.destroy,
            font=("Poppins", 11),
            bg="#21262d",
            fg="white",
            relief="flat",
            padx=30,
            pady=8,
            cursor="hand2",
        ).pack(side="right")

        amount_entry.bind("<Return>", lambda e: process_deposit())

    def withdraw_money(self):
        self.reset_daily_limits_if_new_day()
        
        window = tk.Toplevel()
        window.title("Withdraw Money")
        window.config(bg="#0f1419")
        window.resizable(False, False)
        window.geometry("400x450")
        center_window(window, 400, 450)

        # Header
        header_frame = tk.Frame(window, bg="#1e2328", height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="💸 Withdraw Money",
            font=("Poppins", 16, "bold"),
            bg="#1e2328",
            fg="#ffffff",
        ).pack(expand=True)

        # Limits info
        info_frame = tk.Frame(window, bg="#21262d")
        info_frame.pack(fill="x", padx=20, pady=10)

        remaining_daily = self.daily_withdrawal_limit - self.daily_withdrawal_amount
        
        tk.Label(
            info_frame,
            text=f"Available Balance: ₱{self.balance:.2f}",
            font=("Poppins", 10),
            bg="#21262d",
            fg="#8b949e",
        ).pack(pady=2)

        tk.Label(
            info_frame,
            text=f"Daily Withdrawal Remaining: ₱{remaining_daily:.2f}",
            font=("Poppins", 10),
            bg="#21262d",
            fg="#8b949e",
        ).pack(pady=2)

        tk.Label(
            info_frame,
            text=f"Transactions Today: {self.get_daily_transaction_count()}/{self.max_transaction_count_per_day}",
            font=("Poppins", 10),
            bg="#21262d",
            fg="#8b949e",
        ).pack(pady=2)

        # Input section
        input_frame = tk.Frame(window, bg="#0f1419")
        input_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            input_frame,
            text="Enter withdrawal amount:",
            font=("Poppins", 12),
            bg="#0f1419",
            fg="#ffffff",
        ).pack(anchor="w", pady=(0, 5))

        amount_entry = tk.Entry(
            input_frame,
            font=("Poppins", 14),
            bg="#21262d",
            fg="#ffffff",
            relief="flat",
            bd=0,
            insertbackground="#ffffff",
        )
        amount_entry.pack(fill="x", pady=(0, 10), ipady=8)
        amount_entry.focus()

        status_label = tk.Label(
            input_frame, text="", font=("Poppins", 10), bg="#0f1419"
        )
        status_label.pack(pady=10)

        progress_bar = ttk.Progressbar(
            input_frame, 
            mode='indeterminate',
            length=300
        )

        def process_withdrawal():
            try:
                # Check daily transaction limit
                can_transact, limit_message = self.check_daily_transaction_limit()
                if not can_transact:
                    self.show_status_message(status_label, limit_message, "#f85149")
                    return

                amount = float(amount_entry.get())
                
                # Validate amount
                if amount < self.min_transaction_amount:
                    self.show_status_message(
                        status_label,
                        f"Minimum withdrawal amount is ₱{self.min_transaction_amount:.2f}!",
                        "#f85149"
                    )
                    return
                
                if amount > self.balance:
                    self.show_status_message(status_label, "Insufficient funds!", "#f85149")
                    return
                
                if self.daily_withdrawal_amount + amount > self.daily_withdrawal_limit:
                    remaining = self.daily_withdrawal_limit - self.daily_withdrawal_amount
                    self.show_status_message(
                        status_label,
                        f"Daily withdrawal limit exceeded! Remaining: ₱{remaining:.2f}",
                        "#f85149"
                    )
                    return

                # Show processing animation
                progress_bar.pack(pady=10)
                progress_bar.start(10)
                status_label.config(text="Processing withdrawal...", fg="#da3633")
                
                def complete_withdrawal():
                    progress_bar.stop()
                    progress_bar.pack_forget()
                    
                    self.balance -= amount
                    self.daily_withdrawal_amount += amount
                    self.add_transaction("Withdrawal", amount)
                    
                    self.show_status_message(
                        status_label,
                        f"Successfully withdrew ₱{amount:.2f}!",
                        "#2ea043"
                    )
                    amount_entry.delete(0, tk.END)
                
                window.after(2000, complete_withdrawal)
                
            except ValueError:
                self.show_status_message(status_label, "Please enter a valid number!", "#f85149")

        # Buttons
        button_frame = tk.Frame(input_frame, bg="#0f1419")
        button_frame.pack(fill="x", pady=20)

        tk.Button(
            button_frame,
            text="Withdraw",
            command=process_withdrawal,
            font=("Poppins", 11, "bold"),
            bg="#da3633",
            fg="white",
            relief="flat",
            padx=30,
            pady=8,
            cursor="hand2",
        ).pack(side="right", padx=(10, 0))

        tk.Button(
            button_frame,
            text="Cancel",
            command=window.destroy,
            font=("Poppins", 11),
            bg="#21262d",
            fg="white",
            relief="flat",
            padx=30,
            pady=8,
            cursor="hand2",
        ).pack(side="right")

        amount_entry.bind("<Return>", lambda e: process_withdrawal())

    def buy_load(self):
        window = tk.Toplevel()
        window.title("Buy Mobile Load")
        window.geometry("400x450")
        window.config(bg="#0f1419")
        window.resizable(False, False)
        center_window(window, 400, 450)

        # Header
        header_frame = tk.Frame(window, bg="#1e2328", height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="📱 Buy Mobile Load",
            font=("Poppins", 16, "bold"),
            bg="#1e2328",
            fg="#ffffff",
        ).pack(expand=True)

        # Service fee and limits info
        info_frame = tk.Frame(window, bg="#21262d")
        info_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            info_frame,
            text="Service fee: 2% of load amount",
            font=("Poppins", 10),
            bg="#21262d",
            fg="#8b949e",
        ).pack(pady=2)

        tk.Label(
            info_frame,
            text=f"Daily Transactions: {self.get_daily_transaction_count()}/{self.max_transaction_count_per_day}",
            font=("Poppins", 10),
            bg="#21262d",
            fg="#8b949e",
        ).pack(pady=2)

        # Input section
        input_frame = tk.Frame(window, bg="#0f1419")
        input_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            input_frame,
            text="Enter load amount:",
            font=("Poppins", 12),
            bg="#0f1419",
            fg="#ffffff",
        ).pack(anchor="w", pady=(0, 5))

        amount_entry = tk.Entry(
            input_frame,
            font=("Poppins", 14),
            bg="#21262d",
            fg="#ffffff",
            relief="flat",
            bd=0,
            insertbackground="#ffffff",
        )
        amount_entry.pack(fill="x", pady=(0, 10), ipady=8)
        amount_entry.focus()

        # Total calculation display
        total_frame = tk.Frame(input_frame, bg="#21262d", relief="flat", bd=1)
        total_frame.pack(fill="x", pady=10)

        total_label = tk.Label(
            total_frame,
            text="Total amount: ₱0.00",
            font=("Poppins", 11, "bold"),
            bg="#21262d",
            fg="#ffffff",
        )
        total_label.pack(pady=10)

        def calculate_total():
            try:
                amount = float(amount_entry.get() or 0)
                service_fee = amount * 0.02
                total = amount + service_fee
                total_label.config(
                    text=f"Load: ₱{amount:.2f} + Fee: ₱{service_fee:.2f} = Total: ₱{total:.2f}"
                )
            except ValueError:
                total_label.config(text="Total amount: ₱0.00")

        amount_entry.bind("<KeyRelease>", lambda e: calculate_total())

        status_label = tk.Label(
            input_frame, text="", font=("Poppins", 10), bg="#0f1419"
        )
        status_label.pack(pady=10)

        progress_bar = ttk.Progressbar(
            input_frame, 
            mode='indeterminate',
            length=300
        )

        def process_purchase():
            try:
                # Check daily transaction limit
                can_transact, limit_message = self.check_daily_transaction_limit()
                if not can_transact:
                    self.show_status_message(status_label, limit_message, "#f85149")
                    return

                amount = float(amount_entry.get())
                
                if amount < self.min_transaction_amount:
                    self.show_status_message(
                        status_label,
                        f"Minimum load amount is ₱{self.min_transaction_amount:.2f}!",
                        "#f85149"
                    )
                    return
                
                service_fee = amount * 0.02
                total_amount = amount + service_fee

                if total_amount > self.balance:
                    self.show_status_message(status_label, "Insufficient funds!", "#f85149")
                    return

                # Show processing animation
                progress_bar.pack(pady=10)
                progress_bar.start(10)
                status_label.config(text="Processing load purchase...", fg="#1f6feb")
                
                def complete_purchase():
                    progress_bar.stop()
                    progress_bar.pack_forget()
                    
                    self.balance -= total_amount
                    self.add_transaction("Mobile Load", amount, f"(Fee: ₱{service_fee:.2f})")
                    
                    self.show_status_message(
                        status_label,
                        f"Successfully purchased ₱{amount:.2f} load!",
                        "#2ea043"
                    )
                    amount_entry.delete(0, tk.END)
                    total_label.config(text="Total amount: ₱0.00")
                
                window.after(1500, complete_purchase)
                
            except ValueError:
                self.show_status_message(status_label, "Please enter a valid number!", "#f85149")

        # Buttons
        button_frame = tk.Frame(input_frame, bg="#0f1419")
        button_frame.pack(fill="x", pady=20)

        tk.Button(
            button_frame,
            text="Purchase Load",
            command=process_purchase,
            font=("Poppins", 11, "bold"),
            bg="#1f6feb",
            fg="white",
            relief="flat",
            padx=30,
            pady=8,
            cursor="hand2",
        ).pack(side="right", padx=(10, 0))

        tk.Button(
            button_frame,
            text="Cancel",
            command=window.destroy,
            font=("Poppins", 11),
            bg="#21262d",
            fg="white",
            relief="flat",
            padx=30,
            pady=8,
            cursor="hand2",
        ).pack(side="right")

        amount_entry.bind("<Return>", lambda e: process_purchase())

    def transfer_money(self, accounts):
        self.reset_daily_limits_if_new_day()
        
        window = tk.Toplevel()
        window.title("Transfer Money")
        window.geometry("450x500")
        window.config(bg="#0f1419")
        window.resizable(False, False)
        center_window(window, 450, 500)

        # Header
        header_frame = tk.Frame(window, bg="#1e2328", height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="💸 Transfer Money",
            font=("Poppins", 16, "bold"),
            bg="#1e2328",
            fg="#ffffff",
        ).pack(expand=True)

        # Limits info
        info_frame = tk.Frame(window, bg="#21262d")
        info_frame.pack(fill="x", padx=20, pady=10)

        remaining_daily = self.daily_transfer_limit - self.daily_transfer_amount

        tk.Label(
            info_frame,
            text=f"Daily Transfer Remaining: ₱{remaining_daily:.2f}",
            font=("Poppins", 10),
            bg="#21262d",
            fg="#8b949e",
        ).pack(pady=2)

        tk.Label(
            info_frame,
            text=f"Transactions Today: {self.get_daily_transaction_count()}/{self.max_transaction_count_per_day}",
            font=("Poppins", 10),
            bg="#21262d",
            fg="#8b949e",
        ).pack(pady=2)

        # Input section
        input_frame = tk.Frame(window, bg="#0f1419")
        input_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Recipient selection
        tk.Label(
            input_frame,
            text="Select recipient:",
            font=("Poppins", 12),
            bg="#0f1419",
            fg="#ffffff",
        ).pack(anchor="w", pady=(0, 5))

        recipient_var = tk.StringVar()
        recipient_combo = ttk.Combobox(
            input_frame,
            textvariable=recipient_var,
            font=("Poppins", 11),
            state="readonly",
        )

        recipient_options = []
        for acc in accounts:
            if acc != self:
                recipient_options.append(f"{acc.name} ({acc.phone_number})")

        recipient_combo["values"] = recipient_options
        recipient_combo.pack(fill="x", pady=(0, 15), ipady=5)

        # Amount input
        tk.Label(
            input_frame,
            text="Enter amount to transfer:",
            font=("Poppins", 12),
            bg="#0f1419",
            fg="#ffffff",
        ).pack(anchor="w", pady=(0, 5))

        amount_entry = tk.Entry(
            input_frame,
            font=("Poppins", 14),
            bg="#21262d",
            fg="#ffffff",
            relief="flat",
            bd=0,
            insertbackground="#ffffff",
        )
        amount_entry.pack(fill="x", pady=(0, 10), ipady=8)

        status_label = tk.Label(
            input_frame, text="", font=("Poppins", 10), bg="#0f1419"
        )
        status_label.pack(pady=10)

        progress_bar = ttk.Progressbar(
            input_frame, 
            mode='indeterminate',
            length=300
        )

        def process_transfer():
            try:
                # Check daily transaction limit
                can_transact, limit_message = self.check_daily_transaction_limit()
                if not can_transact:
                    self.show_status_message(status_label, limit_message, "#f85149")
                    return

                if not recipient_var.get():
                    self.show_status_message(status_label, "Please select a recipient!", "#f85149")
                    return

                amount = float(amount_entry.get())
                
                if amount < self.min_transaction_amount:
                    self.show_status_message(
                        status_label,
                        f"Minimum transfer amount is ₱{self.min_transaction_amount:.2f}!",
                        "#f85149"
                    )
                    return
                
                if amount > self.balance:
                    self.show_status_message(status_label, "Insufficient funds!", "#f85149")
                    return
                
                if self.daily_transfer_amount + amount > self.daily_transfer_limit:
                    remaining = self.daily_transfer_limit - self.daily_transfer_amount
                    self.show_status_message(
                        status_label,
                        f"Daily transfer limit exceeded! Remaining: ₱{remaining:.2f}",
                        "#f85149"
                    )
                    return

                # Find recipient account
                recipient = None
                for acc in accounts:
                    if f"{acc.name} ({acc.phone_number})" == recipient_var.get():
                        recipient = acc
                        break

                if not recipient:
                    self.show_status_message(status_label, "Recipient not found!", "#f85149")
                    return

                # Show processing animation
                progress_bar.pack(pady=10)
                progress_bar.start(10)
                status_label.config(text="Processing transfer...", fg="#1f6feb")
                
                def complete_transfer():
                    progress_bar.stop()
                    progress_bar.pack_forget()
                    
                    self.balance -= amount
                    recipient.balance += amount
                    self.daily_transfer_amount += amount
                    
                    self.add_transaction("Transfer Out", amount, f"to {recipient.name}")
                    recipient.add_transaction("Transfer In", amount, f"from {self.name}")
                    
                    self.show_status_message(
                        status_label,
                        f"Successfully transferred ₱{amount:.2f}!",
                        "#2ea043"
                    )
                    amount_entry.delete(0, tk.END)
                    recipient_combo.set("")
                
                window.after(2500, complete_transfer)

            except ValueError:
                self.show_status_message(status_label, "Please enter a valid number!", "#f85149")

        # Buttons
        button_frame = tk.Frame(input_frame, bg="#0f1419")
        button_frame.pack(fill="x", pady=20)

        tk.Button(
            button_frame,
            text="Transfer",
            command=process_transfer,
            font=("Poppins", 11, "bold"),
            bg="#1f6feb",
            fg="white",
            relief="flat",
            padx=30,
            pady=8,
            cursor="hand2",
        ).pack(side="right", padx=(10, 0))

        tk.Button(
            button_frame,
            text="Cancel",
            command=window.destroy,
            font=("Poppins", 11),
            bg="#21262d",
            fg="white",
            relief="flat",
            padx=30,
            pady=8,
            cursor="hand2",
        ).pack(side="right")

    def view_transactions(self):
        window = tk.Toplevel()
        window.title("Transaction History")
        window.geometry("700x600")
        window.config(bg="#0f1419")
        center_window(window, 700, 600)

        # Header
        header_frame = tk.Frame(window, bg="#1e2328", height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="📊 Transaction History",
            font=("Poppins", 16, "bold"),
            bg="#1e2328",
            fg="#ffffff",
        ).pack(expand=True)

        # Stats frame
        stats_frame = tk.Frame(window, bg="#21262d")
        stats_frame.pack(fill="x", padx=20, pady=10)

        today_count = self.get_daily_transaction_count()
        total_transactions = len(self.transaction_history)

        tk.Label(
            stats_frame,
            text=f"Total Transactions: {total_transactions} | Today: {today_count}/{self.max_transaction_count_per_day}",
            font=("Poppins", 11),
            bg="#21262d",
            fg="#8b949e",
        ).pack(pady=10)

        # Transaction list
        list_frame = tk.Frame(window, bg="#0f1419")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Scrollable text widget
        text_frame = tk.Frame(list_frame, bg="#0f1419")
        text_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(
            text_frame,
            font=("Courier New", 10),
            bg="#21262d",
            fg="#ffffff",
            yscrollcommand=scrollbar.set,
            relief="flat",
            bd=0,
            state="disabled",
        )
        text_widget.pack(fill="both", expand=True)

        scrollbar.config(command=text_widget.yview)

        # Populate transactions with color coding
        text_widget.config(state="normal")
        
        if self.transaction_history:
            for i, transaction in enumerate(self.transaction_history, 1):
                # Color code based on transaction type
                if "Deposit" in transaction:
                    text_widget.insert("end", f"{i:3d}. {transaction}\n", "deposit")
                elif "Withdrawal" in transaction or "Transfer Out" in transaction:
                    text_widget.insert("end", f"{i:3d}. {transaction}\n", "withdrawal")
                elif "Transfer In" in transaction:
                    text_widget.insert("end", f"{i:3d}. {transaction}\n", "transfer_in")
                else:
                    text_widget.insert("end", f"{i:3d}. {transaction}\n")
        else:
            text_widget.insert("end", "No transactions yet.\n")

        # Configure text tags for colors
        text_widget.tag_configure("deposit", foreground="#2ea043")
        text_widget.tag_configure("withdrawal", foreground="#f85149")
        text_widget.tag_configure("transfer_in", foreground="#1f6feb")
        
        text_widget.config(state="disabled")


def center_window(window, width, height):
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def fade_in_window(window, steps=10):
    """Create a fade-in effect for windows"""
    try:
        window.attributes('-alpha', 0.0)
        for i in range(steps + 1):
            alpha = i / steps
            window.attributes('-alpha', alpha)
            window.update()
            time.sleep(0.03)
    except:
        # If transparency is not supported, just show the window normally
        window.attributes('-alpha', 1.0)


def create_login_window():
    def authenticate():
        phone = phone_entry.get()
        password = password_entry.get()

        for account in accounts:
            if account.phone_number == phone and account.password == password:
                # Show loading animation
                login_btn.config(text="Logging in...", state="disabled")
                progress_login.pack(pady=10)
                progress_login.start(10)
                
                def complete_login():
                    progress_login.stop()
                    login_window.destroy()
                    create_main_window(account)
                
                login_window.after(1500, complete_login)
                return

        messagebox.showerror("Login Failed", "Invalid phone number or password!")

    login_window = tk.Tk()
    login_window.title("GCash Banking System - Login")
    login_window.config(bg="#0f1419")
    login_window.resizable(False, False)
    center_window(login_window, 450, 800)
    login_window.geometry("450x800")

    # Apply fade-in effect
    threading.Thread(target=lambda: fade_in_window(login_window), daemon=True).start()

    # Header
    header_frame = tk.Frame(login_window, bg="#0f1419")
    header_frame.pack(fill="x", padx=40, pady=40)

    tk.Label(
        header_frame,
        text="GCash Banking System",
        font=("Poppins", 24, "bold"),
        bg="#0f1419",
        fg="#ffffff",
    ).pack()

    tk.Label(
        header_frame,
        text="Secure Mobile Banking with Smart Limits",
        font=("Poppins", 12),
        bg="#0f1419",
        fg="#8b949e",
    ).pack(pady=(5, 0))

    # Login form
    form_frame = tk.Frame(login_window, bg="#0f1419")
    form_frame.pack(fill="both", expand=True, padx=40)

    # Phone number
    tk.Label(
        form_frame,
        text="Phone Number:",
        font=("Poppins", 12),
        bg="#0f1419",
        fg="#ffffff",
    ).pack(anchor="w", pady=(0, 5))

    phone_entry = tk.Entry(
        form_frame,
        font=("Poppins", 14),
        bg="#21262d",
        fg="#ffffff",
        relief="flat",
        bd=0,
        insertbackground="#ffffff",
    )
    phone_entry.pack(fill="x", pady=(0, 20), ipady=10)
    phone_entry.insert(0, "+63: ")

    # Password
    tk.Label(
        form_frame, text="Password:", font=("Poppins", 12), bg="#0f1419", fg="#ffffff"
    ).pack(anchor="w", pady=(0, 5))

    password_entry = tk.Entry(
        form_frame,
        font=("Poppins", 14),
        bg="#21262d",
        fg="#ffffff",
        relief="flat",
        bd=0,
        show="●",
        insertbackground="#ffffff",
    )
    password_entry.pack(fill="x", pady=(0, 30), ipady=10)

    # Login button
    login_btn = tk.Button(
        form_frame,
        text="Login",
        command=authenticate,
        font=("Poppins", 12, "bold"),
        bg="#1f6feb",
        fg="white",
        relief="flat",
        bd=0,
        cursor="hand2",
    )
    login_btn.pack(fill="x", ipady=12, pady=(0, 20))

    # Progress bar for login (hidden initially)
    progress_login = ttk.Progressbar(
        form_frame,
        mode='indeterminate',
        length=300
    )

    # Demo accounts info
    info_frame = tk.Frame(login_window, bg="#21262d")
    info_frame.pack(fill="x", padx=40, pady=(0, 40))

    tk.Label(
        info_frame,
        text="🔥 Enhanced Features:",
        font=("Poppins", 11, "bold"),
        bg="#21262d",
        fg="#ffffff",
    ).pack(pady=(10, 5))

    features = [
        "• Daily transaction limits (10 transactions/day)",
        "• Maximum balance cap (₱100,000)",
        "• Daily withdrawal limit (₱20,000)",
        "• Daily transfer limit (₱50,000)",
        "• Smooth loading animations",
        "• Enhanced security checks"
    ]

    for feature in features:
        tk.Label(
            info_frame,
            text=feature,
            font=("Poppins", 9),
            bg="#21262d",
            fg="#8b949e",
        ).pack(anchor="w", padx=10)

    tk.Label(
        info_frame,
        text="Demo Accounts:",
        font=("Poppins", 10, "bold"),
        bg="#21262d",
        fg="#ffffff",
    ).pack(pady=(15, 5))

    for account in accounts:
        tk.Label(
            info_frame,
            text=f"{account.name}: {account.phone_number} / {account.password}",
            font=("Poppins", 9),
            bg="#21262d",
            fg="#8b949e",
        ).pack()

    # Bind Enter key
    password_entry.bind("<Return>", lambda e: authenticate())
    phone_entry.focus()

    login_window.mainloop()


def create_main_window(account):
    main_window = tk.Tk()
    main_window.title("GCash Banking System")
    main_window.geometry("500x700")
    main_window.config(bg="#0f1419")
    main_window.resizable(False, False)
    center_window(main_window, 500, 700)

    # Apply fade-in effect
    threading.Thread(target=lambda: fade_in_window(main_window), daemon=True).start()

    # Header with user info
    header_frame = tk.Frame(main_window, bg="#1e2328")
    header_frame.pack(fill="x", padx=20, pady=20)

    tk.Label(
        header_frame,
        text=f"Welcome, {account.name}! 👋",
        font=("Poppins", 18, "bold"),
        bg="#1e2328",
        fg="#ffffff",
    ).pack(pady=10)

    tk.Label(
        header_frame,
        text=account.phone_number,
        font=("Poppins", 11),
        bg="#1e2328",
        fg="#8b949e",
    ).pack()

    # Quick balance display with animation capability
    balance_frame = tk.Frame(main_window, bg="#0f1419")
    balance_frame.pack(fill="x", padx=20, pady=10)

    balance_label = tk.Label(
        balance_frame,
        text=f"Balance: ₱{account.balance:.2f}",
        font=("Poppins", 14, "bold"),
        bg="#0f1419",
        fg="#2ea043",
    )
    balance_label.pack()

    # Daily limits status
    status_frame = tk.Frame(main_window, bg="#21262d")
    status_frame.pack(fill="x", padx=20, pady=10)

    def update_status_display():
        account.reset_daily_limits_if_new_day()
        daily_count = account.get_daily_transaction_count()
        remaining_transfer = account.daily_transfer_limit - account.daily_transfer_amount
        remaining_withdrawal = account.daily_withdrawal_limit - account.daily_withdrawal_amount
        
        status_text = f"Today: {daily_count}/{account.max_transaction_count_per_day} transactions"
        if daily_count >= account.max_transaction_count_per_day:
            status_text += " ⚠️ LIMIT REACHED"
        
        status_label.config(text=status_text)
        
        limits_text = f"Transfer: ₱{remaining_transfer:,.0f} | Withdrawal: ₱{remaining_withdrawal:,.0f}"
        limits_label.config(text=limits_text)

    status_label = tk.Label(
        status_frame,
        text="",
        font=("Poppins", 10),
        bg="#21262d",
        fg="#8b949e",
    )
    status_label.pack(pady=2)

    limits_label = tk.Label(
        status_frame,
        text="",
        font=("Poppins", 9),
        bg="#21262d",
        fg="#8b949e",
    )
    limits_label.pack(pady=2)

    def refresh_balance():
        balance_label.config(text=f"Balance: ₱{account.balance:.2f}")
        update_status_display()

    # Initial status update
    update_status_display()

    # Menu buttons
    menu_frame = tk.Frame(main_window, bg="#0f1419")
    menu_frame.pack(fill="both", expand=True, padx=20, pady=20)

    buttons_config = [
        ("💰 View Balance", account.show_balance),
        ("💵 Deposit Money", account.deposit_money),
        ("💸 Withdraw Money", account.withdraw_money),
        ("📱 Buy Load", account.buy_load),
        ("🔄 Transfer Money", lambda: account.transfer_money(accounts)),
        ("📊 Transaction History", account.view_transactions),
    ]

    for i, (text, command) in enumerate(buttons_config):
        btn = tk.Button(
            menu_frame,
            text=text,
            command=lambda cmd=command: [cmd(), refresh_balance()],
            font=("Poppins", 12),
            bg="#21262d",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            anchor="w",
            padx=20,
        )
        btn.pack(fill="x", pady=5, ipady=12)

        # Enhanced hover effects with color transitions
        def create_hover_effect(button):
            def on_enter(e):
                button.config(bg="#30363d")
            def on_leave(e):
                button.config(bg="#21262d")
            return on_enter, on_leave

        on_enter, on_leave = create_hover_effect(btn)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # Bottom buttons
    bottom_frame = tk.Frame(main_window, bg="#0f1419")
    bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

    tk.Button(
        bottom_frame,
        text="🔄 Switch Account",
        command=lambda: [main_window.destroy(), create_login_window()],
        font=("Poppins", 10),
        bg="#6f42c1",
        fg="white",
        relief="flat",
        padx=20,
        pady=8,
        cursor="hand2",
    ).pack(side="left")

    tk.Button(
        bottom_frame,
        text="🚪 Exit",
        command=sys.exit,
        font=("Poppins", 10),
        bg="#da3633",
        fg="white",
        relief="flat",
        padx=20,
        pady=8,
        cursor="hand2",
    ).pack(side="right")

    # Auto-refresh every 30 seconds
    def auto_refresh():
        refresh_balance()
        main_window.after(30000, auto_refresh)
    
    auto_refresh()

    main_window.mainloop()


# Initialize accounts with some sample data for testing
accounts = [
    GCashSystem("Adz", "+63: 936402438", "qwerty125"),
    GCashSystem("Guest", "+63: 12345", "222"),
]

# Add some sample balance for testing
accounts[0].balance = 5000.00
accounts[1].balance = 2500.00

# Start application
if __name__ == "__main__":
    create_login_window()