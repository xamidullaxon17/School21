def my_csv():
    # Faylni utf-8 kodlashda o'qish
    with open("ds.csv", 'r', encoding='utf-8') as csv_file:
        lines = csv_file.readlines()

    changed_lines = [line.replace(',', '\t') for line in lines]

    with open("ds.tsv", 'w', encoding='utf-8') as tsv_file:
        tsv_file.writelines(changed_lines)

if __name__ == "__main__":
    my_csv()
