import time
import argparse
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bwgi_test import computed_property


class Dummy:
    def __init__(self, value):
        self.value = value

    @computed_property('value')
    def doubled(self):
        return self.value * 2


def run_benchmark(n):
    items = [Dummy(i) for i in range(n)]
    start = time.time()
    total = sum(item.doubled for item in items)
    mid = time.time()
    total += sum(item.doubled for item in items)
    end = time.time()
    print(f"Initial access: {mid - start:.4f}s, Cached access: {end - mid:.4f}s, Total: {total}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=1000000, help="Number of objects")
    args = parser.parse_args()
    run_benchmark(args.n)
