from bwgi_test import last_lines

def create_sample_file(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write("Línea uno\n")
        f.write("Línea dos\n")
        f.write("Linha três\n")
        f.write("四行目\n")  # Japanese
        f.write("पांचवी पंक्ति\n")  # Hindi
        f.write("六行目\n")  # Chinese

def main():
    test_file = 'example_utf8.txt'
    create_sample_file(test_file)

    print("Reading last lines in reverse order:")
    for line in last_lines(test_file):
        print(repr(line))

if __name__ == "__main__":
    main()
