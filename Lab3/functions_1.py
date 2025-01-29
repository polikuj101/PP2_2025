import random
from itertools import permutations

def convert_grams_to_ounces(grams):
    return 28.3495231 * grams

def convert_fahrenheit_to_celsius(fahrenheit):
    return (5 / 9) * (fahrenheit - 32)

def solve(numheads, numlegs):
    for chickens in range(numheads + 1):
        rabbits = numheads - chickens
        if (2 * chickens + 4 * rabbits) == numlegs:
            return chickens, rabbits
    return None

def filter_prime(numbers):
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    return [num for num in numbers if is_prime(num)]

def get_permutations(string):
    perms = [''.join(p) for p in permutations(string)]
    return sorted(list(set(perms)))  

def reverse_words(sentence):
    return ' '.join(sentence.split()[::-1])

def has_33(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 3 and nums[i + 1] == 3:
            return True
    return False

def spy_game(nums):
    code = [0, 0, 7]
    pos = 0
    for num in nums:
        if num == code[pos]:
            pos += 1
            if pos == len(code):
                return True
    return False

def sphere_volume(radius):
    import math
    return (4/3) * math.pi * (radius ** 3)

def get_unique_list(lst):
    unique = []
    for item in lst:
        if item not in unique:
            unique.append(item)
    return unique

def is_palindrome(text):
    text = ''.join(c.lower() for c in text if c.isalnum())
    return text == text[::-1]

def histogram(numbers):
    for num in numbers:
        print('*' * num)

def guess_number_game():
    name = input("Hello! What is your name?\n")
    number = random.randint(1, 20)
    print(f"Well, {name}, I am thinking of a number between 1 and 20.")
    
    guesses = 0
    while True:
        guesses += 1
        guess = int(input("Take a guess.\n"))
        
        if guess < number:
            print("Your guess is too low.")
        elif guess > number:
            print("Your guess is too high.")
        else:
            print(f"Good job, {name}! You guessed my number in {guesses} guesses!")
            break

if __name__ == "__main__":
    grams = int(input())
    print(f"1. Converting {grams} grams to ounces:", convert_grams_to_ounces(grams))
    deg = int(input())
    print(f"2. Converting {deg}°F to Celsius:", convert_fahrenheit_to_celsius(98.6))
    print("3. Solving farm puzzle (35 heads, 94 legs):", solve(35, 94))
    lst = list(map(int,input().split()))
    print("4. Prime numbers in [1,2,3,4,5,6,7,8,9,10]:", filter_prime(lst))
    word = input()
    print(f"5. Permutations of '{word}':", get_permutations(word))
    print(f"6. Reversing '{word}':", reverse_words(word))
    new = list(map(int,input().split()))
    print("7. Checking a list for adjacent 3s:", has_33(new))
    new = list(map(int,input().split()))
    print("8. Checking list for 007:", spy_game(new))
    r = int(input())
    print(f"9. Volume of sphere with radius {r}:", sphere_volume(r))
    new = list(map(int,input().split()))
    print("10. Unique elements in list:", get_unique_list())
    word = input()
    print(f"11. Is '{word}' a palindrome?:", is_palindrome(word))
    new = list(map(int,input().split()))
    print("\n12. Histogram of list:")
    histogram(new)
    
    print("\n13. Let's play guess the number!")
    guess_number_game()
