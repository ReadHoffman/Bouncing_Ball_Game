# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 16:15:35 2020

@author: Read
"""

import pygame, sys, math, random, gc , numpy as np

gc.collect()

#constants
scr_w = 400
scr_h = 700
g = 9.8
fps = 60
friction=.9



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

    @property
    def next_x(self):
        return(self.x+self.xv)

    @property
    def next_y(self):
        return(self.y-self.yv)
        


class Ball(Object):
    collide=False
    still_collide = False

    def bouncer_collision(self, bouncer):
        x_dist = abs(bouncer.next_x - self.next_x)
        y_dist = abs(bouncer.next_y - self.next_y)
        hypot = math.sqrt(x_dist**2+y_dist**2)
        radius_sum = bouncer.r+self.r
        angle = math.atan2(bouncer.y-self.y,bouncer.x-self.x) #y is measured from top so this has to be a little backwards
        if angle<0:
            angle = angle + 2*math.pi

        fut_dist_from_bouncer = math.hypot(self.x+self.xv,self.y+self.yv)

        if hypot>radius_sum:
            self.collide = False
            self.still_collide = False
            self.color = (255,0,0)
        else:
            if self.still_collide==True:
                pass
            else:
                self.collide = True
                self.color = (100,255,150)
            
                #reverse rad of ball for new angle around which we will transform the entry/exit vector       
                rev_ball_rad = (self.rad+math.pi) % (2*math.pi)
        
                #take difference in rad_bouncer and angle of enrty
                diff_rad = angle-rev_ball_rad
        
                #double it
                doub_diff_rad = diff_rad*2
        
                # and subtract that from new angle of entry
                new_rad = rev_ball_rad+doub_diff_rad
        
                #calc new xv and yv for ball and set ball.xv and ball.yv to that
                new_xv = math.cos(new_rad )*self.v  
                new_yv = math.sqrt(self.v**2-new_xv**2)
                new_x = self.x+new_xv
                new_y = self.y+new_yv
            
                if math.hypot(bouncer.y-new_y,bouncer.x+new_x)<radius_sum:
                    self.still_collide=True

                #assign vals
                self.x = new_x
                self.y = new_y
                self.xv = new_xv
                self.yv = new_yv


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
            yv2 = self.yv*-1 + g/fps
            xv2 = self.xv * friction
            y2 = min(max(self.y + yv2 ,0),scr_h-self.h)
                   
        return(x2,y2,xv2,yv2)
    
    @property
    def rect(self):
        return pygame.Rect.circle(surface=screen, color=self.color, center=(self.x,self.y), radius=self.r, width=self.w)
        
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
            x2 = min(max(self.x - self.w,0),scr_w-self.w)
        if y2-self.h<0 or (y2+self.h)>scr_h:
            yv2 = 0
            y2 = min(max(self.y - self.h ,0),scr_h-self.h)
            
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
    

pygame.init()
screen = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption('AI BOUNCER')

font = pygame.font.Font(None, 15)
clock = pygame.time.Clock()  

class Game:
    def menu():
        pass
    
    def main():
        while True:
            # user event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        #sys.exit() 
            
            
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]: Gary.y -= 3
            if pressed[pygame.K_s]: Gary.y += 3
            if pressed[pygame.K_a]: Gary.x -= 3
            if pressed[pygame.K_d]: Gary.x += 3
            
            
            
            
            # update game state
            Bally.x,Bally.y,Bally.xv,Bally.yv = Bally.calc_new_loc
            Gary.x,Gary.y,Gary.xv,Gary.yv = Gary.calc_new_loc
                                 
            #more game state here
            Bally.bouncer_collision(Gary)


            
            #draw screen
            screen.fill((0, 0, 0))
                    
            # draw game state to screen
            pygame.draw.circle(screen, Gary.color, (int(Gary.x),int(Gary.y)) ,Gary.w)
            pygame.draw.circle(screen, Bally.color, (int(Bally.x),int(Bally.y)) ,Bally.w)
            
            # draw framerate on screen
            framerate = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
            screen.blit(framerate, (scr_w-50,50))
            
        #    draw hypot distance on screen #for debugging
            Bally_rad = font.render(str(Bally.rad),True,pygame.Color('white'))
            screen.blit(Bally_rad,(Gary.x,Gary.y))
            
            pygame.display.flip()
            clock.tick(fps)
        

        
x = 200
y = 200
blue = (0, 128, 255)

  

if __name__=="__main__":
    Game.main()
