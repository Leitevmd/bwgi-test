import time
import tempfile
import argparse
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bwgi_test import last_lines

def generate_file(path, line_count):
    with open(path, 'w', encoding='utf-8') as f:
        for i in range(line_count):
            f.write(f"This is line {i}\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lines', type=int, default=1000000, help="Number of lines to generate")
    parser.add_argument('--buffer', type=int, default=8192, help="Buffer size in bytes")
    args = parser.parse_args()

    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
        generate_file(temp_file.name, args.lines)
        temp_path = temp_file.name

    print(f"File with {args.lines} lines created at {temp_path}")
    start = time.time()
    count = sum(1 for _ in last_lines(temp_path, buffer_size=args.buffer))
    duration = time.time() - start

    print(f"Read {count} lines in reverse in {duration:.2f} seconds")
    os.remove(temp_path)

if __name__ == '__main__':
    main()
