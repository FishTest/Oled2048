# coding=UTF-8
# 2048 pygame edition by FishX
# based on cam.py by Phil Burgess / Paint Your Dragon for Adafruit Industries.
# BSD license, all text above must be included in any redistribution.

import os
import random
import fnmatch
import pygame
from   pygame.locals import *

# UI classes ---------------------------------------------------------------
# Icon is a very simple bitmap class, just associates a name and a pygame
# image (PNG loaded from icons directory) for each.
# There isn't a globally-declared fixed list of Icons.  Instead, the list
# is populated at runtime from the contents of the 'icons' directory.
class Icon:
	def __init__(self, name):
	  self.name = name
	  try:
	    self.bitmap = pygame.image.load(iconPath + '/' + name + '.png')
	  except:
	    pass

# Button is a simple tappable screen region.  Each has:
#  - bounding rect ((X,Y,W,H) in pixels)
#  - optional background color and/or Icon (or None), always centered
#  - optional foreground Icon, always centered
#  - optional single callback function
#  - optional single value passed to callback
# Occasionally Buttons are used as a convenience for positioning Icons
# but the taps are ignored.  Stacking order is important; when Buttons
# overlap, lowest/first Button in list takes precedence when processing
# input, and highest/last Button is drawn atop prior Button(s).  This is
# used, for example, to center an Icon by creating a passive Button the
# width of the full screen, but with other buttons left or right that
# may take input precedence (e.g. the Effect labels & buttons).
# After Icons are loaded at runtime, a pass is made through the global
# buttons[] list to assign the Icon objects (from names) to each Button.

class Button:
	def __init__(self, rect, **kwargs):
	  self.rect     = rect # Bounds
	  self.color    = None # Background fill color, if any
	  self.iconBg   = None # Background Icon (atop color fill)
	  self.iconFg   = None # Foreground Icon (atop background)
	  self.bg       = None # Background Icon name
	  self.fg       = None # Foreground Icon name
	  self.callback = None # Callback function
	  self.value    = None # Value passed to callback
	  for key, value in kwargs.iteritems():
	    if   key == 'color': self.color    = value
	    elif key == 'bg'   : self.bg       = value
	    elif key == 'fg'   : self.fg       = value
	    elif key == 'cb'   : self.callback = value
	    elif key == 'value': self.value    = value
	def selected(self, pos):
	  x1 = self.rect[0]
	  y1 = self.rect[1]
	  x2 = x1 + self.rect[2] - 1
	  y2 = y1 + self.rect[3] - 1
	  if ((pos[0] >= x1) and (pos[0] <= x2) and
	      (pos[1] >= y1) and (pos[1] <= y2)):
	    if self.callback:
	      if self.value is None: self.callback()
	      else:                  self.callback(self.value)
	    return True
	  return False
	def draw(self, screen):
	  if self.color:
	    screen.fill(self.color, self.rect)
	  if self.iconBg:
	    screen.blit(self.iconBg.bitmap,
	      (self.rect[0]+(self.rect[2]-self.iconBg.bitmap.get_width())/2,
	       self.rect[1]+(self.rect[3]-self.iconBg.bitmap.get_height())/2))
	  if self.iconFg:
	    screen.blit(self.iconFg.bitmap,
	      (self.rect[0]+(self.rect[2]-self.iconFg.bitmap.get_width())/2,
	       self.rect[1]+(self.rect[3]-self.iconFg.bitmap.get_height())/2))
	def setBg(self, name):
	  if name is None:
	    self.iconBg = None
	  else:
	    for i in icons:
	      if name == i.name:
	        self.iconBg = i
	        break

# Go to the specified screen
def goScreen(n):
	global screenMode
	screenMode = n

# Exit System
def exitSystem():
	raise SystemExit
# Get Random num 2 or 4
def getRandom2or4():
	randList=[2,4]
	return random.choice(randList)
# Check and generate empty Array
def checkEmptyArray():
	global myArray,emptyArray
	count = 0
	emptyArray = []
	for m in range(0,4):
		for n in range(0,4):
			if myArray[m][n] is 0:
				count = count + 1
				emptyArray.append([m,n])
	return count
# Fill empty Array with random nums
def fillEmptyArray(c):
	global emptyArray
	for k in range(0,c):
		emptyItem = random.choice(emptyArray)
		myArray[emptyItem[0]][emptyItem[1]] = getRandom2or4()
		emptyArray.remove([emptyItem[0],emptyItem[1]])
# Init Array
def initArray():
	global myArray,Score
	Score = 0
	for m in range(0,4):
		for n in range(0,4):
			myArray[m][n]=0
	checkEmptyArray()
	fillEmptyArray(2)
# Array Operation
def users_choice(user_input):
    global myArray,Score
    if user_input == "u":
        i=0
        for j in range(0,4):
            if myArray[i][j]!=0 or myArray[i+1][j]!=0 or myArray[i+2][j]!=0 or myArray[i+3][j]!=0:
                if myArray[i][j]==0:
                    while myArray[i][j]==0:
                        myArray[i][j]=myArray[i+1][j]
                        myArray[i+1][j]=myArray[i+2][j]
                        myArray[i+2][j] = myArray[i+3][j]
                        myArray[i+3][j]=0
                if myArray[i+1][j]==0 and (myArray[i+2][j]!=0 or myArray[i+3][j]!=0):
                    while myArray[i+1][j]==0:
                        myArray[i+1][j]=myArray[i+2][j]
                        myArray[i+2][j]=myArray[i+3][j]
                        myArray[i+3][j]=0
                if myArray[i+2][j]==0 and (myArray[i+3][j]!=0):
                    while myArray[i+2][j]==0:
                        myArray[i+2][j]=myArray[i+3][j]
                        myArray[i+3][j]=0
        i=0
        for j in range(0,4):
            if myArray[i][j]==myArray[i+1][j]:
                myArray[i][j]=myArray[i][j]+myArray[i+1][j]
                myArray[i+1][j]=myArray[i+2][j]
                myArray[i+2][j]=myArray[i+3][j]
                myArray[i+3][j]=0
            if myArray[i+1][j]==myArray[i+2][j]:
                myArray[i+1][j]=myArray[i+1][j]+myArray[i+2][j]
                myArray[i+2][j]=myArray[i+3][j]
                myArray[i+3][j]=0
            if myArray[i+2][j]==myArray[i+3][j]:
                myArray[i+2][j]=myArray[i+2][j]+myArray[i+3][j]
                myArray[i+3][j]=0
    elif user_input == "d":
        i=0
        for j in range(0,4):
            if myArray[i][j]!=0 or myArray[i+1][j]!=0 or myArray[i+2][j]!=0 or myArray[i+3][j]!=0:
                if myArray[i+3][j]==0:
                    while myArray[i+3][j]==0:
                        myArray[i+3][j]=myArray[i+2][j]
                        myArray[i+2][j]=myArray[i+1][j]
                        myArray[i+1][j]=myArray[i][j]
                        myArray[i][j]=0
                if myArray[i+2][j]==0 and (myArray[i+1][j]!=0 or myArray[i][j]!=0):
                    while myArray[i+2][j]==0:
                        myArray[i+2][j]=myArray[i+1][j]
                        myArray[i+1][j]=myArray[i][j]
                        myArray[i][j]=0

                if myArray[i+1][j]==0 and myArray[i][j]!=0:
                    while myArray[i+1][j]==0:
                        myArray[i+1][j]=myArray[i][j]
                        myArray[i][j]=0
        i=0
        for j in range(0,4):
            if myArray[i+3][j]==myArray[i+2][j]:
                myArray[i+3][j]=myArray[i+3][j] + myArray[i+2][j]
                myArray[i+2][j]=myArray[i+1][j]
                myArray[i+1][j]=myArray[i][j]
                myArray[i][j]=0
            if myArray[i+2][j]==myArray[i+1][j]:
                myArray[i+2][j]=myArray[i+2][j]+myArray[i+1][j]
                myArray[i+1][j]=myArray[i][j]
                myArray[i][j]=0
            if myArray[i+1][j]==myArray[i][j]:
                myArray[i+1][j]=myArray[i+1][j]+myArray[i][j]
                myArray[i][j]=0
    elif user_input == "l":
        j=0
        for i in range(0,4):
            if myArray[i][j]!=0 or myArray[i][j+1]!=0 or myArray[i][j+2]!=0 or myArray[i][j+3]!=0:
                if myArray[i][j]==0:
                    while myArray[i][j]==0:
                        myArray[i][j]=myArray[i][j+1]
                        myArray[i][j+1]=myArray[i][j+2]
                        myArray[i][j+2] = myArray[i][j+3]
                        myArray[i][j+3]=0
                if myArray[i][j+1]==0 and (myArray[i][j+2]!=0 or myArray[i][j+3]!=0):
                    while myArray[i][j+1]==0:
                        myArray[i][j+1]=myArray[i][j+2]
                        myArray[i][j+2]=myArray[i][j+3]
                        myArray[i][j+3]=0
                if myArray[i][j+2]==0 and (myArray[i][j+3]!=0):
                    while myArray[i][j+2]==0:
                        myArray[i][j+2]=myArray[i][j+3]
                        myArray[i][j+3]=0
        j=0
        for i in range(0,4):
            if myArray[i][j]==myArray[i][j+1]:
                myArray[i][j]=myArray[i][j]+myArray[i][j+1]
                myArray[i][j+1]=myArray[i][j+2]
                myArray[i][j+2]=myArray[i][j+3]
                myArray[i][j+3]=0
            if myArray[i][j+1]==myArray[i][j+2]:
                myArray[i][j+1]=myArray[i][j+1]+myArray[i][j+2]
                myArray[i][j+2]=myArray[i][j+3]
                myArray[i][j+3]=0
            if myArray[i][j+2]==myArray[i][j+3]:
                myArray[i][j+2]=myArray[i][j+2]+myArray[i][j+3]
                myArray[i][j+3]=0
    elif user_input == "r":
        j=0
        for i in range(0,4):
            if myArray[i][j]!=0 or myArray[i][j+1]!=0 or myArray[i][j+2]!=0 or myArray[i][j+3]!=0:
                if myArray[i][j+3]==0:
                    while myArray[i][j+3]==0:
                        myArray[i][j+3]=myArray[i][j+2]
                        myArray[i][j+2]=myArray[i][j+1]
                        myArray[i][j+1]=myArray[i][j]
                        myArray[i][j]=0
                if myArray[i][j+2]==0 and (myArray[i][j+1]!=0 or myArray[i][j]!=0):
                    while myArray[i][j+2]==0:
                        myArray[i][j+2]=myArray[i][j+1]
                        myArray[i][j+1]=myArray[i][j]
                        myArray[i][j]=0

                if myArray[i][j+1]==0 and myArray[i][j]!=0:
                    while myArray[i][j+1]==0:
                        myArray[i][j+1]=myArray[i][j]
                        myArray[i][j]=0
        j=0
        for i in range(0,4):
            if myArray[i][j+3]==myArray[i][j+2]:
                myArray[i][j+3]=myArray[i][j+3] + myArray[i][j+2]
                myArray[i][j+2]=myArray[i][j+1]
                myArray[i][j+1]=myArray[i][j]
                myArray[i][j]=0
            if myArray[i][j+2]==myArray[i][j+1]:
                myArray[i][j+2]=myArray[i][j+2]+myArray[i][j+1]
                myArray[i][j+1]=myArray[i][j]
                myArray[i][j]=0
            if myArray[i][j+1]==myArray[i][j]:
                myArray[i][j+1]=myArray[i][j+1]+myArray[i][j]
                myArray[i][j]=0

    emptyArrayCount = checkEmptyArray()
    Score = Score + 1
    if emptyArrayCount >= 2:
        fillEmptyArray(2)
    elif emptyArrayCount == 1:
        fillEmptyArray(1)

# Global Settings
screenMode      =  0      # Current screen mode; default = HOME
screenModePrior = -1      # Prior screen mode (for detecting changes)
iconPath        = 'icons' # Subdirectory containing UI bitmaps (PNG format)
icons           = []      # This list gets populated at startup
fontFile        = "/usr/share/fonts/opentype/SourceHanSansCN-Regular.otf"
myArray         = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
inducerlist     = [0,1,2,3]
emptyArray      = []
Score           = 0
lineSpace       = 60
charSpace       = 59
lineX           = 9
lineY           = 20

# buttons[] is a list of lists; each top-level list element corresponds
# to one screen mode (e.g. viewfinder, image playback, storage settings),
# and each element within those lists corresponds to one UI button.
# There's a little bit of repetition (e.g. prev/next buttons are
# declared for each settings screen, rather than a single reusable
# set); trying to reuse those few elements just made for an ugly
# tangle of code elsewhere.

buttons = [
  # Screen mode 0 is the Main GUI
  [Button((63,  0,114, 80), bg='btnupbig',   cb=users_choice,value='u'),
  Button((  0, 80,120, 80), bg='btnleftbig', cb=users_choice,value='l'),
  Button((120, 80,120, 80), bg='btnrightbig',cb=users_choice,value='r'),
  Button(( 63,160,114, 80), bg='btndown',    cb=users_choice,value='d'),
  Button((236,  0, 84, 48), bg='btnexit',    cb=exitSystem),
  Button((242, 63, 74, 28), bg='btnnew',     cb=initArray),
  Button((262,107, 35, 35), bg='btnup',      cb=users_choice,value='u'),
  Button((242,146, 35, 35), bg='btnleft',    cb=users_choice,value='l'),
  Button((281,146, 35, 35), bg='btnright',   cb=users_choice,value='r'),
  Button((262,185, 35, 35), bg='btndown',    cb=users_choice,value='d')]
  ]

print "Game 2048 v0.1"
print "initing..."
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')
os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')
print "init pygame and screen"
pygame.init()
pygame.mouse.set_visible(False)
modes    = pygame.display.list_modes(16)
screen   = pygame.display.set_mode(modes[0], FULLSCREEN, 16)
fontMain = pygame.font.Font(fontFile,20)
print "Loading Icons..."
# Load all icons at startup.
for file in os.listdir(iconPath):
  if fnmatch.fnmatch(file, '*.png'):
    icons.append(Icon(file.split('.')[0]))
# Assign Icons to Buttons, now that they're loaded
print"Assigning Buttons"
for s in buttons:        # For each screenful of buttons...
  for b in s:            #  For each button on screen...
    for i in icons:      #   For each icon...
      if b.bg == i.name: #    Compare names; match?
        b.iconBg = i     #     Assign Icon to Button
        b.bg     = None  #     Name no longer used; allow garbage collection
      if b.fg == i.name:
        b.iconFg = i
        b.fg     = None

print "loading background.."
imgworking = pygame.image.load("bg.png")
if imgworking is None or imgworking.get_height() < 240: # Letterbox, clear background
  screen.fill(0)
if imgworking:
  screen.blit(imgworking,((320 - imgworking.get_width() ) / 2, (240 - imgworking.get_height()) / 2))
pygame.display.update()

# Init Array
print "init array!"
initArray()
# Main loop ----------------------------------------------------------------
print "mainloop.."

while(True):
	# Process touchscreen input
	while True:
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONDOWN):
				pos = pygame.mouse.get_pos()
				for b in buttons[screenMode]:
					if b.selected(pos): break
		if screenMode >= 0 or screenMode != screenModePrior: break

	screen.blit(imgworking,((320 - imgworking.get_width() ) / 2, (240 - imgworking.get_height()) / 2))
	# Overlay buttons on display and update
	for i,b in enumerate(buttons[screenMode]):
		b.draw(screen)
	# Draw specified screen
	if screenMode == 0:
		# draw Numbers
		for m in range(0,4):
			for n in range(0,4):
				lable = fontMain.render(unicode(str(myArray[m][n])),1,(119,110,101))
				if myArray[m][n] is not 0:
					screen.blit(lable,(n*charSpace + lineX,m*lineSpace + lineY))
		# draw Score
		lable = fontMain.render(unicode(str(Score)),1,(119,110,101))
		screen.blit(lable,(245,67))
		# draw Arrow
		arrowArray = [u'↑',u'←',u'→',u'↓']
		gpsArray   = [(269,114),(249,153),(288,153),(269,192)]
		for k in range(0,4):
			lable = fontMain.render(arrowArray[k],1,(119,110,101))
			screen.blit(lable,gpsArray[k])
	pygame.display.update()
	screenModePrior = screenMode
print "Game Over!"