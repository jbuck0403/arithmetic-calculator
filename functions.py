from operators_module import Operators, Arithmetic, helpStr

#Accept passed string or request input from user if none is passed
#convert string into list split by numbers and operators
def GatherInput(inputStr=""):
    """Returns expression ready for Pemdas()
    
    Accepts an expression string "2+2" or, if none is provided, requests one from the
      user, then converts it to a list for further processing"""

    newList = []
    num = ""

    #if no string is provided, request one via input
    if inputStr == "":
        inputStr = input("Enter expression to calculate: ")

    #convert input string into a list for further processing
    for char in inputStr:
        if char.isdigit():
            num += char
        elif char == " ":
            continue
        else:
            if num.isdigit():
                newList.append(int(num))
                num = ""

            newList.append(char)

    if num.isdigit():
        newList.append(int(num))

    parsedNegativeNumbers = ParseNegativeNumbers(newList)
    parsedDecimalNumbers = ParseDecimals(parsedNegativeNumbers)

    #pass the new list into the negative number parser to fully ready the list for processing
    return ParseNegativeNumbers(parsedDecimalNumbers)


def ParseDecimals(expression):
    """Returns converted expression as a list ready for Pemdas()
    
    Takes a list that has already passed through ParseNegativeNumbers
    and converts any intended decimal numbers"""
    parsedExpression = []
    decimalNumber = ""
    
    for index in range(0, len(expression)):
        element = expression[index]
            
        if isinstance(element, int) or element == ".":
            decimalNumber += str(element)
        elif isinstance(element, str):
            if not decimalNumber == "":
                parsedExpression.append(float(decimalNumber))
                decimalNumber = ""
            parsedExpression.append(element)
              
    return parsedExpression

def ParseNegativeNumbers(expression):
    """Returns expression ready for ParseDecimals()
    
    Take an expression in list form [2, '+', 2] and convert any intended negative numbers 
    into an actual negative number in the list e.g. [2, '+', '-', 2] -> [2, '+', -2]"""
    parsedExpression = []
    nextIsNegative = False

    for index in range(0, len(expression)):
        if nextIsNegative:
            parsedExpression.append(expression[index] * (-1))
            nextIsNegative = False
        elif expression[index] is Operators.minus and not expression[index - 1] == None and expression[index - 1] in Operators.allOperators:
            nextIsNegative = True
            continue
        else:
            parsedExpression.append(expression[index])
                                
    return parsedExpression

def PopFromExpression(expression, index):
    """Returns modified expression, 2 numbers and their associated arithmetic operator
    
    Removes elements from expression, returns them separately"""
    num1 = expression.pop(index)
    operator = expression.pop(index)
    num2 = expression.pop(index)

    return expression, num1, operator, num2

def ReduceExpression(expression, index = 0):
    """Returns modified expression
    
    Takes 3 elements from the expression list, starting at the passed index, and applies arithmetic based on the operator"""
    
    expression, num1, operator, num2 = PopFromExpression(expression, index)

    if operator == Operators.exponent:
        expression.insert(index, Arithmetic.Exponent(num1, num2))
    elif operator in Operators.multiplyDivide:
        if operator == Operators.multiply:
            expression.insert(index, Arithmetic.Multiply(num1, num2))
        else:
            expression.insert(index, Arithmetic.Divide(num1, num2))
    elif operator in Operators.plusMinus:
        if operator == Operators.plus:
            expression.insert(index, Arithmetic.Add(num1, num2))
        else:
            expression.insert(index, Arithmetic.Subtract(num1, num2))

    return expression

def Pemdas(expression):
    """Returns expression, recursive

    Takes a processed expression list [2, '+', 2] and recursively solves the problem according to PEMDAS"""
    #reduces all parentheses first
    while Operators.openParen in expression:
        expression = ReduceParens(expression)

    if Operators.exponent in expression:
        expression = FindExpressionSegment(expression)

    elif Operators.multiply in expression or Operators.divide in expression:
        expression = FindExpressionSegment(expression, [Operators.multiply, Operators.divide])

    elif Operators.plus in expression or Operators.minus in expression:
        expression = FindExpressionSegment(expression, [Operators.plus, Operators.minus])

    if len(expression) > 1:
        Pemdas(expression)
    elif len(expression) == 1:
        return expression
    
    return expression

#if no input, expect exponent, otherwise input correct input ( * / + -)
def FindExpressionSegment(expression, operators = [Operators.exponent]):
    """Returns expression, accepts expression and operator argument

    Decides which arithmetic to apply based on the passed operator"""

    if len(operators) == 1:
        for index in range(0, len(expression)):
            if expression[index + 1] == operators[0]:
                expression = ReduceExpression(expression, index)
                break
            index += 1
    else:
        for index in range(0, len(expression)):
                if expression[index + 1] == operators[0]:
                    expression = ReduceExpression(expression, index)
                    break
                elif expression[index + 1] == operators[1]:
                    expression = ReduceExpression(expression, index)
                    break
                index += 1

    return expression

def ReduceParens(expression, index = 0):
    """Returns expression list
    
    Isolates and subsequently reduces all parentheses sub-expressions; if multiple parentheses exist
    in the expression it recursively solves them as they show up, returning the reduced sub-expression"""

    #if there are no parens in expression return the unchanged expression
    if not Operators.openParen in expression:
        return expression

    parenExpression = []
    parenIndex = 0

    #checks the last known index of a parenthesis (important for recursion)
    for index in range(index, len(expression)):
        if expression[index] == Operators.openParen:
            parenIndex = index
            #as long as it hasn't come across the closing parenthesis
            while not expression[index] == Operators.closedParen:
                #append the sub-expression to the temp list
                parenExpression.append(expression.pop(index))
                #if another starting parenthesis appears
                if expression[index] == Operators.openParen:
                    #start recursion to reduce the nested parentheses
                    expression = ReduceParens(expression)
            #add the completed sub-expression to the temp list
            parenExpression.append(expression.pop(index))
            #
            parenExpression = TrimParens(parenExpression)
            expression.insert(parenIndex, Pemdas(parenExpression)[0])
            break
    return expression

def TrimParens(expression):
    """Accepts expression with parens, returns same expression without parens
    
    Takes in the parentheses sub-expression and trims the parentheses so the
    expression can be reduced returns the trimmed expression"""
    trimmedExpression = []
    for element in expression:
        if element in Operators.paren:
            continue
        trimmedExpression.append(element)
    
    return trimmedExpression

def VerifyInput(expression):
    """Returns False if input is bad, True if acceptable
    
    Blocks most bad inputs; not 100% foolproof, but close"""

    if expression[0] == "h":
        return False, helpStr()

    tempList = []
    expressionStr = "".join(str(element) for element in expression)

    if expression == [Operators.openParen, Operators.closedParen]:
        return False, "Must contain numbers..."
    elif expressionStr.find("()") == 2:
        return False, "No empty Parentheses..."

    #blocks any disallowed characters (e.g. $#% etc...)
    for element in expression:
        if element in Operators.disallowedCharacters or str(element).isalpha():
            return False, "Numbers and operators only..."

    #blocks single parenthesis
    if Operators.openParen in expression and not Operators.closedParen in expression:
        return False, "NO CLOSED PAREN"
    elif Operators.closedParen in expression and not Operators.openParen in expression:
        return False, "NO OPEN PAREN"

    #blocks incorrect parentheses placement
    for element in expression:
        if element == Operators.openParen or element == Operators.closedParen:
            tempList.append(element)
            if len(tempList) == 2:
                if tempList[0] == Operators.closedParen:
                    return False, "CLOSED PAREN AT 0"
    #blocks uneven parentheses ( e.g. ((2+2) )
    openParenCount = 0
    closedParenCount = 0
    for element in tempList:
        if element == Operators.openParen:
            openParenCount += 1
        elif element == Operators.closedParen:
            closedParenCount += 1
    if not openParenCount == closedParenCount:
        return False, "DIFFERENT NUMBER OF PARENS"
    tempList = []

    #blocks multiple operators (e.g. 2 + + 2)
    for index in range(0, len(expression)):
        if len(tempList) > 2 and not Operators.openParen in expression:
            return False, "MORE THAN 2 NON NUMBERS AND NOT PARENS"
        if expression[index] in Operators.operatorsWithoutParen:
            tempList.append(expression[index])
        elif str(expression[index]).isdigit():
            tempList = []
    if len(tempList) == 2 and not "." in tempList:
            if not tempList[1] == Operators.minus and not tempList[1] == Operators.openParen:
                return False, "not sure"

    #returns true if no spotted errors (NOT 100% FOOLPROOF)
    return True, ""