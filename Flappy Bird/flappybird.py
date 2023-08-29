
import random
import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup

pygame.init()

#define frame-rate limit
clock=pygame.time.Clock()
fps=60

screen_width=864
screen_height=936

screen= pygame.display.set_mode((screen_width,screen_height)) # create blank game window and initialized it as screen

pygame.display.set_caption('Flappy Bird')

#define font 
font=pygame.font.SysFont('Bauhaus 93',60)

#define color
font_color=(225,255,255)

#define game variables
ground_scroll=0
scroll_speed=4
flying=False
game_over=False
pipe_gap = 150
pipe_frequency=1500 #milliseconds
last_pipe=pygame.time.get_ticks() - pipe_frequency
score=0
pass_pipe=False
#load images
bg=pygame.image.load('img/bg.png')
ground_img=pygame.image.load('img/ground.png')
button_img=pygame.image.load('img/restart.png')

#score
def draw_text(text,font, text_color, x,y):
    img=font.render(text,True, text_color)
    screen.blit(img,(x,y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x=100
    flappy.rect.y=int(screen_height)/2
    global score
    score=0
    


class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for num in range(1,4):
            img=pygame.image.load(f'img/bird{num}.png')
            self.images.append(img) #list containing all the images 
        self.image = self.images[self.index] #take the first image
        self.rect=self.image.get_rect() #box around the image like a hitbox
        self.rect.center=[x,y] #set to their coordinates
        self.vel=0;
        self.clicked=False

    def update(self):
        if flying==True:
            #gravity
            self.vel+=0.5 #increases speed of falling down
            if self.vel>8:
                self.vel=8
            if self.rect.bottom<768: #hits the ground, doesn't go lower
                self.rect.y+=int(self.vel)

        
        if game_over==False: #game is running and I've clicked the start button proceed
            #jump
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False: #left click is 0 and it check if it's being pressed
                self.clicked=True
                self.vel=-10

            if pygame.mouse.get_pressed()[0]==0: #left click is not clicked it's false
                self.clicked=False



            #handle the animation
            self.counter+=1
            flap_cooldown=5
            #if self counter > flap counter, once you've iterated 5 times, move on to the next one 
            if self.counter>flap_cooldown:
                self.counter=0
                self.index+=1
                if self.index>=len(self.images): #animation is complete
                    self.index=0
            self.image=self.images[self.index]

            #rotate the bird
            self.image=pygame.transform.rotate(self.images[self.index],self.vel * -2) #at whatever image we're at, by default this is anticlock wise 
        else:
            self.image=pygame.transform.rotate(self.images[self.index],-90)  


class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/pipe.png")
        self.rect=self.image.get_rect()
        #position 1 is from top, -1 is from bottom
        if position==1:
            #flip the image
            self.image=pygame.transform.flip(self.image,False, True)
            self.rect.bottomleft=[x,y-int(pipe_gap/2)]
        if position==-1:
            self.rect.topleft=[x,y+int(pipe_gap/2)] #position
    
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right<0:
            self.kill()

class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)  
    def draw(self):
        action=False
        pos=pygame.mouse.get_pos() #list

        #check if mouse is over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                #mouse over the button and being clicked
                action=True
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action

    
        

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy=Bird(100,int(screen_height)/2)
        
button=Button(screen_width//2 - 50, screen_height//2 -100, button_img)
bird_group.add(flappy)



run=True

while run:

    clock.tick(fps) # fix it to 60fps

    #draw background
    screen.blit(bg,(0,0)) # to show images use blit function, start from top left corner

    bird_group.draw(screen)
    bird_group.update() 
    pipe_group.draw(screen)
    

    screen.blit(ground_img,(ground_scroll,768)) #this is more so beacuse once we hit the ground we stop scrolling 

    #check the score
    if len(pipe_group) > 0:
          #pipes group are like lists, containing all of the pipes but we need the one we're about to pass through 
          if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe==False:
              pass_pipe=True

          if pass_pipe==True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score+=1
                    pass_pipe=False
    
    draw_text(str(score),font,font_color, int(screen_width/2), 20)
              
              #enter the pipe region but not went out of it 


    #look for collision
    if pygame.sprite.groupcollide(bird_group,pipe_group, False, False) or flappy.rect.top<0:
        #this more like shooting where bird or pipe would be deleted hence both are False;
        game_over=True




    if flappy.rect.bottom >= 768:
        game_over=True
        flying=False
        reset_game()




    #draw and scroll the ground
    if game_over==False and flying==True:
        #generate new pipes
        time_now=pygame.time.get_ticks()
        if time_now-last_pipe>pipe_frequency:
            pipe_height=random.randint(-100,100)
            btm_pipe=Pipe(screen_width,int(screen_height)/2 + pipe_height, -1)
            top_pipe=Pipe(screen_width,int(screen_height)/2 + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now


        ground_scroll-=scroll_speed
        if abs(ground_scroll)>35:
            ground_scroll=0
        pipe_group.update()


    #check for game over and reset
    if game_over==True:
        if button.draw()==True:
            game_over=False



    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.MOUSEBUTTONDOWN and flying==False and game_over==False:
            flying=True
    

    pygame.display.update()    

pygame.quit()
 
