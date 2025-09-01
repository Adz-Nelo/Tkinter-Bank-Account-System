import tkinter as tk
import sys

class Gcash_System:
    def __init__(self, name, phone_number: str, password):
        self.name = name
        self.phone_number = phone_number
        self.password = password
        self.balance = 0.00
        self.transaction_history = []

    def clicked_balance(self):
        def show_balance():
            self.transaction_history.append(
                "Balance: ₱" + "{:.2f}".format(self.balance)
            )
            balance_value_label.config(
                text="Balance: ₱" + "{:.2f}".format(self.balance)
            )

        window_balance = tk.Toplevel()
        window_balance.title("Balance Menu")
        window_balance.geometry("200x125")
        window_balance.config(bg="#19bad3")

        balance_label = tk.Label(
            window_balance, text="Balance 🏦", font=("Roboto", 12), bg="#C0f0f6"
        )
        balance_label.pack()

        balance_button = tk.Button(
            window_balance,
            text="Refresh",
            font=("Roboto", 12),
            padx="2",
            pady="2",
            command=show_balance,
            bg="#Cfecf0",
        )
        balance_button.pack()

        balance_value_label = tk.Label(
            window_balance,
            text="Balance: ₱" + "{:.2f}".format(self.balance),
            font=("Roboto", 12),
            bg="#C0f0f6",
        )
        balance_value_label.pack()

    def clicked_cash_in(self):
        def deposit_amount():
            try:
                amount = float(show_deposit_entry.get())
                if amount < 0:
                    deposit_label.config(
                        text="Amount should not be negative! 🗙",
                        font=("Roboto", 12),
                        fg="red",
                    )
                else:
                    self.balance = self.balance + amount
                    self.transaction_history.append("Deposited: ₱{:.2f}".format(amount))
                    deposit_label.config(
                        text="Deposit successful! 💰", font=("Roboto", 12), fg="#2d7f2a"
                    )
            except ValueError:
                deposit_label.config(text="Please enter numbers only 😤.", fg="red")

        window_deposit = tk.Toplevel()
        window_deposit.title("Deposit Menu")
        window_deposit.geometry("250x110")
        window_deposit.config(bg="#19bad3")

        show_deposit = tk.Label(
            window_deposit, text="Deposit 💰", font=("Roboto", 12), bg="#C0f0f6"
        )
        show_deposit.pack()

        show_deposit_entry = tk.Entry(window_deposit, font=("Roboto", 12))
        show_deposit_entry.pack()

        show_deposit_button = tk.Button(
            window_deposit,
            text="Enter Amount",
            font=("Roboto", 12),
            bg="#Cfecf0",
            command=deposit_amount,
        )
        show_deposit_button.pack()

        deposit_label = tk.Label(
            window_deposit, text="", font=("Roboto", 12), bg="#19bad3"
        )
        deposit_label.pack()

    def clicked_cash_out(self):
        def withdraw_amount():
            try:
                amount = float(show_withdrawal_entry.get())
                if amount < 0:
                    withdraw_label.config(
                        text="Amount should not be negative! 🗙",
                        font=("Roboto", 12),
                        fg="red",
                    )
                elif self.balance >= amount:
                    self.balance = self.balance - amount
                    self.transaction_history.append("Cash out: ₱{:.2f}".format(amount))
                    withdraw_label.config(
                        text="Withdrawal successful! 💸",
                        font=("Roboto", 12),
                        fg="#2d7f2a",
                    )
                else:
                    withdraw_label.config(
                        text="Insufficient funds! 😢", font=("Roboto", 12), fg="red"
                    )
            except ValueError:
                withdraw_label.config(text="Please enter numbers only 😤.", fg="red")

        window_withdraw = tk.Toplevel()
        window_withdraw.title("Withdraw Menu")
        window_withdraw.geometry("250x110")
        window_withdraw.config(bg="#19bad3")

        show_withdrawal = tk.Label(
            window_withdraw, text="Withdraw Money 🤑", font=("Roboto", 12), bg="#C0f0f6"
        )
        show_withdrawal.pack()

        show_withdrawal_entry = tk.Entry(window_withdraw, font=("Roboto", 12))
        show_withdrawal_entry.pack()

        show_withdrawal_button = tk.Button(
            window_withdraw,
            text="Enter Amount",
            font=("Roboto", 12),
            bg="#Cfecf0",
            command=withdraw_amount,
        )
        show_withdrawal_button.pack()

        withdraw_label = tk.Label(
            window_withdraw, text="", font=("Roboto", 12), bg="#19bad3"
        )
        withdraw_label.pack()

    def clicked_buy_load(self):
        def purchase_load():
            try:
                amount2 = float(show_buy_load_entry.get())
                service_fee = amount2 * 0.02
                total_amount = amount2 + service_fee

                if amount2 < 0:
                    buy_load_label.config(
                        text="Amount should not be negative! 🗙",
                        font=("Roboto", 12),
                        fg="Red",
                    )

                elif self.balance >= total_amount:
                    self.balance = self.balance - total_amount
                    self.transaction_history.append(
                        "Load Purchased: ₱" + "{:.2f}".format(amount2)
                    )
                    buy_load_label.config(
                        text="Purchase successful! 💸",
                        font=("Roboto", 12),
                        fg="#2d7f2a",
                    )
                else:
                    buy_load_label.config(
                        text="Insufficient funds! 😢", font=("Roboto", 12), fg="red"
                    )
            except ValueError:
                buy_load_label.config(text="Please enter numbers only 😤.", fg="red")

        window_load = tk.Toplevel()
        window_load.title("Buy Load Menu")
        window_load.geometry("275x100")
        window_load.config(bg="#19bad3")

        show_load = tk.Label(
            window_load, text="Buy Load 📱", font=("Roboto", 12), bg="#C0f0f6"
        )
        show_load.pack()

        show_buy_load_entry = tk.Entry(window_load, font=("Roboto", 12))
        show_buy_load_entry.pack()

        show_buy_load_button = tk.Button(
            window_load,
            text="Purchase",
            font=("Roboto", 12),
            bg="#Cfecf0",
            command=purchase_load,
        )
        show_buy_load_button.pack()

        buy_load_label = tk.Label(
            window_load, text="", font=("Roboto", 12), bg="#19bad3"
        )
        buy_load_label.pack()

    def clicked_transfer_money(self, sender_acc, recipient_acc):
        def transfer_amount():
            try:
                recipient_num = str(enter_recipient_num_entry.get())
                amount = float(enter_amount_entry.get())

                if amount < 0:
                    enter_amount_label.config(
                        text="Amount should not be negative ❌", fg="Red", bg="#19bad3"
                    )

                elif (
                    recipient_num == "+63: 12345" and recipient_num == "+63: 936402438"
                ):
                    enter_recipient_num_label.config(
                        text="Phone Number Entry Success! ✔️", fg="Green", bg="#19bad3"
                    )

                elif (
                    recipient_num != "+63: 12345" and recipient_num != "+63: 936402438"
                ):
                    enter_recipient_num_label.config(
                        text="Invalid Phone Number ❌", fg="Red", bg="#19bad3"
                    )

                elif sender_acc.balance >= amount:
                    recipient_num == "+63: 12345"
                    sender_acc.balance -= amount
                    recipient_acc.balance += amount
                    sender_acc.transaction_history.append(
                        "Cash sent to "
                        + recipient_acc.name
                        + ": ₱"
                        + "{:.2f}".format(amount)
                    )
                    enter_recipient_num_label.config(
                        text="Phone Number Entry Success! ✔️", fg="Green", bg="#19bad3"
                    )

                    enter_amount_label.config(
                        text="Amount transferred successfully 💸",
                        fg="Green",
                        bg="#19bad3",
                    )

                elif recipient_acc.balance >= amount:
                    recipient_num == "+63: 936402438"
                    recipient_acc.balance -= amount
                    sender_acc.balance += amount
                    recipient_acc.transaction_history.append(
                        "Cash sent to "
                        + sender_acc.name
                        + ": ₱"
                        + "{:.2f}".format(amount)
                    )

                    enter_recipient_num_label.config(
                        text="Phone Number Entry Success! ✔️", fg="Green", bg="#19bad3"
                    )

                    enter_amount_label.config(
                        text="Amount transferred successfully 💸",
                        fg="Green",
                        bg="#19bad3",
                    )

                else:
                    enter_amount_label.config(
                        text="Insufficient funds! 😢", fg="Red", bg="#19bad3"
                    )
            except ValueError:
                enter_amount_label.config(
                    text="Please enter a valid amount for transfer 😒",
                    fg="Red",
                    bg="#19bad3",
                )

        window_transfer_money = tk.Toplevel()
        window_transfer_money.title("Transfer Money 💸")
        window_transfer_money.geometry("320x150")
        window_transfer_money.config(bg="#19bad3")

        enter_recipient_num_label = tk.Label(
            window_transfer_money,
            text="Recipient's Phone Number 🖁",
            font=("Roboto", 12),
            bg="#C0f0f6",
        )
        enter_recipient_num_label.pack()

        enter_recipient_num_entry = tk.Entry(window_transfer_money, font=("Roboto", 12))
        enter_recipient_num_entry.insert(3, "+63: ")
        enter_recipient_num_entry.pack()

        enter_amount_label = tk.Label(
            window_transfer_money,
            text="Enter amount 💵",
            font=("Roboto", 12),
            bg="#C0f0f6",
        )
        enter_amount_label.pack()

        enter_amount_entry = tk.Entry(window_transfer_money, font=("Roboto", 12))
        enter_amount_entry.pack()

        transfer_button = tk.Button(
            window_transfer_money,
            text="Transfer Money 🤑💸",
            font=("Roboto", 12),
            bg="#Cfecf0",
            command=transfer_amount,
        )
        transfer_button.pack()

    def clicked_transaction_history(self):
        window_history = tk.Toplevel()
        window_history.title("Transaction History")
        window_history.geometry("300x300")
        window_history.config(bg="#19bad3")

        history_label = tk.Label(
            window_history,
            text="Transaction History",
            font=("Roboto", 12),
            bg="#19bad3",
        )
        history_label.pack()

        scrollbar = tk.Scrollbar(window_history)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        history_text = tk.Text(
            window_history,
            font=("Roboto", 12),
            bg="#C0f0f6",
            yscrollcommand=scrollbar.set
        )
        history_text.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=history_text.yview)

        # Populate transaction history text
        for i, transaction in enumerate(self.transaction_history, start=1):
            history_text.insert(tk.END, f"{i}. {transaction}\n")

        # Disable text editing
        history_text.config(state=tk.DISABLED)

    def clicked_switched_account(self, new_account):
        global current_account
        current_account = new_account
        switch_window.destroy()
        window.destroy()
        option_window(current_account.name, current_account.phone_number)

    def clicked_exit(self):
        print("You have closed the system.")
        sys.exit(0)

account1 = Gcash_System("Adz", "+63: 936402438", "qwerty125")
account2 = Gcash_System("Guest", "+63: 12345", "222")

current_account = None

def log_in():
    global current_account
    phone_number = phone_entry.get()
    password = pin_entry.get()

    if phone_number == account1.phone_number and password == account1.password:
        current_account = account1
        print("Log-in Success! 🤩")
        window.withdraw()  # Hides the login window
        option_window(current_account.name, current_account.phone_number)

    elif phone_number == account2.phone_number and password == account2.password:
        current_account = account2
        print("Log-in Success! 🤩")
        window.withdraw()  # Hides the login window
        option_window(current_account.name, current_account.phone_number)

    else:
        login_failed_label = tk.Label(
            window, text="Log-in Failed! 😤", font=("Roboto", 12), fg="red", bg="#19bad3"
        )
        login_failed_label.pack()


def switch_account_window():
    global switch_window
    switch_window = tk.Toplevel()
    switch_window.title("Switch Account")
    switch_window.config(bg="#19bad3")

    option_label = tk.Label(switch_window, text="Select Account:", bg="#19bad3")
    option_label.pack()

    account1_button = tk.Button(
        switch_window,
        text="Account 1",
        command=lambda: current_account.clicked_switched_account(account1),
        bg="#Cfecf0",
    )
    account1_button.pack()

    account2_button = tk.Button(
        switch_window,
        text="Account 2",
        command=lambda: current_account.clicked_switched_account(account2),
        bg="#Cfecf0",
    )
    account2_button.pack()

def option_window(username, phone_number):
    global window
    window = tk.Tk()
    window.title("GCash Python System")
    window.geometry("390x315")
    window.config(bg="#19bad3")

    welcome_label = tk.Label(
        window,
        text="Welcome to GCash Banking System 😎, " + username,
        bg="#19bad3",
        font=("Roboto", 12),
    )
    welcome_label.pack()

    phone_label = tk.Label(
        window,
        text="Phone Number: " + str(phone_number),
        bg="#19bad3",
        font=("Roboto", 12),
    )
    phone_label.pack()

    welcome_label.config(font=("Roboto", 12))
    welcome_label.pack()

    balance_button = tk.Button(
        window,
        text="Balance 🏦",
        command=current_account.clicked_balance,
        bg="#Cfecf0",
        font=("Roboto", 12),
    )
    balance_button.pack()

    cash_in_button = tk.Button(
        window,
        text="Deposit 💰",
        command=current_account.clicked_cash_in,
        bg="#Cfecf0",
        font=("Roboto", 12),
    )
    cash_in_button.pack()

    cash_out_button = tk.Button(
        window,
        text="Withdraw 🫰",
        command=current_account.clicked_cash_out,
        bg="#Cfecf0",
        font=("Roboto", 12),
    )
    cash_out_button.pack()

    buy_load_button = tk.Button(
        window,
        text="Buy Load 🤑",
        command=current_account.clicked_buy_load,
        bg="#Cfecf0",
        font=("Roboto", 12),
    )
    buy_load_button.pack()

    send_money_button = tk.Button(
        window,
        text="Transfer Cash 💸",
        command=lambda: current_account.clicked_transfer_money(account1, account2),
        bg="#Cfecf0",
        font=("Roboto", 12),
    )
    send_money_button.pack()

    view_transactions_button = tk.Button(
        window,
        text="View Transaction History 📜",
        command=current_account.clicked_transaction_history,
        bg="#Cfecf0",
        font=("Roboto", 12),
    )
    view_transactions_button.pack()

    switch_account_button = tk.Button(
        window,
        text="Switch Account 🔁",
        command=switch_account_window,
        bg="#Cfecf0",
        font=("Roboto", 12),
    )
    switch_account_button.pack()

    exit_button = tk.Button(
        window,
        text="Exit 🚪",
        command=current_account.clicked_exit,
        bg="#Cfecf0",
        font=("Roboto", 12),
    )
    exit_button.pack()

    window.mainloop()


# Main window
window = tk.Tk()
window.title("GCash Banking App")
window.geometry("405x250")
window.config(bg="#19bad3")

balance_label = tk.Label(
    window,
    text="Welcome to the GCash Banking System 💲🏦",
    font=("Roboto", 14),
    bg="#19bad3",
)
balance_label.pack(pady=20)

phone_label = tk.Label(
    window, text="Enter Phone Number:", font=("Roboto", 12), bg="#C0f0f6"
)
phone_label.pack()
phone_entry = tk.Entry(window, font=("Roboto", 12))
phone_entry.insert(1, "+63: ")
phone_entry.pack()

password_label = tk.Label(
    window, text="Enter Password:", font=("Roboto", 12), bg="#C0f0f6"
)
password_label.pack()

pin_entry = tk.Entry(window, show="❌", font=("Roboto", 12), fg="Red")
pin_entry.pack()

login_button = tk.Button(
    window,
    text="Log-In",
    font=("Roboto", 12),
    padx="5",
    pady="5",
    command=log_in,
    bg="#Cfecf0",
)
login_button.pack(pady=(20, 8))

buttons_frame = tk.Frame(window, bg="#19bad3")

window.mainloop()
# Looping