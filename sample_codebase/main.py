from math_ops import add, subtract
from calculator import Calculator

if __name__ == "__main__":
    print("Addition:", add(5, 3))
    print("Subtraction:", subtract(10, 4))

    calc = Calculator()
    print("Multiplication:", calc.multiply(2, 3))
    print("Division:", calc.divide(10, 2))
