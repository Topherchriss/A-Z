class Calculator:
    def addition(self, number1, number2):
        return number1 + number2

    def subraction(self, number1, number2):
        return number1 - number2

    def multiplication(self, number1, number2):
        return number1 * number2

    def division(self, number1, number2):
        if number2 != 0:
            return number1 / number2
        else:
            raise ValueError("Cannot divide by zero!")