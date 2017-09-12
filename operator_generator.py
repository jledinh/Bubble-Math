import random

def o_generate(range1,range2):
    operations=["+","-","*","/"]
    choice=operations[range1:range2+1]
    operator=choice[random.randrange(len(choice))]
    return operator,choice
print o_generate(1,3)
