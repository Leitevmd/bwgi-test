import random
import time
from datetime import datetime, timedelta
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bwgi_test import reconcile_accounts

def generate_transaction(date, departments, payees):
    dept = random.choice(departments)
    payee = random.choice(payees)
    amount = f"{random.uniform(10.0, 1000.0):.2f}"
    return [date.strftime("%Y-%m-%d"), dept, amount, payee]

def generate_large_datasets(n):
    base_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
    departments = ["Finance", "IT", "Legal", "HR", "Marketing"]
    payees = [f"Vendor{i}" for i in range(50)]

    transactions1 = []
    transactions2 = []

    for _ in range(n):
        date = base_date + timedelta(days=random.randint(0, 30))
        tx = generate_transaction(date, departments, payees)
        transactions1.append(tx)

        date2 = date + timedelta(days=random.choice([-1, 0, 1]))
        tx2 = tx[:]
        tx2[0] = date2.strftime("%Y-%m-%d")

        if random.random() < 0.1:
            tx2[2] = f"{float(tx2[2]) + random.uniform(0.01, 1.00):.2f}"

        transactions2.append(tx2)

    return transactions1, transactions2

def benchmark_reconcile(n):
    print(f"Generating {n} transactions...")
    tx1, tx2 = generate_large_datasets(n)
    print("Running reconciliation...")
    start_time = time.time()
    out1, out2 = reconcile_accounts(tx1, tx2)
    duration = time.time() - start_time
    print(f"Reconciled {len(out1)} x {len(out2)} transactions in {duration:.2f} seconds.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print("Usage: python benchmark_reconcile.py [number_of_transactions]")
            sys.exit(1)
    else:
        n = 100_000
    benchmark_reconcile(n)