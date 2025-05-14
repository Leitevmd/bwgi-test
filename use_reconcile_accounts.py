from bwgi_test import reconcile_accounts
from pprint import pprint

# Example inputs as if they were read from CSV
transactions1 = [
    ["2020-12-04", "Tecnologia", "16.00", "Bitbucket"],
    ["2020-12-04", "Jurídico", "60.00", "LinkSquares"],
    ["2020-12-05", "Tecnologia", "50.00", "AWS"],
]

transactions2 = [
    ["2020-12-04", "Tecnologia", "16.00", "Bitbucket"],
    ["2020-12-05", "Tecnologia", "49.99", "AWS"],
    ["2020-12-04", "Jurídico", "60.00", "LinkSquares"],
]

# Call reconciliation
out1, out2 = reconcile_accounts(transactions1, transactions2)

# Print results
print("Result for transactions1:")
pprint(out1)
print("\nResult for transactions2:")
pprint(out2)
