import pygame, sys, cPickle, shelve, towerMove
from pygame.locals import *
 
pygame.init()
pygame.key.set_repeat(0)
 
class GameMenu():
    def __init__(self, screen, items, bg_color=(255,255,255), font=None, font_size=30,font_color=(0, 0, 0)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
 
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
 
        self.items = items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.title=pygame.image.load("Images/title.png")
        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)
            width = label.get_rect().width
            height = label.get_rect().height
            posx = (self.scr_width / 2) - (width / 2)
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)+150
            x=[item, label, (width, height), (posx, posy)]
            self.items.append(x)

    def update(self,cur,choice,ent,operations,optcur,leader):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.title,(322,50))
        if ent==True and choice[cur]=="leader":
            i=0
            for lines in leader:
                label = self.font.render(lines, 1, (0,0,0))
                width = label.get_rect().width
                height = label.get_rect().height
                posx = 600
                t_h = len(leader) * height
                posy = (self.scr_height / 2) - (t_h / 2) + (i* height)+150
                self.screen.blit(self.font.render(lines,1,(0,0,0)),(posx,posy))
                i+=1
        elif ent==True and choice[cur]=="options":
            oper=["Addition","Subtraction","Multiplication","Division"]
            x=450
            for i in range(4):
                if i==optcur:
                    self.screen.blit(self.font.render(oper[i],1,(124,55,201)),(575,x+i*25))     
                else:
                    self.screen.blit(self.font.render(oper[i],1,(0,0,0)),(575,x+i*25))     
                if operations[i]==0:
                    image=pygame.image.load("Images/box.png").convert_alpha()
                    self.screen.blit(image,(715,x+i*25+5))
                else:
                    image=pygame.image.load("Images/cross.png").convert_alpha()
                    self.screen.blit(image,(715,x+i*25+5))
        elif 1==1:    
            y=0
            for x in self.items:
                if y==cur:
                    x[1] = self.font.render(x[0], 1,(124,55,201))
                    self.screen.blit(x[1],x[3])
                else:
                    x[1] = self.font.render(x[0], 1,(0,0,0))
                    self.screen.blit(x[1],x[3])
                y+=1
        pygame.display.flip()

        
    def run(self):
        mainloop = True
        music = pygame.mixer.Sound("Sound/loop1.ogg")
        music.set_volume(.5)
        music.play(-1)
        choice=["play","leader","options","quit"]
        operations=[1,1,1,1]
        cur=0
        optcur=0
        ent=False
        leader=[]
        f = open("Data/highscore2.dat", "r")
        for i in range(10):
            try:
                leader.append(str(cPickle.load(f)))
            except:
                a=1
        leader=leader[::-1]
        for i in range(len(leader)):
            leader[i]=str(i+1)+"."+leader[i]
        while mainloop:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT or event.type==KEYDOWN and event.key == K_ESCAPE:
                    if ent==True:
                        ent=False
                    else:
                        mainloop = False
                        pygame.quit()
                        sys.exit()
                if event.type==KEYDOWN and event.key==K_DOWN:
                    if ent==False:
                        if cur+1==len(choice):
                            cur=0
                        else:
                            cur+=1
                    if ent==True:
                        if optcur+1==len(operations):
                            optcur=0
                        else:
                            optcur+=1
                if event.type==KEYDOWN and event.key==K_UP:
                    if ent==False:
                        if cur-1==-1:
                            cur=len(choice)-1
                        else:
                            cur-=1
                    if ent==True:
                        if optcur-1==-1:
                            optcur=len(operations)-1
                        else:
                            optcur-=1
                if event.type==KEYDOWN and event.key==K_RETURN:
                    
                    if choice[cur]=="play":
                        towerMove.play()
                        a=1
                    
                    elif choice[cur]=="quit":
                        mainloop = False
                        pygame.quit()
                        sys.exit()
                    elif choice[cur]=="options" and ent==True:
                        if operations[optcur]==0:
                            operations[optcur]=1
                        else:
                            operations[optcur]=0
                        
                        
                    ent=True
            self.update(cur,choice,ent,operations,optcur,leader)            
 
 
if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((1280,720), FULLSCREEN, 32)
    menu_items = ('Start','Leaderboards', 'Options','Quit')
 
    pygame.display.set_caption('Marble Math')
    gm = GameMenu(screen, menu_items)
    gm.run()
