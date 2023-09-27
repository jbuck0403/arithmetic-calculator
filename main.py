from operators_module import Operators
from functions import *
from art import logo
from ui import clearTerminal

calculating = True
errorMessage = ""


while calculating:
    clearTerminal()
    print(logo)

    print(errorMessage)

    inputStr = GatherInput()
    errorCheck, errorMessage = VerifyInput(inputStr)

    if errorCheck:
        answer = Pemdas(inputStr)[0]
    else:
        continue

    print(f"The answer is: {answer}")

    if not input("Calculate again? (y/n): ")[0].lower() == "y":
        calculating == False
        break