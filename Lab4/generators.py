def square_generator(N):
    """Generator that yields squares of numbers up to N."""
    for i in range(N + 1):
        yield i ** 2


def even_numbers(N):
    """Generator that yields even numbers up to N."""
    for i in range(0, N + 1, 2):
        yield i


def divisible_by_3_and_4(N):
    """Generator that yields numbers divisible by 3 and 4 up to N."""
    for i in range(N + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


def squares(a, b):
    """Generator that yields squares of numbers from a to b."""
    for i in range(a, b + 1):
        yield i ** 2


def countdown(n):
    """Generator that counts down from n to 0."""
    while n >= 0:
        yield n
        n -= 1


# Testing all generators

# 1. Squares up to N
N = 10
print("Squares up to N:", list(square_generator(N)))

# 2. Even numbers up to N
N = int(input("Enter a number for even numbers: "))
print("Even numbers:", ",".join(str(num) for num in even_numbers(N)))

# 3. Numbers divisible by 3 and 4 up to N
N = int(input("Enter a number for divisible by 3 and 4: "))
print("Numbers divisible by 3 and 4:", list(divisible_by_3_and_4(N)))

# 4. Squares between (a) and (b)
a, b = 3, 8
print(f"Squares from {a} to {b}:", list(squares(a, b)))

# 5. Countdown from N to 0
N = int(input("Enter a number for countdown: "))
print("Countdown:", list(countdown(N)))
