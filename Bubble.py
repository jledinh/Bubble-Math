import pygame
from pygame.locals import *

class Bubble(object):
    def __init__(self,rect,color,numbers):  #constructor
        self.rect=rect
        self.color=color
        self.value = numbers[0]
        numbers.pop(0)
        self.font=pygame.font.SysFont("monospace",16)
        self.text=self.font.render(str(self.value),True,(0,0,0))
        self.textRect=self.text.get_rect()
        self.textRect.center=self.rect.center
    def draw(self,displaysurf):  #draws the bubble onto the surface
        pygame.draw.circle(displaysurf,self.color,self.rect.center,15,0)
        self.textRect=self.text.get_rect()
        self.textRect.center=self.rect.center
        self.textRect.centery=self.rect.centery-10
        self.textRect.centerx=self.rect.centerx-6
        displaysurf.blit(self.text,self.textRect.center)
    def __str__(self):    #prints the bubble's rect and color
        return str(self.rect) +" "+str(self.color)
