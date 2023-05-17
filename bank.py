import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from PIL import ImageTk, Image

class BankingGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Banking Application')
        self.geometry('300x200')
        self.configure(bg='#588A8A')

        # Set custom background image
        background_image = ImageTk.PhotoImage(Image.open('l.jpg'))
        background_label = tk.Label(self, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.account_number = simpledialog.askstring("Account Number", "Enter your account number:")
        self.pin = simpledialog.askstring("PIN", "Enter your PIN:")

        self.account = BankAccount(self.account_number, self.pin)

        # Create a frame for buttons
        button_frame = tk.Frame(self, bg='#588A8A')
        button_frame.pack(pady=10)

        # Define button styles
        style = ttk.Style()
        style.configure('TButton',
                        background='red',  
                        foreground='red')  # White text color

        # Create deposit button
        deposit_button = ttk.Button(button_frame, text="Deposit", command=self.deposit)
        deposit_button.pack(side='left', padx=5)

        # Create withdraw button
        withdraw_button = ttk.Button(button_frame, text="Withdraw", command=self.withdraw)
        withdraw_button.pack(side='left', padx=5)

        # Create statement button
        statement_button = ttk.Button(button_frame, text="Get Statement", command=self.get_statement)
        statement_button.pack(side='left', padx=5)

    def deposit(self):
        if self.authenticate():
            amount = simpledialog.askfloat("Deposit", "Enter the amount to deposit:")
            if amount is not None:
                try:
                    self.account.deposit(amount)
                    messagebox.showinfo("Deposit", "Deposit successful.")
                except ValueError as e:
                    messagebox.showerror("Invalid Amount", str(e))

    def withdraw(self):
        if self.authenticate():
            amount = simpledialog.askfloat("Withdraw", "Enter the amount to withdraw:")
            if amount is not None:
                try:
                    self.account.withdraw(amount)
                    messagebox.showinfo("Withdrawal", "Withdrawal successful.")
                except ValueError as e:
                    messagebox.showerror("Invalid Amount", str(e))

    def get_statement(self):
        if self.authenticate():
            statement = self.account.get_statement()
            messagebox.showinfo("Bank Statement", statement)

    def authenticate(self):
        pin = simpledialog.askstring("Authentication", "Enter your PIN:")
        if pin == self.pin:
            return True
        else:
            messagebox.showerror("Authentication Failed", "Invalid PIN.")
            return False

# Define the bank account class
class BankAccount:
    def __init__(self, account_number, pin):
        self.account_number = account_number
        self.pin = pin
        self.balance = 0
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposit: +{amount}")

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.transactions.append(f"Withdrawal: -{amount}")

    def get_statement(self):
        statement = f"Bank Statement for Account Number: {self.account_number}\n"
        statement += f"Current Balance: {self.balance}\n"
        statement += "Transactions:\n"
        for transaction in self.transactions:
            statement += f"- {transaction}\n"
        return statement

if __name__ == '__main__':
    app = BankingGUI()
    app.mainloop()
