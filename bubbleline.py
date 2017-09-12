import pygame, sys, math, random, distance, Bubble, check_answer, cPickle, shelve
from pygame.locals import *
fpsClock=pygame.time.Clock()
class BubbleLine(object):
    def __init__(self,displaysurf,numbers):
        self.set_path()
        self.bubbles=[]
        self.bubbles.append(Bubble.Bubble(pygame.draw.circle(displaysurf,(255,0,0),(0,self.path[0]),15,0),(255,0,0),numbers))
        self.num_of_circles=len(self.bubbles)
        self.displaysurf=displaysurf

    def step(self,stop,numbers): #this method controls moving the whole bubble line
        
        if stop==0:  #checks whether to move whole line or part of the line based on parameters
            stop=len(self.bubbles)
            
        if (self.bubbles[len(self.bubbles)-1].rect.centerx>=23): #adds new bubble if there is enough space
            self.num_of_circles+=1
            color=(random.randrange(255),random.randrange(255),0)
            self.bubbles.append(Bubble.Bubble(pygame.draw.circle(self.displaysurf,color,(1,int(self.path[0])),15,0),color,numbers))

        start = 0
        for o in range(stop):
            if (distance.distance(self.bubbles[o].rect.center,self.bubbles[o-1].rect.center)>60):
                start = o
        
        for o in range(start, stop):
            if self.bubbles[o].rect.centerx>1280 and o==1: #level over/ game over
                pygame.quit()
                sys.exit()
            if (o==0):   #moves the first bubble
                self.bubbles[o].rect.centery=self.path[self.bubbles[o].rect.centerx+1]
                self.bubbles[o].rect.centerx=self.bubbles[o].rect.centerx+1
            else:
                if (distance.distance(self.bubbles[o].rect.center,self.bubbles[o-1].rect.center)>29):
                    for x in range(2):                                                #only lets it move if there is enough space between
                        self.bubbles[o].rect.centery=self.path[self.bubbles[o].rect.centerx+1]               #it and the bubble in front of it
                        self.bubbles[o].rect.centerx=self.bubbles[o].rect.centerx+1

    def draw(self):
        for o in range(1,len(self.bubbles)):
            self.bubbles[o].draw(self.displaysurf)
    def numdraw(self):
        for o in range(1,len(self.bubbles)):
            self.bubbles[o].numdraw(self.displaysurf)

    def collide(self,projectiles,numbers,score):
        removeList = []
        for o in projectiles:
            for x in range(len(self.bubbles)):
                if (self.bubbles[x].rect.colliderect(o.rect)):
                    if x == len(self.bubbles) - 1:
                        if check_answer.operate(o.operator,self.bubbles[x].value,self.bubbles[x-1].value,o.answer):
                            # removing bubbles and adding to score
                            score+=self.bubbles[x].value
                            score+=self.bubbles[x-1].value
                            print score
                            self.bubbles.remove(self.bubbles[x])
                            self.bubbles.remove(self.bubbles[x-1])
                            removeList.append(o)
                            break
                        else:
                            self.add(o,x,numbers)
                            projectiles.remove(o)
                            break
                    elif distance.distance(o.rect.center,self.bubbles[x-1].rect.center)<distance.distance(o.rect.center,self.bubbles[x+1].rect.center):
                        if check_answer.operate(o.operator,self.bubbles[x].value,self.bubbles[x-1].value,o.answer):
                            # removing bubbles and adding to score
                            score+=self.bubbles[x].value
                            score+=self.bubbles[x-1].value
                            print score
                            self.bubbles.remove(self.bubbles[x])
                            self.bubbles.remove(self.bubbles[x-1])
                            removeList.append(o)
                            break
                        else:
                            self.add(o,x,numbers)
                            projectiles.remove(o)
                            break
                        
                    else:
                        if check_answer.operate(o.operator,self.bubbles[x+1].value,self.bubbles[x].value,o.answer):
                            # removing bubbles and adding to score
                            score+=self.bubbles[x].value
                            score+=self.bubbles[x-1].value
                            print score
                            removeList.append(o)
                            self.bubbles.remove(self.bubbles[x])
                            self.bubbles.remove(self.bubbles[x])
                            break
                        else:
                            self.add(o,x,numbers)
                            projectiles.remove(o)
                            break

        for o in removeList:
            projectiles.remove(o)
                    
                        
    def add(self,projectile,insert_position,numbers): #adds to the bubble line by first finding the other adjacent bubble then inserting in between
        index=0
        if insert_position==0 or (insert_position==1 and distance.distance(projectile.rect.center,self.bubbles[0].rect.center)<distance.distance(projectile.rect.center,self.bubbles[2].rect.center)):
            self.bubbles.insert(1,Bubble.Bubble(projectile.rect,projectile.color,numbers)) #checks if adding bubble to front
            index=1
        else:
            if distance.distance(projectile.rect.center,self.bubbles[insert_position-1].rect.center)<distance.distance(projectile.rect.center,self.bubbles[insert_position+1].rect.center):
                self.bubbles.insert(insert_position,Bubble.Bubble(projectile.rect,projectile.color,numbers))  #if next closest bubble is in front it gets the index
                index=insert_position
            else:
                self.bubbles.insert(insert_position+1,Bubble.Bubble(projectile.rect,projectile.color,numbers)) #if next closest bubble is in back
                index=insert_position+1
                
        move_vector=((self.bubbles[index-1].rect.centerx-self.bubbles[index].rect.centerx),(self.bubbles[index-1].rect.centery-self.bubbles[index].rect.centery))
        target_point=(self.bubbles[index-1].rect.centerx,self.bubbles[index-1].rect.centery) #point that new bubble is joining. move_vector is movement of new bubble to the target_point
        
        while(self.bubbles[index].rect.center!=target_point): #moves the bubbles in front of new bubble while moving new bubble to target_point
            if (distance.distance(target_point,self.bubbles[index-1].rect.center)<29):
                self.step(index,numbers) #moves bubbles in front
                self.step(index,numbers)
            if (math.fabs(target_point[1]-self.bubbles[index].rect.centery)<math.fabs(move_vector[1]/15) or move_vector[1]/15==0):
                self.bubbles[index].rect.centery=target_point[1]
            elif(self.bubbles[index].rect.centery!=target_point[1]):
                if move_vector[1]/15==0:
                    self.bubbles[index].rect.centery+=(move_vector[1])/(math.fabs(move_vector[1]))
                else:
                    self.bubbles[index].rect.centery+=move_vector[1]/15
            if (math.fabs(target_point[0]-self.bubbles[index].rect.centerx)<math.fabs(move_vector[0]/15)):
                self.bubbles[index].rect.centerx=target_point[0]
            elif(self.bubbles[index].rect.centerx!=target_point[0]):
                if move_vector[0]/15==0:
                    self.bubbles[index].rect.centerx+=(move_vector[0])/(math.fabs(move_vector[0]) or move_vector[0]/15==0)
                else:
                    self.bubbles[index].rect.centerx+=move_vector[0]/15
            self.displaysurf.fill((255,255,255))
            self.draw()

            fpsClock.tick(100)
            pygame.display.update()
 
    def set_path(self):
        f=open("Data/level_paths.dat","r")
        self.path=cPickle.load(f)
        f.close()
if __name__ == "__main__":
    print "This module handles all the bubble line movements."
    raw_input("\n\nPress the enter key to exit.")          

