def main():
    number = get_number()
    if is_valid(number):
        print(get_type(number))
    else:
        print("INVALID")


def get_number():
    while True:
        try:
            n = int(input("Number: "))
            if n > 0:
                return n
        except ValueError:
            pass


def is_valid(number):
    digits = str(number)
    total = 0

    # الأرقام اللي تتضاعف (كل ثاني رقم من اليمين)
    for i in range(len(digits) - 2, -1, -2):
        d = int(digits[i]) * 2
        if d > 9:
            total += d // 10 + d % 10  # اجمع أرقام الناتج
        else:
            total += d

    # الأرقام اللي ما تتضاعف
    for i in range(len(digits) - 1, -1, -2):
        total += int(digits[i])

    return total % 10 == 0


def get_type(number):
    digits = str(number)
    length = len(digits)
    first_two = int(digits[:2])
    first_one = int(digits[0])

    if length == 15 and first_two in [34, 37]:
        return "AMEX"
    elif length == 16 and 51 <= first_two <= 55:
        return "MASTERCARD"
    elif length in [13, 16] and first_one == 4:
        return "VISA"
    else:
        return "INVALID"


main()
