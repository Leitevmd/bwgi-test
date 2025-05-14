from copy import deepcopy
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Tuple

def reconcile_accounts(transactions1: List[List[str]], transactions2: List[List[str]]) -> Tuple[List[List[str]], List[List[str]]]:
    t1 = deepcopy(transactions1)
    t2 = deepcopy(transactions2)

    def normalize(row):
        return (row[1], row[2], row[3])

    def parse_date(s):
        return datetime.strptime(s, "%Y-%m-%d").date()

    index2 = defaultdict(list)
    for idx, row in enumerate(t2):
        key = normalize(row)
        date = parse_date(row[0])
        index2[key].append([idx, date, False])

    for row in t1:
        key = normalize(row)
        date1 = parse_date(row[0])
        candidates = index2.get(key, [])
        # Filter to only candidates within ±1 day and not used
        valid_candidates = [c for c in candidates if not c[2] and -1 <= (c[1] - date1).days <= 1]
        # Sort by candidate date to ensure earliest match is selected
        valid_candidates.sort(key=lambda c: c[1])

        if valid_candidates:
            best_match = valid_candidates[0]
            best_match[2] = True
            row.append("FOUND")
        else:
            row.append("MISSING")

    for row in t2:
        key = normalize(row)
        date2 = parse_date(row[0])
        matched = False
        for candidate in index2[key]:
            if candidate[1] == date2 and candidate[2] is True:
                matched = True
                candidate[2] = "MARKED"
                break
        row.append("FOUND" if matched else "MISSING")

    return t1, t2
