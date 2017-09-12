import pygame, random, sys, bubbleline
from pygame.locals import *

pygame.init()
pygame.mixer.init()

SCREEN_SIZE = (1280, 720)
height = SCREEN_SIZE[1]
width = SCREEN_SIZE[0]
DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN, 32)
pygame.display.set_caption("Tower Test")
pygame.mouse.set_visible(False)

cannon_image = pygame.image.load("Images/tower_50x80.png")

WHITE = (255, 255, 255)
RED   = (255, 0, 0)

pygame.key.set_repeat(10)

keystates = {'left':False, 'right':False, 'space':False}
opList    = ["mult", "add", "sub", "div"]
opImgs    = ["Images/multiply_sm.png", "Images/plus_sm.png", "Images/minus_sm.png", "Images/divide_sm.png"]
bigopImgs = ["Images/multiply.png", "Images/plus.png", "Images/minus.png", "Images/divide.png"]
operators = []
range1    = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

'''
    ANSWER GENERATOR START
'''
#Based on the operation, this generates an answer as well as all the solutions
#operator is the operation sign, range1 is the range of numbers chosen

def genAnswer(operator, range1):
    num1=range1[random.randrange(len(range1))]
    num2=range1[random.randrange(len(range1))]
    answer = 0
    if operator=="add": 
        answer=num1+num2

    elif operator=="sub":  
        answer=num1-num2

    elif operator=="mult": 
        answer=num1*num2

    elif operator=="div": 
        answer=num1

    return answer

def generateright(operator, range1, answer):
    num1=range1[random.randrange(len(range1))]
    num2=range1[random.randrange(len(range1))]
    solutions=[]
    if operator=="add": #addition 
        for i in range(len(range1)): 
            for j in range(len(range1)):
                if range1[i]+range1[j]==answer:
                    solutions.append([range1[i],range1[j]])
    elif operator=="sub": #subtraction, add abs() to make it work backwards
        for i in range(len(range1)):
            for j in range(len(range1)):
                if range1[i]-range1[j]==answer:
                    solutions.append([range1[i],range1[j]])
    elif operator=="mult": #multiplication
        for i in range(len(range1)):
            for j in range(len(range1)):
                if range1[i]*range1[j]==answer:
                    solutions.append([range1[i],range1[j]])
    elif operator=="div": #division
        num1=num2*answer
        high=max(range1)*max(range1)
        for i in range(high):
            for j in range(len(range1)):
                if float(i)/float(range1[j])==float(answer):
                    solutions.append([i,range1[j]])

    return solutions
    #answer is the chosen number, solutions are all solutions to the equation


#Generates random wrong numbers
#Range1 is an array of numbers selected
def generatewrong(operator, range1, answer): 
    num1=range1[random.randrange(len(range1))]
    num2=range1[random.randrange(len(range1))] 
    if operator=="add":
        #While loops just make sure numbers dont generate right asnwer
        while (num1+num2)==answer: 
            num1=range1[random.randrange(len(range1))]
    elif operator=="sub":
        while abs(num1-num2)==answer:
            num1=range1[random.randrange(len(range1))]
    elif operator=="mult":
        while (num1*num2)==answer:
            num1=range1[random.randrange(len(range1))]
    elif operator=="div":
        num1=num1*num2
        while (num1/num2)==answer:
            num2=range1[random.randrange(len(range1))]
    return [num1,num2]



def pick(operator, range1, answer): #Picks either the right answer, or a wrong generated number
    x=random.randrange(6) #Chance for right is 1/x
    solutions = generateright(operator, range1, answer)
    if x == 1:
        return solutions[random.randrange(len(solutions))] #Right
    else:
        return generatewrong(operator,range1,answer) #Wrong

'''
    ANSWER GENERATOR END
'''

'''
    TOWER MOVE START
'''
class Operator(pygame.sprite.Sprite):
    color = (random.randrange(255), random.randrange(255), random.randrange(255))
    def __init__(self, xCoord, yCoord, imageIndex, operator, answer):
        self.xCoord     = xCoord
        self.yCoord     = yCoord
        self.imageIndex = imageIndex
        self.operator   = operator
        self.answer     = answer
        pygame.sprite.Sprite.__init__(self)
        self.image      = pygame.image.load(opImgs[imageIndex]).convert_alpha()
        self.rect       = self.image.get_rect()
        self.rect.topleft = [self.xCoord, self.yCoord]

    def update(self):
        self.yCoord -= 5
        self.rect.topleft = [self.xCoord, self.yCoord]
        DISPLAYSURF.blit(self.image, (self.xCoord + 5, self.yCoord - 20))
        if self.yCoord < 0:
            del self
    
class Cannon(pygame.sprite.Sprite):
    fontObj = pygame.font.Font("freesansbold.ttf", 48)
    def __init__(self, xCoord, yCoord, image, speed):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.speed  = speed
        self.currentIndex = random.choice([0, 1, 2, 3])
        pygame.sprite.Sprite.__init__(self)
        self.image  = image.convert_alpha()
        self.rect   = self.image.get_rect()
        self.rect.topleft = [self.xCoord, self.yCoord]
        self.answer = genAnswer(opList[self.currentIndex], range1)
        self.shootSound = pygame.mixer.Sound("Sound/Bubble.ogg")
        self.numbers=[1]
    def shoot(self):
        self.shootSound.play()
        operators.append(Operator(self.xCoord, self.yCoord, self.currentIndex, opList[self.currentIndex], self.answer))
        #solutions = pick(opList[self.currentIndex], range1, self.answer)
        self.numbers=[1]
        a=pick(opList[self.currentIndex], range1, self.answer)
        for j in range(2):
            self.numbers.append(a[j])
        print self.numbers,self.answer
        ''' PREFORM ACTIONS TO CHECK FOR COLLISION AND CORRECTNESS'''
        self.currentIndex = random.choice([0, 1, 2, 3]) #changes operator to new one
        self.answer = genAnswer(opList[self.currentIndex], range1) #changes answer
        
    def update(self, right, left, space):
        if right and self.xCoord <= width - 50:
            self.xCoord += self.speed
        if left and self.xCoord > 0:
            self.xCoord -= self.speed
        if space:
            self.shoot()
        a=pick(opList[self.currentIndex], range1, self.answer)
        for j in range(2):
            self.numbers.append(a[j])
        answerText = self.fontObj.render(str(self.answer), True, RED)
        pygame.draw.line(DISPLAYSURF, RED, (self.xCoord + 24, height - 100), (self.xCoord + 24, 0), 1)
        DISPLAYSURF.blit(self.image, (self.xCoord, self.yCoord))
        DISPLAYSURF.blit(pygame.image.load(bigopImgs[self.currentIndex]).convert_alpha(), (0, 0))
        DISPLAYSURF.blit(answerText, (1190, 0))

def play():
    cannon = Cannon((width / 2) - 25, height - 100, cannon_image, 2)
    bubbleLine = bubbleline.BubbleLine(DISPLAYSURF,cannon.numbers)
    counter = 0
    score=0
    scoreFont = pygame.font.Font("freesansbold.ttf", 48)
    while True:
        DISPLAYSURF.fill(WHITE)
    
        if counter % 8 == 0:
            bubbleLine.step(0,cannon.numbers)
        bubbleLine.draw()
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == KEYDOWN:  
                if event.key == K_RIGHT:
                    keystates['right'] = True
                if event.key == K_LEFT:
                    keystates['left'] = True
                if event.key == K_SPACE:
                    pygame.key.set_repeat(0)
                    cannon.shoot()
                    pygame.key.set_repeat(10)

            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    keystates['right'] = False
                if event.key == K_LEFT:
                    keystates['left'] = False


        if not len(operators) == 0:
            bubbleLine.collide(operators,cannon.numbers,score)

        for op in operators:
            if not op.yCoord < 0:
                op.update()
            else:
                operators.remove(op)
        
        cannon.update(keystates['right'], keystates['left'], keystates['space'])
        scoreText = scoreFont.render("Score:"+str(score), True, RED)
        DISPLAYSURF.blit(scoreText,(0,660))
        pygame.display.update()
        counter += 1
        
'''
    TOWER MOVE END
'''
