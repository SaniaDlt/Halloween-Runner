import pygame
from sys import exit
from random import randint
from random import choice

def ratio_calc(x,y):
    ratio=x/y
    return (180*ratio,180)

def getPoint(player,points):
    global pointCounter
    if pygame.sprite.spritecollide(player.sprite,points,True):
        pointCounter+=1
        brain_music.play()
    return points

def display_score():
    point_surf=point_font.render(f'Score : {pointCounter}',True ,(255,0,0))
    point_rect=point_surf.get_rect(center=(400,50))
    screen.blit(point_surf,point_rect)
    
def collision(player,obstaclegroup):
    if pygame.sprite.spritecollide(player.sprite,obstaclegroup,False):
        game_music.stop()
        game_over_music.play()
        obstacle_group.empty()
        points.empty()
        return 2
    return 1

def start_idle():
    global idle_index
    idle_index+=0.1
    if idle_index>=len(boy_frames):
        idle_index=0
    else:
        screen.blit(girl_frames[int(idle_index)],idle_girlrect)
        screen.blit(boy_frames[int(idle_index)],idle_boyrect)
        
    
#Class Player
class Player(pygame.sprite.Sprite):
    
    def __init__(self,code):
        super().__init__()
        self.point=0
        self.player_jump=[]
        self.player_run=[]
        self.gravity=0
        global identity
        if code:
            for i in range(5,11):
                image=pygame.image.load('Game/Boy/run/Run'+str(i)+'.png').convert_alpha()
                x=image.get_width()
                y=image.get_height()
                image=pygame.transform.scale(image,ratio_calc(x,y))
                self.player_run.append(image)
            identity='Boy'
            for i in range(1,8):
                image=pygame.image.load('Game/Boy/jump/Jump'+str(i)+'.png').convert_alpha()
                x=image.get_width()
                y=image.get_height()
                image=pygame.transform.scale(image,ratio_calc(x,y))
                self.player_jump.append(image)
                 
        else:
            for i in range(5,11):
                image = pygame.image.load("Game/Girl/run/Run"+str(i)+".png").convert_alpha()
                x=image.get_width()
                y=image.get_height()
                image=pygame.transform.scale(image,ratio_calc(x,y))
                self.player_run.append(image)
            for i in range(1,8):
                image = pygame.image.load("Game/Girl/jump/Jump"+str(i)+".png").convert_alpha()
                x=image.get_width()
                y=image.get_height()
                image=pygame.transform.scale(image,ratio_calc(x,y))
                self.player_jump.append(image)
            identity='Girl'
        self.index=0
        self.index_jump=0
        self.image=self.player_run[self.index]
        self.rect=self.image.get_rect(midbottom=(76,406))
        
                
    def movement(self):
        key = pygame.key.get_pressed()
        if (key[pygame.K_SPACE] or key[pygame.K_UP])and self.rect.bottom>=groundpix:
            self.gravity=-25
        
    def gravity_apply(self):
        self.gravity+=1
        self.rect.y+=self.gravity
        if self.rect.bottom>groundpix:
            self.rect.bottom=groundpix        

    def animation(self):
        if self.rect.bottom<groundpix:
            self.index_jump+=0.12
            if self.index_jump>=len(self.player_jump):
                self.index_jump=0
            self.image=self.player_jump[int(self.index_jump)]
        else:
            self.index+=0.15
            if self.index>=len(self.player_run):
                self.index=0
            self.image=self.player_run[int(self.index)]
    
    def update(self):
        self.movement()
        self.gravity_apply()
        self.animation()
#Class brain (points)
class Brain(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("Game/Brain.png").convert_alpha()
        self.image=pygame.transform.scale2x(self.image)
        self.rect=self.image.get_rect(midbottom=(randint(900,1000),randint(220,400)))
    def update(self):
        self.rect.x-=7
        self.destroy()
    def destroy(self):
        if self.rect.x<=-100:
            self.kill()
    


#Class obstacle
class obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        self.obstacle_run=[]
        self.obstacle_index=0
        if type=='Bat':
            for i in range(1,5):
                image=pygame.image.load(f'Game/Obstacle/Bat/Bat{i}.png')
                image=pygame.transform.scale2x(image)
                self.obstacle_run.append(image)
            self.image=self.obstacle_run[self.obstacle_index]
            self.rect=self.image.get_rect(midbottom=(randint(900,1100),220))
             
        else:
            for i in range(1,7):
                image=pygame.image.load(f'Game/Obstacle/Fire/Explosion_{i}.png')
                image=pygame.transform.scale(image,(64,64))
                self.obstacle_run.append(image)
            self.image=self.obstacle_run[self.obstacle_index]
            self.rect=self.image.get_rect(midbottom=((randint(900,1100),groundpix)))

    def obstacle_animation(self):
        self.obstacle_index+=0.1
        self.rect.x-=6
        if self.obstacle_index>=len(self.obstacle_run):
            self.obstacle_index=0
        else:
            self.image=self.obstacle_run[int(self.obstacle_index)]
    
    def destroy(self):
        if self.rect.x<=-100:
            self.kill()
                  
    def update(self):
        self.obstacle_animation()
        self.destroy()
    
#Main            
pygame.init()
groundpix = 406
screen=pygame.display.set_mode((800,450))
pygame.display.set_caption('Halloween Runner')
clock =pygame.time.Clock()
isActive=True
background = pygame.image.load('Game/Background/background1.png').convert()
background=pygame.transform.scale(background,(800,450))

start_background = pygame.image.load('Game/Background/startbackground.jpg').convert()
start_background=pygame.transform.scale(start_background,(800,450))

end_background=pygame.image.load('Game/Background/endbackground.jpg').convert()
end_background=pygame.transform.scale(end_background,(800,450)).convert()

dead_girl=pygame.image.load('Game/End/GirlDead.png').convert_alpha()
dead_girl=pygame.transform.scale(dead_girl,ratio_calc(dead_girl.get_width(),dead_girl.get_height()))
dead_girl_rect=dead_girl.get_rect(midbottom=(400,300))

dead_boy=pygame.image.load('Game/End/BoyDead.png').convert_alpha()
dead_boy=pygame.transform.scale(dead_boy,ratio_calc(dead_boy.get_width(),dead_boy.get_height()))
dead_boy_rect=dead_boy.get_rect(midbottom=(400,300))

point_font=pygame.font.Font('halloween/Halloween.otf',50)

end_message=pygame.font.Font('halloween/Halloween.otf',50)
end_message_surf=end_message.render('YOU DIED!',True,(255,0,0))
end_message_rect=end_message_surf.get_rect(midbottom=(400,100))

player=pygame.sprite.GroupSingle()
pointCounter=0
#Brain
points=pygame.sprite.Group()

whatscreen=0

identity=''
#Obstacle
obstacle_group=pygame.sprite.Group()
#Idle Start
idle_index=0
girl_frames=[]
for i in range(1,5):
    image=pygame.image.load(f"Game/Start/GirlIdle/Idle{i}.png").convert_alpha()
    x=image.get_width()
    y=image.get_height()
    image=pygame.transform.scale(image,ratio_calc(x,y))
    girl_frames.append(image)
idle_girlrect=girl_frames[idle_index].get_rect(midbottom=(300,groundpix))

boy_frames=[]
for i in range(1,5):
    image=pygame.image.load(f'Game/Start/BoyIdle/Idle{i}.png').convert_alpha()
    image=pygame.transform.scale(image,ratio_calc(image.get_width(),image.get_height()))
    boy_frames.append(image)
idle_boyrect=boy_frames[idle_index].get_rect(midbottom=(500,groundpix))
#Event 
brain_event=pygame.USEREVENT +1
pygame.time.set_timer(brain_event,2000)

obstacle_event=pygame.USEREVENT+2
pygame.time.set_timer(obstacle_event,3000)
#Music
pygame.mixer.init()
brain_music=pygame.mixer.Sound('audio/brain.mp3')
brain_music.set_volume(1)
game_over_music=pygame.mixer.Sound('audio/gameover.mp3')
game_over_music.set_volume(1)
game_music=pygame.mixer.Sound('audio/game.mp3')
game_music.set_volume(0.1)
game_music.play(loops=-1)

#File
highestRecord=0
file=open("record.txt","r")
record=file.read()
if record !="":
    highestRecord=int(record)
file.close()


while isActive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isActive=False
            file=open("record.txt","w")
            file.write(str(highestRecord))
            file.close()
            exit()
        if whatscreen==0:
            if pygame.mouse.get_pressed()[0]:
                mouse_x,mouse_y=pygame.mouse.get_pos()
                if idle_girlrect.collidepoint(mouse_x,mouse_y):
                    whatscreen=1
                    player.add(Player(0))
                elif idle_boyrect.collidepoint(mouse_x,mouse_y):
                    player.add(Player(1))
                    whatscreen=1
        if whatscreen==1:
            if event.type == brain_event:
                points.add(Brain())
            if event.type==obstacle_event:
                obstacle_group.add(obstacle(choice(["Fire","Fire","Bat"])))
        if event.type==pygame.K_SPACE:
            whatscreen=0
            pointCounter=0
            
    if whatscreen ==0:
        screen.blit(start_background,(0,0))
        start_idle()
        

    elif whatscreen==1 :
        screen.blit(background,(0,0))
        player.draw(screen)
        player.update()
        points.draw(screen)
        points.update()
        points=getPoint(player,points)
        display_score()
        obstacle_group.draw(screen)
        obstacle_group.update()
        whatscreen=collision(player,obstacle_group)       
        

    elif whatscreen==2:
        if pointCounter>highestRecord:
            highestRecord=pointCounter
        screen.fill('#052347')
        if identity=='Girl':
            screen.blit(dead_girl,dead_girl_rect)
        else:
            screen.blit(dead_boy,dead_boy_rect)
        screen.blit(end_message_surf,end_message_rect)
        point_message=pygame.font.Font('halloween/Halloween.otf',50)
        point_message_surf=point_message.render(f'the brain you eat {pointCounter}   '+f' Highest Record : {highestRecord}',True,(255,0,0))
        point_message_rect=point_message_surf.get_rect(midbottom=(400,400))
        screen.blit(point_message_surf,point_message_rect)
          
    pygame.display.update()

    clock.tick(60)

    
