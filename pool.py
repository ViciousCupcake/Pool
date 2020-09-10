from vpython import *
#from visual import *
import random
import math
import time

scene.width = 1000
scene.height= 600
scene.title = "Billiards- Jonathan Xu"
scene.userzoom = False
scene.userspin = True


#Exception class to escape nested loops
class ContinueI(Exception):
    pass

#Wrapper class for balls
class mySphere:
    
    def __init__(self, position, color, striped):
        """if striped == False:
            self.sph = sphere(pos= position, radius = ballRad, color = color) 
        else:
            self.sphere = sphere(pos= position, radius = ballRad, color = color) 
            self.hat = sphere(pos = position+ vector(0,0,ballRad),radius = 0.03, color = vector(1,1,1))
            self.sph = compound([self.sphere,self.hat])"""

        self.sph = sphere(pos= position, radius = ballRad, color = color)
        #self.hat = ring(pos = position+ vector(0,0,ballRad),axis = vector(0,0,1),radius = ballRad, color = vector(1,1,1))
        self.hat = ring(pos = position,axis = vector(0,0,1),radius = 0.08625,thickness = 0.03, color = vector(1,1,1))
        self.hat.visible = striped
        #self.vel = vector(random.uniform(-2,2),random.uniform(-2,2),0)
        self.vel = vector(0,0,0)
        self.mass = 1
        self.striped = striped
        if self.striped is None:
            self.vel = vector(0,0,0)
        """if striped:
            self.sph.radius = 0.08"""
    """def __init__(self):
        self.sph = sphere(pos= vector(random.uniform(-4.5+ballRad,4.5-ballRad),random.uniform(-2.25+ballRad,2.25-ballRad),ballRad), radius = ballRad, color = color.red) 
        self.vel = vector(random.uniform(-2,2),random.uniform(-2,2),0)
        self.mass = 1"""


class cueStick:

    def __init__(self):
        self.rod = cylinder(pos = vector(0,0,ballRad), axis = vector(0,0,0),radius = 0.020833, color = vector(139,69,19)/255)
        self.rod.visible = False
        self.theta = 0
        self.length = 0.1
        self.maxLength = 2


class boolWrapper:
    def __init__(self):
        self.bool = False


#Helper function; called when key is pressed
def keyDown(evt):
    if not evt.key in pressed:
        pressed.append(evt.key)

#Helper function; called when key is released
def keyUp(evt):
    if evt.key in pressed:
        pressed.remove(evt.key)

#Helper function; called when mouse is pressed
def down():
    mouseDown.bool = True

#Helper function; called when mouse is released
def up():
    mouseDown.bool = False

#Returns Pythagorean Length of diagonal
def absolute(xa):
    return math.sqrt((xa.x)**2+(xa.y)**2+(xa.z)**2)

#True if you hit your own ball into hole
def isHit(dellst, Player1Striped, Player1Turn):
    if Player1Turn:
        for sphere in dellst:
            #print(sphere.striped)
            if sphere.striped == (Player1Striped):
                return True
    else:
        for sphere in dellst:
            if sphere.striped == (not Player1Striped):
                return True
    return False


#Bind user input to methods above
scene.bind('keydown', keyDown)
scene.bind('keyup', keyUp)
scene.bind("mousedown", down)
scene.bind("mouseup", up)

#Initalize Variables
ballRad = 0.09375
mouseDown = boolWrapper()
continue_i = ContinueI()
myStick = cueStick()
playerIndicator = box(pos = vector(5,2,0),axis =  vector(0,0,1), size = vector(0.2,0.2,0.2),color = vector(247, 35, 240)/255)
player1TurnMessage = text(pos=vector(0,0,0),text='Player One\'s Turn', align='center', color=color.green, height = 0.8)
player2TurnMessage = text(pos=vector(0,0,0),text='Player Two\'s Turn', align='center', color=color.green, height = 0.8)
playerStripe = box(pos = vector(5,2,0),axis = vector(0,0,1), size = vector(0.25,.05,0.25), color = vector(1,1,1))

cirRad = ballRad*2
dt = float(1)/300
b = 0.6
yPos = -2.25 + ballRad/2
counter = 0
Player1Striped = None
recentUpdate = None
dellst = []
pressed = []
Player1Turn = False
legalMouseMove = True
blackBallHit = False
stopped = False
cueBallInHole = False
player1TurnMessage.visible = False
player2TurnMessage.visible = False
hit = False
canReset = False
firstStoppedFrame = False

#Initialize billiard table+walls
mybox = box(pos=vector(0,0,0), size=vector(9,4.5,0),shininess=0, color=vector(63,149,35)/255, texture=textures.rough)
topWall = box(pos=vector(0,2.35,0.1),size=vector(9,0.2,0.2),shininess=0.2, color = color.orange, texture=textures.wood)
bottomWall = box(pos=vector(0,-2.35,0.1),size=vector(9,0.2,0.2),shininess=0.2, color = color.orange, texture=textures.wood)
rightWall = box(pos=vector(4.6,0,0.1),size=vector(0.2,4.9,0.2),shininess=0.2, color = color.orange, texture=textures.wood)
rightWall = box(pos=vector(-4.6,0,0.1),size=vector(0.2,4.9,0.2),shininess=0.2, color = color.orange, texture=textures.wood)
"""mybox = box(pos=vector(0,0,0), size=vector(9,4.5,0),shininess=0, color=vector(63,149,35)/255, material=materials.rough)
topWall = box(pos=vector(0,2.35,0.1),size=vector(9,0.2,0.2),shininess=0.2, color = color.orange, material=materials.wood)
bottomWall = box(pos=vector(0,-2.35,0.1),size=vector(9,0.2,0.2),shininess=0.2, color = color.orange, material=materials.wood)
rightWall = box(pos=vector(4.6,0,0.1),size=vector(0.2,4.9,0.2),shininess=0.2, color = color.orange, material=materials.wood)
rightWall = box(pos=vector(-4.6,0,0.1),size=vector(0.2,4.9,0.2),shininess=0.2, color = color.orange, material=materials.wood)"""

#Initalize billiard table holes
holeBL = cylinder(pos = vector(-4.5,-2.25,0),axis=vector(0,0,0.01),radius=cirRad,color  = color.black)
holeBM = cylinder(pos = vector(0,-2.25,0),axis=vector(0,0,0.01),radius=cirRad,color  = color.black)
holeBR = cylinder(pos = vector(+4.5,-2.25,0),axis=vector(0,0,0.01),radius=cirRad,color  = color.black)
holeTL = cylinder(pos = vector(-4.5,2.25,0),axis=vector(0,0,0.01),radius=cirRad,color  = color.black)
holeTM = cylinder(pos = vector(0,2.25,0),axis=vector(0,0,0.01),radius=cirRad,color  = color.black)
holeTR = cylinder(pos = vector(+4.5,2.25,0),axis=vector(0,0,0.01),radius=cirRad,color  = color.black)

holeLst = (holeBL,holeBM,holeBR,holeTL,holeTM,holeTR)

#Initalize each ball on table
cue =mySphere(vector(0,2.25,ballRad),color = color.white, striped = False) 
black =mySphere(vector(-2.5747595264191645,0,ballRad),color=vector(0,0,0)/255,striped=False)
lst = [mySphere(vector(-2.25,0.0,ballRad),color=vector(242,255,0)/255,striped=False),
mySphere(vector(-2.4123797632095823,ballRad,ballRad),color=vector(38,47,224)/255,striped=False),
mySphere(vector(-2.4123797632095823,-ballRad,ballRad),color=vector(109,18,32)/255,striped=True),
mySphere(vector(-2.5747595264191645,0.1875,ballRad),color=vector(9,53,9)/255,striped=True),
mySphere(vector(-2.5747595264191645,-0.1875,ballRad),color=vector(255,157,0)/255,striped=False),
mySphere(vector(-2.7371392896287468,0.28125,ballRad),color=vector(96,0,198)/255,striped=False),
mySphere(vector(-2.7371392896287468,ballRad,ballRad),color=vector(26,32,147)/255,striped=True),
mySphere(vector(-2.7371392896287468,-ballRad,ballRad),color=vector(193,1,193)/255,striped=False),
mySphere(vector(-2.7371392896287468,-0.28125,ballRad),color=vector(157,165,0)/255,striped=True),
mySphere(vector(-2.899519052838329,0.375,ballRad),color=vector(165,102,0)/255,striped=True),
mySphere(vector(-2.899519052838329,0.1875,ballRad),color=vector(224,38,66)/255,striped=False),
mySphere(vector(-2.899519052838329,0.0,ballRad),color=vector(137,0,137)/255,striped=True),
mySphere(vector(-2.899519052838329,-0.1875,ballRad),color=vector(44,0,91)/255,striped=True),
mySphere(vector(-2.899519052838329,-0.375,ballRad),color=vector(19,109,18)/255,striped=False),
cue,black]

#Game loop
while len(lst)!=0:
    rate(1/dt)
    scene.autoscale = False
    stopped = True
    
    #Delete messages after ~3 seconds
    if(counter < 1/dt):
        counter+=1
    else:
        player1TurnMessage.visible = False
        player2TurnMessage.visible = False
        try:
            stripedDisplay.visible = False
        except:
            pass
        counter = 0

    for meSph in lst:
        #Update Location
        meSph.sph.pos += meSph.vel*dt

        #Bounce off Walls, and when balls collide, make the balls lose some energy
        if meSph.sph.pos.y+meSph.sph.radius > 2.25 or meSph.sph.pos.y-meSph.sph.radius < -2.25:
            meSph.vel.y = -meSph.vel.y*0.9
        if meSph.sph.pos.x+meSph.sph.radius > 4.5 or meSph.sph.pos.x-meSph.sph.radius < -4.5:
            meSph.vel.x = -meSph.vel.x*0.9

        #Friction
        if mag(meSph.vel)>0:
            meSph.vel-=norm(meSph.vel)*(0.025/(mag(meSph.vel)+5))
        meSph.hat.pos = meSph.sph.pos

        #If almost stopped, then is stopped, also check to see if all balls are stopped (i.e. end of one round)
        if mag(meSph.vel)<0.01:
            meSph.vel = vector(0,0,0)
        else:
            stopped = False

        #Check to see if ball fell in hole
        try:
            for hole in holeLst:
                if absolute(meSph.sph.pos-hole.pos)<(hole.radius*1.5):
                    
                    #If player has not been assigned stripes or solids, then assign it
                    if Player1Striped is None and recentUpdate is None and not meSph is cue:
                        Player1Striped = meSph.striped
                        recentUpdate = True

                    #Don't move cue ball outside table
                    if meSph is cue:
                        cueBallInHole = True
                        cue.sph.pos = vector(2.25,0,ballRad)
                        cue.vel = vector(0,0,0)

                    #Make a note that the 8-ball is hit, for future calculations
                    elif meSph is black:
                        blackBallHit = True

                    #Move ball in hole outside of table, and remove from list of active balls
                    else:
                        meSph.sph.pos = vector(5,yPos,0)
                        meSph.hat.pos = meSph.sph.pos
                        dellst.append(meSph)
                        lst.remove(meSph)
                        yPos+=0.2
                    meSph.vel=vector(0,0,0)
                    
                    #Escape inner loop to save cpu cycles
                    raise continue_i
        except ContinueI:
            continue
        
        #Calculate collisions
        for otherSph in lst:
            if not (otherSph is meSph):
                if absolute(meSph.sph.pos-otherSph.sph.pos) < 2*meSph.sph.radius-0.03:
                    #Algorithm from-
                    #https://ericleong.me/research/circle-circle/#static-circle-collision
                    """if Player1Turn:
                        if meSph is cue and otherSph.striped == Player1Striped:
                            gotGoodHole = True
                            for sphere in lst:
                                if otherSph is sphere:
                                    gotGoodHole = False
                            hit = gotGoodHole
                    else:
                        if meSph is cue and otherSph.striped == (not Player1Striped):
                            gotGoodHole = True
                            for sphere in lst:
                                if otherSph is sphere:
                                    gotGoodHole = False
                            hit = gotGoodHole"""
                    d = math.sqrt((meSph.sph.pos.x-otherSph.sph.pos.x)**2+(meSph.sph.pos.y-otherSph.sph.pos.y)**2)
                    nx = (otherSph.sph.pos.x-meSph.sph.pos.x)/d
                    ny = (otherSph.sph.pos.y-meSph.sph.pos.y)/d
                    p = 2*(meSph.vel.x*nx+meSph.vel.y*ny - otherSph.vel.x*nx - otherSph.vel.y*ny)/(meSph.mass+otherSph.mass)

                    #Move balls back by 1 frame to prevent balls from clipping in each other
                    meSph.sph.pos+=-1*meSph.vel*dt
                    otherSph.sph.pos+=-1*otherSph.vel*dt

                    #Assign new velocities to balls
                    meSph.vel.x,meSph.vel.y,otherSph.vel.x,otherSph.vel.y=meSph.vel.x-p*meSph.mass*nx,meSph.vel.y-p*meSph.mass*ny,otherSph.vel.x+p*otherSph.mass*nx,otherSph.vel.y+p*otherSph.mass*ny

                    #When balls collide, make the balls lose some energy
                    meSph.vel *=0.9
                    otherSph.vel *=0.9
    
    #Cue stick controls (user input)
    if(cue.vel == vector(0,0,0) and stopped):
        if 'a' in pressed:
            myStick.theta+=0.5
        elif 'd' in pressed:
            myStick.theta -=0.5
        elif 'w' in pressed and myStick.length < 1:
            myStick.length +=0.01
        elif 's' in pressed and myStick.length > 0.1:
            myStick.length -= 0.01
        elif ' ' in pressed:
            cue.vel = myStick.rod.axis*-3
            legalMouseMove = False
            firstStoppedFrame = True
            stopped = False
        elif 'A' in pressed:
            myStick.theta +=0.1
        elif 'D' in pressed:
            myStick.theta -=0.1
        myStick.rod.pos = cue.sph.pos
        myStick.rod.axis = vector(myStick.maxLength*myStick.length*math.cos(math.radians(myStick.theta)),myStick.maxLength*myStick.length*math.sin(math.radians(myStick.theta)),0)
        myStick.rod.visible = True
    #Make rod invisible if not in use   
    else:
        myStick.rod.visible = False

    #Runs when no balls are moving (i.e. round has ended)
    if stopped:

        #Calculations for if the black ball is hit
        #If all of a person's balls are eliminated, and also the black ball, then announce that they win, otherwise announce that they lose
        if blackBallHit:
            temp = True
            if not Player1Striped:
                for sphere in lst:
                    temp = temp and sphere.striped
                if temp:
                    text(pos=vector(0,0,0),text='Player 1 Wins!' if Player1Turn else 'Player 2 Wins!', align='center', color=color.green, height = 0.8)
                else:
                    text(pos=vector(0,0,0),text='Player 1 Loses!' if Player1Turn else 'Player 2 Loses!', align='center', color=color.red, height = 0.8)
            else:
                temp = False
                for sphere in lst:
                    temp = temp or sphere.striped
                if not temp:
                    text(pos=vector(0,0,0),text='Player 1 Wins!' if Player1Turn else 'Player 2 Wins!', align='center', color=color.green, height = 0.8)
                else:
                    text(pos=vector(0,0,0),text='Player 1 Loses!' if Player1Turn else 'Player 2 Loses!', align='center', color=color.red, height = 0.8)
            
            text(pos=vector(0,-1.2,0),text='Game Over!', align='center', color=color.red)

            #Clear temporary list of balls
            del lst[:]

            #End program
            continue

        #Switch turns if player hits the cue ball in the hole
        if cueBallInHole:
            Player1Turn = not Player1Turn
            if Player1Turn:
                playerIndicator.color = vector(247, 35, 240)/255
                player1TurnMessage.visible = True
                if Player1Striped:
                    playerStripe.visible = True
                else:
                    playerStripe.visible = False
                counter = 0
            else:
                playerIndicator.color = vector(37, 250, 225)/255
                player2TurnMessage.visible = True
                if Player1Striped:
                    playerStripe.visible = False
                else:
                    playerStripe.visible = True
                counter = 0
            cueBallInHole = not cueBallInHole
            legalMouseMove = True

        #Switch turns if player doesn't hit their own ball into a hole
        elif not isHit(dellst, Player1Striped, Player1Turn) and firstStoppedFrame:
            Player1Turn = not Player1Turn
            if Player1Turn:
                playerIndicator.color = vector(247, 35, 240)/255
                player1TurnMessage.visible = True
                counter = 0
                if Player1Striped:
                    playerStripe.visible = True
                else:
                    playerStripe.visible = False
            else:
                playerIndicator.color = vector(37, 250, 225)/255
                player2TurnMessage.visible = True
                counter = 0
                if Player1Striped:
                    playerStripe.visible = False
                else:
                    playerStripe.visible = True
            legalMouseMove = True
            hit = False

        #Delete contents of temporary list only once after each round
        elif firstStoppedFrame:
            del dellst[:]

        #Announce what each player should aim for
        if recentUpdate:
            stripedDisplay = text(pos=vector(0,-1,1),text='You are Stripes!' if Player1Striped else 'You are Solids!', align='center', color=color.green, height = 0.8)
            recentUpdate = False
            counter = 0

        #Allow to move the cue ball with the mouse only if the other player fouled
        if mouseDown.bool == True and legalMouseMove:
            cue.sph.pos = scene.mouse.pos
            if scene.mouse.pos.x<-4.5+ballRad:
                cue.sph.pos.x = -4.5+ballRad
            elif scene.mouse.pos.x>4.5-ballRad:
                cue.sph.pos.x = 4.5-ballRad
            if scene.mouse.pos.y<-2.25+ballRad:
                cue.sph.pos.y = -2.25+ballRad
            elif scene.mouse.pos.y>2.25-ballRad:
                cue.sph.pos.y = 2.25-ballRad
        
        firstStoppedFrame = False


#pink player1
#if hit same color other player can mouse control location
#text(pos=vector(0,0,0),text='You Win!', align='center', color=color.green)
