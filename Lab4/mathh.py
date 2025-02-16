import math

# 1. Convert degree to radian
def degree_to_radian(degree):
    return degree * (math.pi / 180)

degree = float(input("Enter degree: "))
print(f"Radian: {degree_to_radian(degree):.6f}")


# 2. Calculate the area of a trapezoid
def trapezoid_area(height, base1, base2):
    return (1/2) * (base1 + base2) * height

height = float(input("Enter height of trapezoid: "))
base1 = float(input("Enter first base: "))
base2 = float(input("Enter second base: "))
print(f"Trapezoid Area: {trapezoid_area(height, base1, base2):.1f}")


# 3. Calculate the area of a regular polygon
def regular_polygon_area(n_sides, side_length):
    return (n_sides * (side_length ** 2)) / (4 * math.tan(math.pi / n_sides))

n_sides = int(input("Enter number of sides: "))
side_length = float(input("Enter length of a side: "))
print(f"Polygon Area: {regular_polygon_area(n_sides, side_length):.1f}")


# 4. Calculate the area of a parallelogram
def parallelogram_area(base, height):
    return base * height

base = float(input("Enter base of parallelogram: "))
height = float(input("Enter height of parallelogram: "))
print(f"Parallelogram Area: {parallelogram_area(base, height):.1f}")
