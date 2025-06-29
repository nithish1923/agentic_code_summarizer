class Calculator:
    def multiply(self, x, y):
        """Multiply two numbers."""
        return x * y

    def divide(self, x, y):
        """Divide x by y. Raises ZeroDivisionError if y is zero."""
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return x / y
