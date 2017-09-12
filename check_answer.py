import math,sys

def operate(operator,value2,value1,solution): #checks if equation is correct
    if (operator=="add"):
        if value1+value2==solution:
            return True
        else:
            return False
    elif (operator=="mult"):
        if value1*value2==solution:
            return True
        else:
            return False
    elif (operator=="div"):
        if value1/value2==solution:
            return True
        else:
            return False
    elif (operator=="sub"):
        if value1-value2==solution:
            return True
        else:
            return False
                
        
