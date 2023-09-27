class Operators:
    """Contains all basic arithmetic operators and helpful lists containing them
    
    Also contains disallowed characters"""
    plus = '+'
    minus = '-'
    multiply = '*'
    divide = '/'
    exponent = '^'
    openParen = '('
    closedParen = ')'
    allOperators = [
        plus, minus, multiply, divide, exponent, openParen, closedParen
    ]
    operatorsWithoutParen = [plus, minus, multiply, divide, exponent]
    plusMinus = [plus, minus]
    multiplyDivide = [multiply, divide]
    paren = [openParen, closedParen]
    operatorsWithoutPlusMinus = [multiply, divide, exponent, openParen, closedParen]
    disallowedCharacters = ["!","@","#","$","%","&","=","_",":",">","<","?","{","}","\\","|",",","\""]

class Arithmetic: 
    """All arithmetic operations"""
    def Add(num1, num2):
        return num1 + num2

    def Subtract(num1, num2):
        return num1 - num2

    def Multiply(num1, num2):
        return num1 * num2

    def Divide(num1, num2):
        return num1 / num2

    def Exponent(num, exponent):
        return num**exponent
    
def helpStr():
    return """This is an arithmetic calculator, it does not currently have the capability 
for algebra, trigenometric functions or logarithms
\nExample: 2 + 2\n\nExample: 2 + (2 * (2 ^ 2))\n\nExample: 2 - -5 * (3 + -3)\n\n"""
