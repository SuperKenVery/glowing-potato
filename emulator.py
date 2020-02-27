import pygame
class vector:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __add__(self,x):
        return vector(self.x+x.x,self.y+x.y)
class position:
    def __init__(self,x,y):
        self.x=x
        self.y=y
class thing:
    def __init__(self,v,a,pos):
        self.v=v
        self.a=a
        self.pos=pos
    def move(self):
        for i in self.a:
            self.v[0].x+=i.x
            self.v[0].y+=i.y
        for i in self.v:
            self.pos.x+=i.x
            self.pos.y+=i.y
screen=pygame.display.set_mode((800,600))
initPos=position(100,100)
'''a=thing(
    v=[vector(1,0)],
    a=[vector(-0.001,0.001)],
    pos=initPos
    )'''
a=thing(
    v=[vector(1,0)],
    a=[vector(0,0.001)],
    pos=initPos
    )
while True:
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((0,0,0))
    a.move()
    pygame.draw.circle(screen,(255,255,255),(int(a.pos.x)%800,int(a.pos.y)%600),20,0)
    pygame.display.flip()
    
