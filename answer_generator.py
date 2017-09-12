#Based on the operation, this generates an answer as well as all the solutions
#operator is the operation sign, range1 is the range of numbers chosen
def generateright(operator,range1):
    num1=range1[random.randrange(len(range1))]
    num2=range1[random.randrange(len(range1))]
    solutions=[]
    if operator=="+": #addition 
        answer=num1+num2
        for i in range(len(range1)): 
            for j in range(len(range1)):
                if range1[i]+range1[j]==answer:
                    solutions.append([range1[i],range1[j]])
    elif operator=="-": #subtraction, add abs() to make it work backwards
        answer=num1-num2
        for i in range(len(range1)):
            for j in range(len(range1)):
                if range1[i]-range1[j]==answer:
                    solutions.append([range1[i],range1[j]])
    elif operator=="*": #multiplication
        answer=num1*num2
        for i in range(len(range1)):
            for j in range(len(range1)):
                if range1[i]*range1[j]==answer:
                    solutions.append([range1[i],range1[j]])
    elif operator=="/": #division
        answer=num1
        num1=num2*answer
        high=max(range1)*max(range1)
        for i in range(high):
            for j in range(len(range1)):
                if float(i)/float(range1[j])==float(answer):
                    solutions.append([i,range1[j]])
        """
        Used for backwards 
        sollength=len(solutions)
        for i in range(sollength):
            solutions.append([solutions[i][1],solutions[i][0]])
        """
    return answer, solutions
    #answer is the chosen number, solutions are all solutions to the equation


#Generates random wrong numbers
#Range1 is an array of numbers selected
def generatewrong(operator,range1,answer): 
    num1=range1[random.randrange(len(range1))]
    num2=range1[random.randrange(len(range1))] 
    if operator=="+":
        #While loops just make sure numbers dont generate right asnwer
        while (num1+num2)==answer: 
            num1=range1[random.randrange(len(range1))]
    elif operator=="-":
        while abs(num1-num2)==answer:
            num1=range1[random.randrange(len(range1))]
    elif operator=="*":
        while (num1*num2)==answer:
            num1=range1[random.randrange(len(range1))]
    elif operator=="/":
        num1=num1*num2
        while (num1/num2)==answer:
            num2=range1[random.randrange(len(range1))]
    return [num1,num2]



def pick(operator,solutions,range1,answer): #Picks either the right answer, or a wrong generated number
    x=random.randrange(9) #Chance for right is 1/x
    if x==1:
        return solutions[random.randrange(len(solutions))] #Right
    else:
        return generatewrong(operator,range1,answer) #Wrong



