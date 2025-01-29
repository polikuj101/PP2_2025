class stroka:
    def getString(self):
        self.string = input("Enter a string: ")
        
    def printString(self):
        print(self.string.upper())

a = stroka()
a.getString()
a.printString()

class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, length):
        self.length = length
        
    def area(self):
        return self.length * self.length

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
        
    def area(self):
        return self.length * self.width

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def show(self):
        print(f"Point coordinates: ({self.x}, {self.y})")
    
    def move(self, x, y):
        self.x = x
        self.y = y
    #pythagoras
    def dist(self, other_point):
        return ((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2) ** 0.5

class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposit of ${amount} accepted. New balance: ${self.balance}")
        else:
            print("Invalid deposit amount")
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawal of ${amount} accepted. New balance: ${self.balance}")
        else:
            print("Insufficient funds!")

def filter_primes(numbers):
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    return list(filter(lambda x: is_prime(x), numbers))
