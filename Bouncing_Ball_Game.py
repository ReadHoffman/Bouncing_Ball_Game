# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 16:15:35 2020

@author: Read
"""

import pygame, sys, math, random, gc , numpy as np, statistics 

gc.collect()

#constants
scr_w = 400
scr_h = 700
g = -9.8
g_rad = math.pi*1.5
fps = 60
friction=.9

def collision(r1,r2):
    ca = r1.radians_from_obj(r2)[0] #ca means contact angle
    xv_new_r1 = ( r1.v*math.cos(r1.rad-ca)*(r1.m-r2.m)+2*r2.mom*math.cos(r2.rad-ca) )/(r1.m+r2.m)*math.cos(ca) + r1.v*math.sin(r1.rad-ca)*math.cos(ca+math.pi/2)
    yv_new_r1 = ( r1.v*math.cos(r1.rad-ca)*(r1.m-r2.m)+2*r2.mom*math.cos(r2.rad-ca) )/(r1.m+r2.m)*math.cos(ca) + r1.v*math.sin(r1.rad-ca)*math.sin(ca+math.pi/2)
   #convert to v and rad
    v_new = math.hypot(yv_new_r1,xv_new_r1)
    rad_new = math.atan2(yv_new_r1,xv_new_r1)
    
    return v_new , rad_new

class Wall():
    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.r = 0
        self.x = statistics.mean([self.x1,self.x2])
        self.y = statistics.mean([self.y1,self.y2])
        self.color = (255,255,255)
        self.m = 1000
        self.v = 0
        self.mom = 0
        self.rad = 0

    @property
    def line_rect(self):
        return(pygame.draw.line(screen, self.color, ( int(self.x1) , int(self.y1) ), ( int(self.x2) , int(self.y2) ), 1) )

Wall_W = Wall(scr_w*.1,scr_h*.1,scr_w*.1,scr_h*.9)
Wall_S = Wall(scr_w*.1,scr_h*.9,scr_w*.9,scr_h*.9)
Wall_E = Wall(scr_w*.9,scr_h*.9,scr_w*.9,scr_h*.1)
Wall_N = Wall(scr_w*.9,scr_h*.1,scr_w*.1,scr_h*.1)
wall_objs = [Wall_W,Wall_S,Wall_E,Wall_N]

class Object(pygame.sprite.Sprite):  
    def __init__(self, color, x, y, w, h, m, v, rad):
        self.color = color 
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.m = m
        self.v = v
        self.rad = rad
             
    @property
    def xv(self):
        return math.cos(self.rad)*self.v
    
    @property
    def yv(self):
        new_yv = math.sin(self.rad)*self.v + g/fps #make sure to add change due to gravity
        if self.y-new_yv+self.h>= Wall_S.y: new_yv = math.sin(self.rad)*self.v
        return new_yv

    @property
    def update_v_rad(self):
        self.v = math.hypot(self.yv,self.xv)
        self.rad =  math.atan2(self.yv,self.xv)
    

    @property
    def next_x(self):
        return self.x+self.xv
    
    @property
    def next_y(self):
        return self.y-self.yv #must subtract y delta since pygame draws from top left

    @property
    def update_xy(self):
        self.x = self.next_x
        self.y = self.next_y 
    
    @property
    def r(self):
        return int(self.w)
    
    @property
    def deg(self):
        return math.degrees(self.rad) 
    
    @property
    def circle_rect(self):
        return pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r) 
        
    @property
    def mom(self):
        return(self.m*self.v)

    def check_collide(self,obj):
        # control for wall collisions
        if obj.__class__.__name__ =='Wall':
            if obj.x == obj.x1:
                obj.y = self.y
            else:
                obj.x = self.x
        else:
            pass
        
        x_dist = abs(obj.x - self.next_x)
        y_dist = abs(obj.y - self.next_y)
        next_hypot = math.hypot(y_dist,x_dist)
        radius_sum = obj.r+self.r
        if next_hypot<radius_sum:
            return True
        else:
            False

    def radians_from_obj(self,obj):
        # control for wall collisions
        if obj.__class__.__name__ =='Wall':
            if obj.x == obj.x1:
                obj.y = self.y
            else:
                obj.x = self.x
        else:
            pass

        x_dist = abs(obj.x - self.x)
        y_dist = abs(obj.y - self.y)
        hypot = math.hypot(y_dist,x_dist)
        radius_sum = obj.r+self.r
        angle = math.atan2(obj.y-self.y,self.x-obj.x) #y is measured from top so this has to be a little backwards
        if angle<0:
            angle = angle + 2*math.pi
        return angle, hypot, radius_sum







#class Ball(Object):
    #collide=False
    #still_collide = False

    #def bouncer_collision(self, bouncer):
    #    x_dist = abs(bouncer.next_x - self.next_x)
    #    y_dist = abs(bouncer.next_y - self.next_y)
    #    hypot = math.sqrt(x_dist**2+y_dist**2)
    #    radius_sum = bouncer.r+self.r
    #    angle = math.atan2(bouncer.y-self.y,bouncer.x-self.x) #y is measured from top so this has to be a little backwards
    #    if angle<0:
    #        angle = angle + 2*math.pi

    #    fut_dist_from_bouncer = math.hypot(self.x+self.xv,self.y+self.yv)

    #    if hypot>radius_sum:
    #        self.collide = False
    #        self.still_collide = False
    #        self.color = (255,0,0)
    #    else:
    #        if self.still_collide==True:
    #            pass
    #        else:
    #            self.collide = True
    #            self.color = (100,255,150)
            
    #            #reverse rad of ball for new angle around which we will transform the entry/exit vector       
    #            rev_ball_rad = (self.rad+math.pi) % (2*math.pi)
        
    #            #take difference in rad_bouncer and angle of enrty
    #            diff_rad = angle-rev_ball_rad
        
    #            #double it
    #            doub_diff_rad = diff_rad*2
        
    #            # and subtract that from new angle of entry
    #            new_rad = rev_ball_rad+doub_diff_rad
        
    #            #calc new xv and yv for ball and set ball.xv and ball.yv to that
    #            new_xv = math.cos(new_rad )*self.v  
    #            new_yv = math.sqrt(self.v**2-new_xv**2)
    #            new_x = self.x+new_xv
    #            new_y = self.y+new_yv
            
    #            if math.hypot(bouncer.y-new_y,bouncer.x+new_x)<radius_sum:
    #                self.still_collide=True

    #            #assign vals
    #            self.x = new_x
    #            self.y = new_y
    #            self.xv = new_xv
    #            self.yv = new_yv


    #@property
    #def calc_new_loc(self):
    #    xv2 = self.xv 
    #    x2 = self.x + xv2
    #    yv2 = self.yv + g/fps
    #    y2 = self.y + yv2
        
    #    if x2-self.w<0 or (x2+self.w)>scr_w:
    #        xv2 = (self.xv *-1) * friction
    #        x2 = min(max(self.x + xv2,0),scr_w-self.w)
    #    if y2-self.h<0 or (y2+self.h)>scr_h:
    #        yv2 = self.yv*-1 + g/fps
    #        xv2 = self.xv * friction
    #        y2 = min(max(self.y + yv2 ,0),scr_h-self.h)
                   
    #    return(x2,y2,xv2,yv2)
    
    #@property
    #def rect(self):
    #    return pygame.Rect.circle(surface=screen, color=self.color, center=(self.x,self.y), radius=self.r, width=self.w)
        
class Bouncer(Object):
    decel_factor = .99
    
    @property
    def calc_new_loc(self):
        yv = self.yv
        xv = self.xv

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]: yv = yv + .3
        if pressed[pygame.K_s]: yv = yv - .3
        if pressed[pygame.K_a]: xv = xv - .3
        if pressed[pygame.K_d]: xv = xv + .3
        
        xv2 = xv * friction
        x2 = self.x + xv2
        yv2 = yv * friction
        y2 = self.y - yv2
        
        if x2-self.w<0 or (x2+self.w)>scr_w:
            xv2 = 0
            x2 = min(max(self.x - self.w,0),scr_w-self.w)
        if y2-self.h<0 or (y2+self.h)>scr_h:
            yv2 = 0
            y2 = min(max(self.y - self.h ,0),scr_h-self.h)
        #convert to v and rad
        v_new = math.hypot(yv2,xv2)
        rad_new = math.atan2(yv2,xv2)
        return v_new, rad_new

    #self, color, x, y, w, h, m, v, rad
Gary = Bouncer(
        color=(0,0,255)
        , x=scr_w/2
        , y= scr_h*.8
        , w=30, h=30
        , m=5, v=0
        , rad=0)

Bally = Object(
        color=(0,255,0)
        , w=10, h=10
        , x=random.randint(scr_w*.1,scr_w*.9) 
        , y= random.randint(scr_h*.1,scr_h*.3)  
        , m=1 , v=.5
        ,rad = math.radians(random.randint( 45, 135) ) )    

  

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
            
            #includes user keypresses
            Gary.v, Gary.rad = Gary.calc_new_loc



            # update game state
            Bally.update_xy
            Bally.update_v_rad

            #check for collisions        
            if Bally.check_collide(Gary)==True:
                Bally.v, Bally.rad = collision(Bally,Gary)
                Gary.v, Gary.rad = collision(Gary,Bally)
            for wall in wall_objs:
                if Bally.check_collide(wall) == True:
                    Bally.v, Bally.rad = collision(Bally,wall)           
                    

            #draw screen
            screen.fill((0, 0, 0))
                    
            # draw game state to screen
            for wall in wall_objs:
                wall.line_rect
            Gary.circle_rect
            Bally.circle_rect
            
            # draw framerate on screen
            framerate = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
            screen.blit(framerate, (scr_w-50,50))
            
        #    draw hypot distance on screen #for debugging
            #Bally_rad = font.render(str(Bally.rad),True,pygame.Color('white'))
            #screen.blit(Bally_rad,(Gary.x,Gary.y))
            
            pygame.display.flip()
            clock.tick(fps)
        
 

if __name__=="__main__":
    Game.main()
