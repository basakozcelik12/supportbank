from collections import defaultdict
import csv

class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.transactions = [] 

    def payDebt(self, payment_to, date, amount, narrative):
        self.balance -= amount
        self.transactions.append(f"{self.name} paid to {payment_to} amount {amount} for {narrative} at {date}")

    def getDebt(self, payment_from, date, amount, narrative):
        self.balance += amount
        self.transactions.append(f"{payment_from} paid to {self.name} amount {amount} for {narrative} at {date}")
        
accounts = {}
file_path = "src/supportbank/Transactions2014.csv"

with open(file_path, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        payer = row['From']
        receiver = row['To']
        amount = float(row['Amount'])
        date = row['Date']
        narrative = row['Narrative']

        if payer not in accounts:
            accounts[payer] = Account(payer)
        if receiver not in accounts:
            accounts[receiver] = Account(receiver)

        accounts[payer].payDebt(receiver, date, amount, narrative)
        accounts[receiver].getDebt(payer, date, amount, narrative)

while True:
    command = input("Enter command (List All / List [Name]): ").strip()
    
    if command.lower() == "list all":
        for account in accounts.values():
            status = "owes" if account.balance < 0 else "is owed"
            print(f"{account.name} {status} {abs(account.balance)}")
    elif command.lower().startswith("list "):
        name = command[5:].strip()
        if name in accounts:
            account = accounts[name]
            print(f"\nTransactions for {name} (Balance: {account.balance}):")
            for t in account.transactions:
                print(t)
        else:
            print(f"No account found for '{name}'.")
    else:
        break



