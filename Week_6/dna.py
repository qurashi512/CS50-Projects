import csv
import sys


def main():
    # تأكد من الأرقمنتس الصحيحة
    if len(sys.argv) != 3:
        print("Usage: python dna.py database sequence")
        sys.exit(1)

    # اقرأ قاعدة البيانات
    database = []
    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        for row in reader:
            database.append(row)

    # اقرأ تسلسل الـ DNA
    with open(sys.argv[2]) as f:
        sequence = f.read()

    # احسب تكرار كل STR
    strs = list(database[0].keys())[1:]  # تجاهل عمود الاسم
    counts = {}
    for str in strs:
        counts[str] = longest_match(sequence, str)

    # قارن مع قاعدة البيانات
    for person in database:
        match = True
        for str in strs:
            if int(person[str]) != counts[str]:
                match = False
                break
        if match:
            print(person["name"])
            return

    print("No match")


def longest_match(sequence, subsequence):
    longest = 0
    length = len(subsequence)

    for i in range(len(sequence)):
        count = 0
        while sequence[i + count * length: i + (count + 1) * length] == subsequence:
            count += 1
        longest = max(longest, count)

    return longest


main()
