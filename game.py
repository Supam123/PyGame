import pygame
pygame.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound("bullet.wav")
hitSound = pygame.mixer.Sound("ouch.wav")
music = pygame.mixer.music.load("music_john.mp3")
pygame.mixer.music.play(-1)


score  = 0
class player(object):
    def __init__(self,x,y,width,height):
         self.x = x
         self.y = y
         self.width = width
         self.height = height
         self.vel = 5
         self.isJump = False
         self.left = False
         self.right = False
         self.walkCount = 0
         self.jumpCount = 10
         self.standing = True # keeps tarck if hes moving or not
         self.hitbox = (self.x + 17, self.y + 11, 29, 52)
    # hitbox dimensions


    def draw(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing: # if hes not standing
             if self.left: #if its left is true means place walk left pics on screen
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
             elif self.right: ##if its right is true means place walk left pics on screen
                 win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                 self.walkCount += 1
        else:
            # we want him to face the last direction
            # we will  keep traack of that
            # so if right ws true
            # we will wwant him to face right so wwalkright pictureee zero faces right at x,y current
            # value
            if self.right:
                win.blit(walkRight[0],(self.x,self.y))
            else:
                win.blit(walkLeft[0],(self.x,self.y))
        self.hitbox  = (self.x + 17,self.y+11,29,52) # updating
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 100  # We are resetting the player position
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

        # After we are hit we are going to display a message to the screen for
        # a certain period of time


#bullets firing
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius =radius
        self.color = color
        self.facing  = facing
        self.vel = 8*facing

    def draw(self,win):
        #bullet shape and drawing
        # self x and slef y are locations of bull et on screen
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)



class enemy(object):

    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]


    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]



    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x,self.end] # this is the start and the endpoint of the hero(x1,x2)

        self.walkCount = 0
        self.vel = 3
        self.hitbox  = (self.x+17,self.y+2,31,57) # hitbox dimensions
        self.health = 30
        self.visible = True


    def draw(self,win):
        #everytime we draw , we move the charcter then draw
        self.move()
        if self.visible: # if hes alive then only draw

            if self.walkCount +1 >= 33: # when it reaches here we wwanna bring back the index
                self.walkCount = 0
            if self.vel > 0: # we moving right
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
            else:# we moving left
                win.blit(self.walkLeft[self.walkCount//3] , (self.x, self.y))
                self.walkCount += 1
            self.hitbox  = (self.x+17,self.y+2,31,57) # hitbox dimensions


            pygame.draw.rect(win,(255,0,0) ,(self.hitbox[0],self.hitbox[1]-20 ,50,10))
            # incraese por decrease the leter of green or red by changing the width of the
            ## leter
            pygame.draw.rect(win,(0,128,0),(self.hitbox[0],self.hitbox[1]-20,50-(5*(10-self.health)),10))
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def move(self):
        if self.vel > 0: # we are moving right
            # if the current position + velocity is less than endpoint we want charcter to  stop
            # so keepon moving untill u hit endpoint
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                # if we are greater than endpoint we want it to move in other direction
                self.vel  = self.vel * -1 # multiply by -1 to flip 180 degree to change direction
                self.walkCount = 0
        else:
            # if the current position + velocity is greater  than startpoint keep moving

            if self.x - self.vel > self.path[0]:
                self.x += self.vel #vel is negative so we add in order to subtract
            else:
                # if we pass over start point we wanna change direction
                self.vel = self.vel * -1  # multiply by -1 to flip 180 degree to change direction
                self.walkCount = 0







    def hit(self):

        if self.health > 1:
            self.health -= 1
        else:
            # enemy dead
            self.visible = False
        print("Hit")


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render("Score : " + str(score),1,(0,0,0)) #now the textt is ready as surface just blit it to the wondow


    win.blit(text,(350,10))
    #DRAWING MAN , BULLETS , ENEMY
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)# drawing bullets with the py game circle draw method
        # eaach bullet has attribte defined when space pressed

    pygame.display.update()


# mainloop
font = pygame.font.SysFont('comicsans',30,True)
man = player(100, 410, 64, 64)
goblin = enemy(200,415,64,64,450)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)
    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
         if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5


    if shootLoop > 0:
        shootLoop +=1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for bullet in bullets:
        #ist part if is if  we are above the bottom of the hitbox
        #2nd part is if we are below the top of the rectangle
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                # so if we are in that range
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hitSound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
        if bullet.x < 500 and bullet.x > 0: # if the bullet is  inside the frame then fire it
           bullet.x += bullet.vel
        else:
            #when off the screen
            bullets.pop(bullets.index(bullet))
    keys = pygame.key.get_pressed()

    # firing bullet on pressing space
    # whenever we press space we create a bullet so wee add it inot bullets
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left: #shooting the bullets in left direction
            facing = -1
        else:
            facing  = 1
            # number of bullets we want to draw on screen at a time
        if len(bullets) < 5:
            # creating a bullet and adding to list of bullets with its attributes
            bullets.append(projectile(round(man.x + man.width  // 2),round(man.y+man.height//2),6,(255,154,0),facing ))
        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel: # if left key press decrease x
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:# if right key press increase x
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False

    else:
        man.standing = True
        man.walkCount = 0

    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg # to craete a parabloa way of jumpping  quadratic eqn
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()

