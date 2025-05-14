import unittest
from bwgi_test import reconcile_accounts

class TestReconcileAccounts(unittest.TestCase):
    def test_all_cases_with_subtests(self):
        test_cases = [
            # --- Basic reconciliation ---
            (
                "basic_reconciliation",
                [["2020-12-04", "Tecnologia", "16.00", "Bitbucket"],
                 ["2020-12-04", "Jurídico", "60.00", "LinkSquares"],
                 ["2020-12-05", "Tecnologia", "50.00", "AWS"]],
                [["2020-12-04", "Tecnologia", "16.00", "Bitbucket"],
                 ["2020-12-05", "Tecnologia", "49.99", "AWS"],
                 ["2020-12-04", "Jurídico", "60.00", "LinkSquares"]],
                [["2020-12-04", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
                 ["2020-12-04", "Jurídico", "60.00", "LinkSquares", "FOUND"],
                 ["2020-12-05", "Tecnologia", "50.00", "AWS", "MISSING"]],
                [["2020-12-04", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
                 ["2020-12-05", "Tecnologia", "49.99", "AWS", "MISSING"],
                 ["2020-12-04", "Jurídico", "60.00", "LinkSquares", "FOUND"]],
            ),

            # --- Prefers earlier match ---
            (
                "prefers_earlier_match",
                [["2023-01-03", "IT", "100.00", "VendorX"],
                 ["2023-01-03", "IT", "100.00", "VendorY"]],
                [["2023-01-03", "IT", "100.00", "VendorX"],
                 ["2023-01-02", "IT", "100.00", "VendorX"]],
                [["2023-01-03", "IT", "100.00", "VendorX", "FOUND"],
                 ["2023-01-03", "IT", "100.00", "VendorY", "MISSING"]],
                [["2023-01-03", "IT", "100.00", "VendorX", "MISSING"],
                 ["2023-01-02", "IT", "100.00", "VendorX", "FOUND"]],
            ),

            # --- Strict field matching ---
            ("mismatch_department",
             [["2023-01-03", "Finance", "500.00", "VendorX"]],
             [["2023-01-02", "Legal", "500.00", "VendorX"]],
             [["2023-01-03", "Finance", "500.00", "VendorX", "MISSING"]],
             [["2023-01-02", "Legal", "500.00", "VendorX", "MISSING"]],
            ),
            ("mismatch_amount",
             [["2023-01-03", "Finance", "500.00", "VendorX"]],
             [["2023-01-02", "Finance", "500.01", "VendorX"]],
             [["2023-01-03", "Finance", "500.00", "VendorX", "MISSING"]],
             [["2023-01-02", "Finance", "500.01", "VendorX", "MISSING"]],
            ),
            ("mismatch_payee",
             [["2023-01-03", "Finance", "500.00", "VendorX"]],
             [["2023-01-02", "Finance", "500.00", "Vendor Y"]],
             [["2023-01-03", "Finance", "500.00", "VendorX", "MISSING"]],
             [["2023-01-02", "Finance", "500.00", "Vendor Y", "MISSING"]],
            ),

            # --- Multiple ±1 day matches, must pick earliest ---
            ("multiple_candidates_earliest_selected",
             [["2023-01-03", "IT", "100.00", "VendorZ"]],
             [["2023-01-02", "IT", "100.00", "VendorZ"],
              ["2023-01-04", "IT", "100.00", "VendorZ"]],
             [["2023-01-03", "IT", "100.00", "VendorZ", "FOUND"]],
             [["2023-01-02", "IT", "100.00", "VendorZ", "FOUND"],
              ["2023-01-04", "IT", "100.00", "VendorZ", "MISSING"]],
            ),

            # --- Matching order matters ---
            ("order_of_matches_matters",
             [["2023-01-02", "IT", "100.00", "VendorB"],
              ["2023-01-02", "IT", "100.00", "VendorB"]],
             [["2023-01-01", "IT", "100.00", "VendorB"],
              ["2023-01-01", "IT", "100.00", "VendorB"]],
             [["2023-01-02", "IT", "100.00", "VendorB", "FOUND"],
              ["2023-01-02", "IT", "100.00", "VendorB", "FOUND"]],
             [["2023-01-01", "IT", "100.00", "VendorB", "FOUND"],
              ["2023-01-01", "IT", "100.00", "VendorB", "FOUND"]],
            ),
        ]

        for name, tx1, tx2, expected1, expected2 in test_cases:
            with self.subTest(name=name):
                out1, out2 = reconcile_accounts(tx1, tx2)
                self.assertEqual(out1, expected1)
                self.assertEqual(out2, expected2)
