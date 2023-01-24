import pygame,sys,random
from pygame.locals import *

WINDOWWIDTH = 400
WINDOWHEIGHT = 600

BIRDWIDTH = 60
BIRDHEIGHT = 45
G=0.5
SPEEDFLY=-8
BIRDIMG=pygame.image.load('img/bird/Transparent PNG/frame-1.png')
BIRDIMG=pygame.transform.scale(BIRDIMG,(60,45))

COLUMNWIDTH = 60
COLUMNHEIGHT = 500
BLANK = 200
DISTANCE = 180
COLUMNSPEED = 2
COLUMNIMG = pygame.image.load('img/column.png')
COLUMNIMG = pygame.transform.scale(COLUMNIMG,(45,500))

BACKGROUND = pygame.image.load('img/background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND,(400,600))
pygame.init()

fps=60
fpsClock= pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption('Flappy bird')
def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False
def isGameOver(bird, columns):
    for i in range(3):
        rectBird = [bird.x, bird.y, bird.width, bird.height]
        rectColumn1 = [columns.ls[i][0], columns.ls[i][1] - columns.height, columns.width, columns.height]
        rectColumn2 = [columns.ls[i][0], columns.ls[i][1] + columns.blank, columns.width, columns.height]
        if rectCollision(rectBird, rectColumn1) == True or rectCollision(rectBird, rectColumn2) == True:
            return True
    if bird.y + bird.height < 0 or bird.y + bird.height > WINDOWHEIGHT:
        return True
    return False
class column():
    def __init__(self):
        self.width = COLUMNWIDTH
        self.height = COLUMNHEIGHT
        self.blank = BLANK
        self.distance = DISTANCE
        self.speed = COLUMNSPEED
        self.surface = COLUMNIMG
        self.ls = []
        for i in range(3):
            x=i*self.distance+WINDOWWIDTH
            y=random.randrange(60,WINDOWHEIGHT - self.blank - 60,50)
            self.ls.append([x,y])
    def draw(self):
        for i in range(3):
            DISPLAYSURF.blit(self.surface,(self.ls[i][0], self.ls[i][1] - self.height))
            DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] + self.blank))
    def update(self):
        for i in range(3):
            self.ls[i][0]-=self.speed
        if self.ls[0][0] <0:
            self.ls.pop(0)
            x=self.ls[1][0] + self.distance
            y=random.randrange(60,WINDOWHEIGHT - self.blank - 60,50)
            self.ls.append([x,y])
class BIRD():
    def __init__(self):
        self.width=BIRDWIDTH
        self.height=BIRDHEIGHT
        self.x=(WINDOWWIDTH-BIRDWIDTH)/2
        self.y=(WINDOWHEIGHT-BIRDHEIGHT)/2
        self.speed=0
        self.surface=BIRDIMG
    def draw(self):
        DISPLAYSURF.blit(self.surface,(self.x,self.y))
    def update(self,Space):
        self.y+=self.speed + 0.5*G
        self.speed+=G
        if self.y>=WINDOWHEIGHT-self.height:
            self.y=WINDOWHEIGHT-self.height
        if(Space == True):
            self.speed = SPEEDFLY
class Score():
    def __init__(self):
        self.score = 0
        self.addScore = True
    def draw(self):
        font = pygame.font.SysFont('consolas',40)
        scoreSurface = font.render('Score: ' + str(self.score),True,(0,0,0))
        textSize= scoreSurface.get_size()
        DISPLAYSURF.blit(scoreSurface,(int((WINDOWWIDTH - textSize[0])/2), 100))
    def update(self,bird,column):
        collision = False
        for i in range(3):
            rectColumn=[column.ls[i][0]+column.width,column.ls[i][1],1,column.blank]
            rectBird=[bird.x,bird.y,bird.width,bird.height]
            if rectCollision(rectBird,rectColumn) == True:
                collision=True
                break
        if collision==True and self.addScore == True:
            self.score+=1
            self.addScore = False
        if collision==False:
            self.addScore=True
def gameStart(bird):
    bird.__init__()

    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('FLAPPY BIRD', True, (255, 0, 0))
    headingSize = headingSuface.get_size()
    
    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Press Space to start', True, (0, 0, 0))
    commentSize = commentSuface.get_size()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return

        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        bird.draw()
        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
        DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 500))

        pygame.display.update()
        fpsClock.tick(fps)
def gamePlay(bird, columns, score):
    bird.__init__()
    columns.__init__()
    score.__init__()
    while True:
        press = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    press = True
        if isGameOver(bird, columns) == True:
            return
        DISPLAYSURF.blit(BACKGROUND,(0,0))
        bird.draw()
        bird.update(press)
        columns.draw()
        columns.update()
        score.draw()
        score.update(bird,columns)
        pygame.display.update()
        fpsClock.tick(fps)
def gameOver(bird, columns, score):
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('GAMEOVER', True, (255, 0, 0))
    headingSize = headingSuface.get_size()
    
    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Press "space" to replay', True, (0, 0, 0))
    commentSize = commentSuface.get_size()

    font = pygame.font.SysFont('consolas', 30)
    scoreSuface = font.render('Score: ' + str(score.score), True, (0, 0, 0))
    scoreSize = scoreSuface.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return
        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        columns.draw()
        bird.draw()
        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
        DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 500))
        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - scoreSize[0])/2), 160))
        pygame.display.update()
        fpsClock.tick(fps)
def main():
    bird = BIRD()
    columns = column()
    score = Score()
    while True:
        gameStart(bird)
        gamePlay(bird,columns,score)
        gameOver(bird,columns,score)
if __name__ == '__main__':
    main()
