# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 16:15:35 2020

@author: Read
"""

#math.tan(math.radians(-30))
#math.atan2(-1,0)

import pygame, sys, math, random, gc , numpy as np

gc.collect()

#constants
scr_w = 400
scr_h = 700
g = 9.8
fps = 60
friction=.8



#def addVectors(angle1, length1, angle2, length2):
#    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
#    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
#    length = math.hypot(x, y)
#    angle = 0.5 * math.pi - math.atan2(y, x)
#    return (angle, length)

def check_distance(bouncer,ball):
    x_dist = abs(bouncer.cx - ball.cx)
    y_dist = abs(bouncer.cy - ball.cy)
    hypot = math.sqrt(x_dist**2+y_dist**2)
    radius_sum = bouncer.r+ball.r
    angle = math.atan2(bouncer.cy-ball.cy,bouncer.cx-ball.cx) #y is measured from top so this has to be a little backwards
    if angle<0:
        angle = angle + 2*math.pi
    if hypot<=radius_sum:
        collide = True
    else:
        collide = False
    return(collide, angle, hypot, radius_sum)

def calc_collision(obj1,obj2):
    collide, angle, hypot, radius_sum = check_distance(bouncer=obj1,ball=obj2)
    orig_color1 = obj1.color
    orig_color2 = obj2.color
    if collide == True:
        obj2.collide=True
        obj1.color = (255,0,0)
        obj2.color = (100,100,100)
            
        #reverse rad of ball for new angle of entry        
        rev_ball_rad = (obj2.rad+math.pi) % (2*math.pi)
        
        #take difference in rad_bouncer and angle of enrty
        diff_rad = angle-rev_ball_rad
        
        #double it
        doub_diff_rad = diff_rad*2
        
        # and subtract that from new angle of entry
        new_rad = rev_ball_rad+doub_diff_rad
        
        #calc new xv and yv for ball and set ball.xv and ball.yv to that
        new_xv = math.cos(new_rad )*obj2.v  
        new_yv = math.sqrt(obj2.v**2-new_xv**2)
        new_x = obj2.x+new_xv
        new_y = obj2.y+new_yv
        obj2.x = new_x
        obj2.y = new_y
        obj2.xv = new_xv*1.02
        obj2.yv = new_yv*1.02
    else:
        obj2.collide=False
    obj1.color = orig_color1
    obj2.color = orig_color2

class Object:  
    def __init__(self, color, x, y, w, h, xv, yv, m):
        self.color = color 
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.xv = xv
        self.yv = yv
        self.m = m
    
    @property
    def r(self):
        return self.w
    
    @property
    def cx(self):
        return self.x 

    @property
    def cy(self):
        return self.y 
        
    @property
    def v(self):
        return math.hypot(self.xv,self.yv)
        
    @property
    def rad(self):
        atan2 = math.atan2(self.yv,self.xv)
        if atan2 <0:
            atan2 = atan2 + 2*math.pi
        return atan2
    
    @property
    def deg(self):
        return math.degrees(self.rad) 
    
    @property
    def circle_rect(self):
        return(pygame.draw.circle(screen, self.color, (self.x, self.y), self.w))
        
    @property
    def mom(self):
        return(self.m*self.v)
        


class Ball(Object):
    collide=False
    
    @property
    def calc_new_loc(self):
        xv2 = self.xv 
        x2 = self.x + xv2
        yv2 = self.yv + g/fps
        y2 = self.y + yv2
        
        if x2-self.w<0 or (x2+self.w)>scr_w:
            xv2 = (self.xv *-1) * friction
            x2 = min(max(self.x + xv2,0),scr_w-self.w)
        if y2-self.h<0 or (y2+self.h)>scr_h:
            if self.collide==False:
                yv2 = self.yv*-1 + g/fps
            else:
                yv2 = self.yv*-1
            xv2 = self.xv * friction
            y2 = min(max(self.y + yv2 ,0),scr_h-self.h)
                   
        return(x2,y2,xv2,yv2)
    
    @property
    def rect(self):
        return pygame.Rect.circle(surface=screen, color=self.color, center=(self.cx,self.cy), radius=self.r, width=self.w)
#    https://stackoverflow.com/questions/10866003/pygame-rect-around-circle/10866541  
#   use the link above
    
#    @property
#    def collide_test(self):
#        return pygame.Rect.colliderect(self.rect)
            
        
class Bouncer(Object):
    decel_factor = .99
    
    @property
    def calc_new_loc(self):
        xv2 = self.xv * friction
        x2 = self.x + xv2
        yv2 = self.yv * friction
        y2 = self.y + yv2
        
        if x2-self.w<0 or (x2+self.w)>scr_w:
            xv2 = 0
            x2 = min(max(self.x + xv2,0),scr_w-self.w)
        if y2-self.h<0 or (y2+self.h)>scr_h:
            yv2 = 0
            y2 = min(max(self.y + yv2 ,0),scr_h-self.h)
            
        return(x2,y2,xv2,yv2)


Gary = Bouncer(
        color=(0,0,255)
        , x=scr_w/2
        , y= scr_h*.8
        , w=30, h=30
        ,xv=0, yv=0
        ,  m=5)

Bally = Ball(
        color=(0,255,0)
        , w=10, h=10
        , x=random.randint(scr_w*.1,scr_w*.9) 
        , y= random.randint(scr_h*.1,scr_h*.3)   
        , xv=random.randint(-2,2)
        , yv=random.randint(0,2)
        , m=1)    

def calc_chg_xv_yv(obj1,obj2):
    obj1_new_xv = (obj1.xv * (obj1.m - obj2.m) + (2 * obj2.m * obj2.xv)) / (obj1.m + obj2.m)
    obj1_new_yv = (obj1.yv * (obj1.m - obj2.m) + (2 * obj2.m * obj2.yv)) / (obj1.m + obj2.m)
    return(obj1_new_xv, obj1_new_yv)
    



class Game:
    def menu():
        pass
    
    def main():
        while True:
            # user event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit() 
            
            
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]: Gary.y -= 3
            if pressed[pygame.K_s]: Gary.y += 3
            if pressed[pygame.K_a]: Gary.x -= 3
            if pressed[pygame.K_d]: Gary.x += 3
            
            
            
            
            # update game state
            Bally.x,Bally.y,Bally.xv,Bally.yv = Bally.calc_new_loc
            Gary.x,Gary.y,Gary.xv,Gary.yv = Gary.calc_new_loc
                                 
            #more game state here
            calc_collision(Gary,Bally)
            
            
            
            
            #draw screen
            screen.fill((0, 0, 0))
                    
            # draw game state to screen
            pygame.draw.circle(screen, Gary.color, (int(Gary.x),int(Gary.y)) ,Gary.w)
            pygame.draw.circle(screen, Bally.color, (int(Bally.x),int(Bally.y)) ,Bally.w)
            
            # draw framerate on screen
            framerate = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
            screen.blit(framerate, (scr_w-50,50))
            
        #    draw hypot distance on screen
        #    hypot_dist = font.render(str(hypot_dist),True,pygame.Color('white'))
        #    screen.blit(hypot_dist,(Gary.cx,Gary.cy))
            
            pygame.display.flip()
            clock.tick(fps)
        

        
x = 200
y = 200
blue = (0, 128, 255)

pygame.init()
screen = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption('AI BOUNCER')

font = pygame.font.Font(None, 15)
clock = pygame.time.Clock()    

if __name__=="__main__":
    Game.main()
