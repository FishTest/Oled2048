# coding=UTF-8
# 2048 Oled edition by FishX
# BSD license, all text above must be included in any redistribution.
# Buttons Config
#   [0]New Game  [1]Up       [2]Exit Game
#   [3]Left      [4]Down     [5]Right

import sys
import random
import fnmatch
import threading
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Image
import ImageDraw
import ImageFont
from   Raspi_MCP230xx import Raspi_MCP230XX
from   time import sleep

# Init control keys
def initMcp():
	global mcp
	mcp = Raspi_MCP230XX(address = 0x20, num_gpios = 8)
	for i in range(0,6):
		mcp.config(i,mcp.INPUT)
	mcp.config(6,mcp.OUTPUT)
	mcp.output(6,1)                         # LED OUTPUT Low (Off)
	
# Init the oled screen
def initOled():
	global oled,image,draw
	RST        = 25
	DC         = 24
	SPI_PORT   = 0
	SPI_DEVICE = 0
	oled = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, 
		SPI_DEVICE, max_speed_hz=8000000))
	oled.begin()
	oled.clear()
	oled.display()
	width = oled.width
	height = oled.height
	image = Image.new('1', (width, height))
	draw = ImageDraw.Draw(image)
# Unicode encoding
def u(s):
	return unicode(s,'utf-8')
	
# Exit System
def exitPrepare():
	global shouldExit
	shouldExit = True
	mcp.output(6,1)

# KeyChecking thread
def checkKeyPress():
	global shouldExit
	while True:
		if mcp.input(0) is 0:
			mcp.output(6,0)
			initArray()
		elif mcp.input(1) is 0:
			mcp.output(6,0)
			users_choice('u')
		elif mcp.input(2) is 0:
			mcp.output(6,0)
			exitPrepare()
		elif mcp.input(3) is 0:
			mcp.output(6,0)
			users_choice('l')
		elif mcp.input(4) is 0:
			mcp.output(6,0)
			users_choice('d')
		elif mcp.input(5) is 0:
			mcp.output(6,0)
			users_choice('r') 
		sleep(0.2)
		mcp.output(6,1)
		if shouldExit:
			break
		
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
    lock.acquire()
    try:
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
    finally:
        lock.release()

print "Game 2048 Oled Version 0.1"
print "initing..."

# Global Settings
fontFile        = "/usr/share/fonts/opentype/SourceHanSansCN-Regular.otf"
myArray         = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
inducerlist     = [0,1,2,3]
emptyArray      = []
Score           = 0
lock            = threading.Lock()
fontMain        = ImageFont.truetype('/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono.ttf', 10)
shouldExit      = False
rectWidth       = 32
rectHeight      = 16

# Init Array,MCP,Oled
print "init array!"
initArray()
print "init MCP!"
initMcp()
print "init Oled!"
initOled()

# Start KeyChecking thread
tKeyChecking = threading.Thread(target=checkKeyPress)
tKeyChecking.start()

# Main loop ----------------------------------------------------------------
print "mainloop.."

while(True):
	# clear screen
	draw.rectangle((0,0,127,63),outline=0,fill=0)
	# draw num's border
	for i in range(0,4):
		for j in range(0,4):
			draw.rectangle(( i * rectWidth + 1, j * rectHeight + 1, 
				(i + 1) * rectWidth - 1 , (j + 1) * rectHeight - 1) , 
				outline = 1,fill = 0)
	# draw numbers
	for m in range(0,4):
		for n in range(0,4):
			if myArray[m][n] is not 0:
				num = u(str(myArray[m][n]))
				w = draw.textsize(num,font = fontMain)[0]
				x = (32 * n + (30 - w) / 2 + 1)
				y = (16 * m + 3) 
				draw.text((x,y),num,font = fontMain ,fill = 255)
	oled.image(image)
	oled.display()
	if shouldExit is True:
		draw.rectangle((0,0,127,63),outline=0,fill=0)
		oled.image(image)
		oled.display()
		break

