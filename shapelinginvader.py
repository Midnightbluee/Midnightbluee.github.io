from Tkinter import *
import random
import copy

def shapeKeyPressed(canvas,event):
    if(event.keysym == 'r'):
        shapeInit(canvas)

def shapeMousePressed(canvas,event):
    targetX,targetY=event.x,event.y
    for i in xrange(len(canvas.data.shapeProtect)):
        canvas.data.candidate.append([((1+i)*(canvas.data.cWidth/6),\
            canvas.data.init+canvas.data.sHeight/2),\
            canvas.data.shapeProtect[i],i])
    for i in xrange(len(canvas.data.shapelings)):
        if shapeDist((targetX,targetY),canvas.data.candidate[i][0])<canvas.data.sWidth:
            if canvas.data.candidate[i] in canvas.data.choose:
                canvas.data.choose.pop()
            else:
                canvas.data.choose.append(canvas.data.candidate[i])
            if len(canvas.data.choose)==2:
                canvas.data.shapeProtect[canvas.data.choose[0][2]]=canvas.data.choose[1][1]
                canvas.data.shapeProtect[canvas.data.choose[1][2]]=canvas.data.choose[0][1]
                canvas.data.choose=[]
    canvas.data.candidate=[]
    
def shapeDist((x1, y1), (x2, y2)):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def shapeInvader(canvas):
    temp=copy.deepcopy(canvas.data.shapelings)
    random.shuffle(temp)
    canvas.data.invader = copy.deepcopy(temp)
    canvas.data.speed=1+1*canvas.data.score
    if canvas.data.win==False:shapeDrawAll(canvas,canvas.data.invader,0)
    
def shapeInvaderAdvance(canvas):
    canvas.data.invaderInit+=canvas.data.speed
    shapeDrawAll(canvas,canvas.data.invader,canvas.data.invaderInit)

def shapeProtect(canvas):
    temp=copy.deepcopy(canvas.data.shapelings)
    random.shuffle(temp)
    canvas.data.shapeProtect = copy.deepcopy(temp)
    canvas.data.init=canvas.data.cHeight-canvas.data.sHeight

def shapeRemove(canvas):
    if canvas.data.invaderInit>=canvas.data.init-canvas.data.sHeight:
        canvas.data.invaderInit=-60
        canvas.data.score-=1
        if canvas.data.score<0:canvas.data.lose=True
        else:canvas.data.stars[canvas.data.score]=False
        shapeInvader(canvas)
    if canvas.data.shapeProtect==canvas.data.invader:
        canvas.data.invaderInit=-60
        canvas.data.stars[canvas.data.score]=True
        canvas.data.score+=1
        if canvas.data.score==len(canvas.data.stars):canvas.data.win=True
        shapeInvader(canvas)
    
def shapeLose(canvas):
    canvas.create_text(canvas.data.cWidth / 2, canvas.data.cHeight / 2, \
                       text = 'Game Over!',font=("Comic Sans MS", 50, "bold"))
    canvas.create_text(canvas.data.cWidth / 2, canvas.data.cHeight / 2+50, \
                       text = 'Press r to Restart',font=("Comic Sans MS", 30, "bold"))

def shapeWin(canvas):
    canvas.create_text(canvas.data.cWidth / 2, canvas.data.cHeight / 2, \
                       text = 'You Win!',font=("Comic Sans MS", 50, "bold"))
    canvas.create_text(canvas.data.cWidth / 2, canvas.data.cHeight / 2+50, \
                       text = 'How to You Make That!',\
                       font=("Comic Sans MS", 30, "bold"))
    canvas.create_text(canvas.data.cWidth / 2, canvas.data.cHeight / 2+90, \
                       text = 'Press r to Restart',\
                       font=("Comic Sans MS", 20, "bold"))

def shapeTimerFired(canvas):
    if canvas.data.lose==False and canvas.data.win==False:
        canvas.delete(ALL)
        canvas.create_rectangle(0,0,canvas.data.cWidth, canvas.data.cHeight,\
                                fill=canvas.data.background)
        shapeRemove(canvas)
        if canvas.data.lose==False:
            shapeDrawAll(canvas,canvas.data.shapeProtect,canvas.data.init)
        shapeInvaderAdvance(canvas)
    delay = 10
    canvas.after(delay, lambda: shapeTimerFired(canvas))

def shapeDrawAll(canvas,lists,advance):
    canvas.data.starX,canvas.data.starY=0,20
    for i in xrange(len(canvas.data.shapelings)):
        canvas.data.starX+=50
        if canvas.data.stars[i]==False:filling=canvas.data.background
        else:filling="yellow"
        shapeDrawStars(canvas,filling)
    for i in xrange(len(canvas.data.shapelings)):
        canvas.data.center=(1+i)*(canvas.data.cWidth/6)
        shapeDrawShape(canvas,lists[i],advance)
    if canvas.data.lose:shapeLose(canvas)
    elif canvas.data.win:shapeWin(canvas)
    
def shapeDrawStars(canvas,filling):
    starX,starY,starR=canvas.data.starX,canvas.data.starY,20
    starSmallR=0.38*starR
    canvas.create_polygon(starX,starY+starR,\
                          starX+0.22452*starR,starY+0.30902*starR,\
                          starX+0.95106*starR,starY+0.30902*starR,\
                          starX+0.36328*starR,starY-0.11804*starR,\
                          starX+0.58779*starR,starY-0.80902*starR,\
                          starX,starY-0.38197*starR,\
                          starX-0.58779*starR,starY-0.80902*starR,\
                          starX-0.36328*starR,starY-0.11804*starR,\
                          starX-0.95106*starR,starY+0.30902*starR,\
                          starX-0.22452*starR,starY+0.30902*starR,\
                          fill=filling,width=1,outline="yellow")
        
def shapeDrawShape(canvas,shape,advance):
    center=canvas.data.center
    if len(canvas.data.choose)==0: outlineWidth=1
    elif shape==canvas.data.choose[0][1] and canvas.data.init==advance:
        outlineWidth=5
    else:outlineWidth=1
    if shape=="circle":
        canvas.create_oval(center-canvas.data.sWidth/2,\
                           canvas.data.sHeight+advance,\
                           center+canvas.data.sWidth/2,\
                           advance,fill="red",width=outlineWidth)
    elif shape=="rectangle":
        canvas.create_rectangle(center-canvas.data.sWidth/2,\
                                canvas.data.sHeight+advance,\
                                center+canvas.data.sWidth/2,\
                                advance,fill="green",width=outlineWidth)
    elif shape=="triangle":
        canvas.create_polygon(center-canvas.data.sWidth/2,\
                              canvas.data.sHeight+advance,\
                              center+canvas.data.sWidth/2,\
                              canvas.data.sHeight+advance,\
                              center,+advance,fill="pink",\
                              width=outlineWidth,outline="black")
    elif shape=="hexagon":
        side=canvas.data.sWidth/2
        canvas.create_polygon(center-side/2,canvas.data.sHeight+advance,\
                              center+side/2,canvas.data.sHeight+advance,\
                              center+side,canvas.data.sHeight/2+advance,\
                              center+side/2,+advance,\
                              center-side/2,+advance,\
                              center-side,canvas.data.sHeight/2+advance,\
                              fill="cyan",width=outlineWidth,outline="black")
    else:
        canvas.create_polygon(center-canvas.data.sWidth/4,\
                              canvas.data.sHeight+advance,\
                              center+canvas.data.sWidth/4,\
                              canvas.data.sHeight+advance,\
                              center+canvas.data.sWidth/2,\
                              canvas.data.sHeight/2+advance,\
                              center,0+advance,\
                              center-canvas.data.sWidth/2,\
                              canvas.data.sHeight/2+advance,\
                              fill="purple",width=outlineWidth,outline="black")
    
      
def shapeInit(canvas):
    canvas.data.background="midnightblue"
    canvas.data.stars=[False,False,False,False,False]
    canvas.data.score=0
    canvas.data.speed=1
    canvas.data.invaderInit=-60
    canvas.data.candidate=[]
    canvas.data.choose=[]
    canvas.data.isSelect=False
    canvas.data.lose,canvas.data.win=False,False
        
def shapeRun():
    root = Tk()
    cWidth=600
    cHeight=600
    class Struct:pass
    canvas = Canvas(root, width=cWidth, height=cHeight)
    canvas.pack()
    canvas.data = Struct()
    canvas.data.cWidth, canvas.data.cHeight = cWidth, cHeight
    canvas.data.sWidth, canvas.data.sHeight = 50, 50
    canvas.data.shapelings=["circle","triangle","rectangle",\
                            "hexagon","pentagon"]
    shapeInit(canvas)
    shapeInvader(canvas)
    shapeProtect(canvas)
    root.bind("<Button-1>", lambda event: shapeMousePressed(canvas, event))
    root.bind("<Key>", lambda event: shapeKeyPressed(canvas, event))
    shapeTimerFired(canvas)
    root.mainloop()
shapeRun()
