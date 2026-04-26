def main():
    height = get_height()
    for i in range(height):
        print(" " * (height - i - 1) + "#" * (i + 1) + "  " + "#" * (i + 1))


def get_height():
    while True:
        try:
            n = int(input("Height: "))
            if 1 <= n <= 8:
                return n
        except ValueError:
            pass


main()
