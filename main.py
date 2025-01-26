# Pip the Mouse
# Created for Hackapet
# Made by j4y_boi

import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
from random import randint
from random import seed
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap
import json
import os

Delius10 = bitmap_font.load_font("fonts/Delius-10.bdf", Bitmap)
Delius8 = bitmap_font.load_font("fonts/Delius-8.bdf", Bitmap)

for x in range(randint(0,10)): #This might look dangerous and all, but this is just to make RNG a bit better
    seed(randint(0,9999999+x))

pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
UIlayer = displayio.Group()
mainlayer = displayio.Group()

# Config (sorry for the essay, better too much documentation than too little am i right)
# It's generally recommended to NOT go under the default values, could lead to some weird glitches...

debug = False #should be off if you're planning on writing it, quite resource intensive (just prints extra data)
TargetFPS = 15 # default = 15 (does change the animation speeds, nope FIXED NOW WHOOOOOO)
autosaveInterval = 30 #seconds for autosave
resetTime = 15 #how long to hold all three buttons to reset button

cheezesspawnlimit = 10 #for performance and also so it doesnt explod (default = 10)
feedingCooldown = 1 #cooldown inbetween giving food (in seconds, default 1)
nutritionalValue = 20 #uhhh yeah (default 20)

notFedTime = 20 #amount of time of unfed before death (in seconds, default 20)
tooFedTime = 50 #amount of food before death (in amounts of food, default 50)
startHunger = 30 #how much time before mous starts to get hungy (in seconds, default 30)

exerciseNeed = 60 #mouse needs to move atleast once every this much seconds (in seconds, default 60)
tooExercise = 30 #amount of play before death (in amount of playing with the ball, default 30)
startFitness = 60 #how much time before pip needs to start MOVIN (in seconds, default 60)

# End Config :P


cheese = displayio.OnDiskBitmap("assets/cheese.bmp")
apple = displayio.OnDiskBitmap("assets/apple_slice.bmp")
peanut = displayio.OnDiskBitmap("assets/peanut.bmp")
grapes = displayio.OnDiskBitmap("assets/grapes.bmp")
foods = [cheese,grapes,peanut,apple]

ball = displayio.OnDiskBitmap("assets/ball.bmp")
heart = displayio.OnDiskBitmap("assets/heart.bmp")

# Background Spritesheet #
backgroundID = randint(1,3)
background_sheet = displayio.OnDiskBitmap(f"assets/room{backgroundID}.bmp")
background_sprite = displayio.TileGrid(
    background_sheet,
    pixel_shader=background_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=(display.width - 128) // 2,  
    y=display.height - 128 - 0
)
splash.append(background_sprite)

angry_eyebrows_file = displayio.OnDiskBitmap("assets/angry_mouse.bmp")
angry_eyebrows_sprite = displayio.TileGrid(
    angry_eyebrows_file,
    pixel_shader=angry_eyebrows_file.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=(display.width - 32) // 2,  
    y=display.height - 32 - 0
)
splash.append(angry_eyebrows_sprite)

# Mouse Spritesheet #
mouse_sheet = displayio.OnDiskBitmap("assets/idle_mouse.bmp")
mouse_sprite = displayio.TileGrid(
    mouse_sheet,
    pixel_shader=mouse_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=(display.width - 32) // 2,  
    y=display.height - 32 - 10     
)
splash.append(mouse_sprite)

# alt+f4 from life Mouse Spritesheet #
died_mouse_sheet = displayio.OnDiskBitmap("assets/died_mouse.bmp")
died_mouse_sprite = displayio.TileGrid(
    died_mouse_sheet,
    pixel_shader=died_mouse_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=(display.width - 32) // 2,  
    y=display.height - 32 - 10     
)
splash.append(died_mouse_sprite)

# itch Mouse Spritesheet #
itch_mouse_sheet = displayio.OnDiskBitmap("assets/itch_mouse.bmp")
itch_mouse_sprite = displayio.TileGrid(
    itch_mouse_sheet,
    pixel_shader=itch_mouse_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=0,  
    y=display.height - 32 - 10     
)
splash.append(itch_mouse_sprite)

# walk Mouse Spritesheet #
walk_mouse_sheet = displayio.OnDiskBitmap("assets/walk2_mouse.bmp")
walk_mouse_sprite = displayio.TileGrid(
    walk_mouse_sheet,
    pixel_shader=walk_mouse_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=0,  
    y=display.height - 32 - 10     
)
splash.append(walk_mouse_sprite)

# Sleeping Mouse Spritesheet #
sleep_mouse_sheet = displayio.OnDiskBitmap("assets/sleep_mouse.bmp")
sleep_mouse_sprite = displayio.TileGrid(
    sleep_mouse_sheet,
    pixel_shader=sleep_mouse_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=0,  
    y=display.height - 32 - 10     
)
splash.append(sleep_mouse_sprite)

# playing mouse spritesheet #
play_mouse_sheet = displayio.OnDiskBitmap("assets/play_mouse.bmp")
play_mouse_sprite = displayio.TileGrid(
    play_mouse_sheet,
    pixel_shader=play_mouse_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=64,
    tile_height=64,
    default_tile=0,
    x=mouse_sprite.x + 16,  
    y=mouse_sprite.y + 30
)
splash.append(play_mouse_sprite)

foodz = []
def giveFood():
    chosen = foods[randint(0,len(foods)-1)]

    foodSprite = displayio.TileGrid(
        chosen,
        pixel_shader=chosen.pixel_shader,
        width=1,
        height=1,
        tile_width=chosen.width,
        tile_height=chosen.height,
        y=randint(67,90),
        x=randint(0,95)
    )
    splash.append(foodSprite)
    foodz.append(foodSprite)

    if len(foodz) > cheezesspawnlimit:
        splash.remove(foodSprite)
        foodz.remove(foodSprite)

throwntoys = []
def throwBall():
    ball_sprite = displayio.TileGrid(
        ball,
        pixel_shader=ball.pixel_shader,
        width=1,
        height=1,
        tile_width=32,
        tile_height=32,
        default_tile=0,
        y=randint(67,90),
        x=randint(0,95),
    )
    splash.append(ball_sprite)
    throwntoys.append(ball_sprite)

    if len(throwntoys) > 1:
        throwntoys.remove(ball_sprite)
        splash.remove(ball_sprite)

def setup():
    global cycleCount #everything to run the game
    global inAlternateAnim, alternateAnimType, animationLoopTimes, frames #animation related
    global walkx, walky, direction #walking related
    global lastFedCycle, feedingCooldownCounter, foodz #food related
    global wakeywakey, consecutiveEvents #sleeping
    global throwntoys, lastexerciseCycle, exerciseNeed #he needs to move
    global inMenu, dialogStage #ui related
    global died, surviveCycle #Yeah, self-explanatory?
    global lastSaveCycle, epicVariable

    cycleCount = 0
    
    lastSaveCycle = cycleCount

    epicVariable = lastSaveCycle

    for x in range(len(foodz)):
        goner = foodz[0]
        del foodz[0]
        splash.remove(goner)
    foodz = []

    lastexerciseCycle = cycleCount+TargetFPS*startFitness # he need to do sport

    inMenu = False
    dialogStage = 0

    frames = {"background" : 0,
            "mouse" : 0,
            "unused1" : 0,
            "unused2" : 0,}
    inAlternateAnim = False
    alternateAnimType = 0
    animationLoopTimes = 0

    sprites = [
        itch_mouse_sprite,
        walk_mouse_sprite,
        sleep_mouse_sprite,
        died_mouse_sprite,
        angry_eyebrows_sprite,
        play_mouse_sprite,
    ]

    lastFedCycle = cycleCount+TargetFPS*startHunger # FEED THE MOUS PLEASEEEE
    feedingCooldownCounter = 0

    walkx = 0.0
    walky = 0.0
    direction = "right"

    wakeywakey = False
    consecutiveEvents = 0

    died = False
    surviveCycle = 0

    # Hide all sprites
    for sprite in sprites:
        sprite.hidden = True
    mouse_sprite.hidden = False

def CalculateGlideTo(sprite: displayio.TileGrid, x: int, y: int, inloops: int):
    global glideX
    global glideY
    global direction
    
    diffX = x - sprite.x 
    diffY = y - sprite.y

    if x < sprite.x:
        direction = "left"
    else:
        direction = "right"

    #Imagine a world, where we could change XY with FIRKCING FLOATS

    if inloops == 0:
        glideX = 0
        glideY = 0

    glideX = diffX / inloops
    glideY = diffY / inloops

#ui setup
bg = displayio.OnDiskBitmap("assets/border.bmp")
bg_Sprite = displayio.TileGrid(
    bg,
    pixel_shader=bg.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=(display.width - 128) // 2,  
    y=32
)
UIlayer.append(bg_Sprite)

bg2 = displayio.OnDiskBitmap("assets/border_bottom.bmp")
bg_Sprite2 = displayio.TileGrid(
    bg2,
    pixel_shader=bg2.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=(display.width - 128) // 2,  
    y=-128
)
UIlayer.append(bg_Sprite2)

labels = label.Label( #charlimit = ~25, this one uses a small font, haven't tested yet
    font= Delius8,
    text="",
    color=0x000000,
    scale=1,
    x=5,
    y=105
)
UIlayer.append(labels)

UIImage = displayio.TileGrid( #image to be used for bottom ui, only 32x32 tho
    cheese,
    pixel_shader=cheese.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=(display.width - 128) // 2,  
    y=-128
)
UIlayer.append(UIImage)

label2 = label.Label( #charlimit = 19, before it goes ofscreen
    font= Delius10,
    text="",
    color=0x000000,
    scale=1,
    x=5,
    y=105
)
UIlayer.append(label2)

autosave = label.Label( #charlimit = 19, before it goes ofscreen
    font= Delius10,
    text="",
    color=0xFFFFFF,
    scale=1,
    x=0,
    y=8
)
UIlayer.append(autosave)

def changeUIImage(image):
    if image == "":
        UIImage.hidden = True
    else:
        UIImage.hidden = False
        UIImage.bitmap = image
        if isinstance(image.pixel_shader, (displayio.ColorConverter, displayio.Palette)):
            UIImage.pixel_shader = image.pixel_shader
        else:
            UIImage.pixel_shader = displayio.ColorConverter()

def saveFileWrite():
    global epicVariable
    global lastSaveCycle
    try:
        toWrite = {"cyclecount": cycleCount,
                "lastfed": lastFedCycle,
                "lastexercise": lastexerciseCycle,
                "survivescore": surviveCycle,
                "mouseX": mouse_sprite.x,
                "mouseY": mouse_sprite.y,
                "house": backgroundID}
        with open("savefile.json","w") as f:
            json.dump(toWrite,f)
        autosave.text = "Saving..."
        epicVariable = cycleCount + (TargetFPS*3)
        lastSaveCycle = cycleCount
    except Exception as e:
        autosave.text = e
        epicVariable = cycleCount + (TargetFPS*3)
        time.sleep(3)
    
setup() #for the variables

#i know i'm supposed to check before loading, but ya know, that costs a lotta time todo
if not os.path.exists("savefile.json"):
    print("no savefile, continue setup")
    saveFileWrite()
    autosave.text = "Created save file"
else:
    try:
        with open("savefile.json","r") as file:
            savefile = json.load(file)
    except:
        savefile = {}

    print("found and loaded save file")
    if len(savefile) == 7:
        cycleCount = savefile["cyclecount"]
        lastFedCycle = savefile["lastfed"]
        lastexerciseCycle = savefile["lastexercise"]
        surviveCycle = savefile["survivescore"]
        mouse_sprite.x,mouse_sprite.y = savefile["mouseX"],savefile["mouseY"]
        backgroundID = savefile["house"]

        splash.remove(background_sprite)
        background_sheet = displayio.OnDiskBitmap(f"assets/room{backgroundID}.bmp")
        background_sprite = displayio.TileGrid(
            background_sheet,
            pixel_shader=background_sheet.pixel_shader,
            width=1,
            height=1,
            tile_width=128,
            tile_height=128,
            default_tile=0,
            x=(display.width - 128) // 2,  
            y=display.height - 128 - 0
        )
        splash.append(background_sprite)

        autosave.text = "Loaded save file"
        epicVariable = cycleCount + (TargetFPS*3)
    else:
        print("error with save file, or i coded wrong oosp.")
        saveFileWrite()

mainlayer.append(splash)
mainlayer.append(UIlayer)
display.show(mainlayer)

while True:
    cycleCount += 1
    keys = pygame.key.get_pressed()
    
    # layer sorting wooooo
    sorted_sprites = sorted(splash, key=lambda sprite: sprite.y)
    for sprite in splash[:]:  # im sure this wont cause any problems
        splash.remove(sprite)
    for sprite in sorted_sprites:
        splash.append(sprite)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if cycleCount % (TargetFPS*autosaveInterval) == 0:
        saveFileWrite()

    if epicVariable == cycleCount:
        autosave.text = ""

    if cycleCount % int(TargetFPS/2) == 0: #background
        background_sprite[0] = frames["background"]
        frames["background"] = (frames["background"] + 1) % (background_sheet.width // background_sprite.tile_width)

    #the original if statement was WAAAY too long, simpler :)
    #expansion script bottom UI
    conditions = {"hungryIn5Secs" : int((lastFedCycle-cycleCount)/TargetFPS) <= 5, "fedTooMuch" : lastFedCycle >= cycleCount+(TargetFPS*(tooFedTime-10)*nutritionalValue), "tooLittleExercise" : int((lastexerciseCycle-cycleCount)/TargetFPS) <= 5, "toomuchexercise" : lastexerciseCycle >= cycleCount+(TargetFPS*(tooExercise-10)*30),}
    if conditions["hungryIn5Secs"] or conditions["fedTooMuch"] or conditions["toomuchexercise"] or conditions["tooLittleExercise"] or (keys[pygame.K_LEFT] and not inMenu) or died: # if less than 5 secs left befor hungy
        if not bg_Sprite.y <= 0:
            bg_Sprite.y -= 2
        bg_Sprite[0] = 1
    else:   
        if bg_Sprite.y <= 32:
            bg_Sprite.y += 2

    #expansion script for top UI
    if (keys[pygame.K_UP] and died == False) or (died == True and animationLoopTimes == 1):
        if not bg_Sprite2.y >= -96:
            bg_Sprite2.y += 2        
        
        inMenu = not (died == True and animationLoopTimes == 1)

        conditions = {"foodLimit" : len(foodz) == cheezesspawnlimit, "toyLimit" : len(throwntoys) == 1, "foodCooldown" : feedingCooldownCounter+(TargetFPS*feedingCooldown) > cycleCount}

        if (conditions["foodLimit"] or conditions["foodCooldown"]) and conditions["toyLimit"]: #for some *flair*
            bg_Sprite2[0] = 1
        elif conditions["toyLimit"]:
            bg_Sprite2[0] = 2
        elif conditions["foodCooldown"] or conditions["foodLimit"]:
            bg_Sprite2[0] = 3
        else:
            bg_Sprite2[0] = 0
    else:
        if not bg_Sprite2.y <= -128:
            bg_Sprite2.y -= 2
        inMenu = False

    labels.x= bg_Sprite.x+5
    labels.y= bg_Sprite.y+110
    labels.hidden = bg_Sprite.hidden

    UIImage.x = bg_Sprite.x+90
    UIImage.y = bg_Sprite.y+95
    UIImage.hidden = bg_Sprite.hidden

    label2.x= bg_Sprite2.x+5
    label2.y= bg_Sprite2.y+110
    label2.hidden = bg_Sprite2.hidden

    # should happen every tick /\

    if died == False: #should only happen if mous is not ded
        if keys[pygame.K_UP]:
            if inMenu: #better safe than sorry
                if keys[pygame.K_RIGHT]:
                    if not feedingCooldownCounter+(TargetFPS*feedingCooldown) > cycleCount:
                        if not alternateAnimType == 3:
                            giveFood()
                            feedingCooldownCounter = cycleCount
                        if alternateAnimType == 3:
                            wakeywakey = True
                        else:
                            wakeywakey = False
                if keys[pygame.K_LEFT]:
                    throwBall()
                    wakeywakey = True
        else:

            if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and not inMenu:
                if os.path.exists("savefile.json"):
                    os.remove("savefile.json")
                    autosave.text = "Restart to delete save,\n (RIGHT) to restore"
                    epicVariable = cycleCount + (TargetFPS*3)
                else:
                    autosave.text = "No save file detected"
                    epicVariable = cycleCount + (TargetFPS*3)
            else:
                if keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not inMenu:
                    saveFileWrite()
            

        if cycleCount % int(TargetFPS/5) == 0: #update the mouse
            if inAlternateAnim == False:

                mouse_sprite[0] = frames["mouse"]
                frames["mouse"] = (frames["mouse"] + 1) % (mouse_sheet.width // mouse_sprite.tile_width)

                if len(throwntoys) > 0 and not cycleCount >= lastFedCycle:
                    itch_mouse_sprite.hidden = True
                    walk_mouse_sprite.hidden = False
                    sleep_mouse_sprite.hidden = True
                    mouse_sprite.hidden = True
                    inAlternateAnim = False

                    walk_mouse_sprite.x = mouse_sprite.x
                    walk_mouse_sprite.y = mouse_sprite.y

                    inAlternateAnim = True
                    alternateAnimType = 5
                    animationLoopTimes = 3
                    frames["mouse"] = 0

                    walkx = walk_mouse_sprite.x
                    walky = walk_mouse_sprite.y

                    CalculateGlideTo(walk_mouse_sprite,throwntoys[0].x,throwntoys[0].y,animationLoopTimes*3)
                elif len(foodz) > 0:
                    itch_mouse_sprite.hidden = True
                    walk_mouse_sprite.hidden = False
                    sleep_mouse_sprite.hidden = True
                    mouse_sprite.hidden = True
                    inAlternateAnim = False

                    walk_mouse_sprite.x = mouse_sprite.x
                    walk_mouse_sprite.y = mouse_sprite.y

                    inAlternateAnim = True
                    alternateAnimType = 4
                    animationLoopTimes = 3
                    frames["mouse"] = 0

                    walkx = walk_mouse_sprite.x
                    walky = walk_mouse_sprite.y

                    CalculateGlideTo(walk_mouse_sprite,foodz[0].x,foodz[0].y,animationLoopTimes*3)

                if frames["mouse"] == 0 and not alternateAnimType in [4,5]: #end of anim cycle! time to roll for an event
                    if not consecutiveEvents >= 5:
                        if randint(1,2) == 1: #50% for fun random event
                            consecutiveEvents += 1 # so we know when he need to slepp
                            chance = randint(1,10)
                            if chance in [1,2,3,4]: #itchy mouse
                                itch_mouse_sprite.x = mouse_sprite.x
                                itch_mouse_sprite.y = mouse_sprite.y

                                mouse_sprite.hidden = True
                                itch_mouse_sprite.hidden = False

                                inAlternateAnim = True
                                alternateAnimType = 1
                                frames["mouse"] = 0
                            if chance in [5,6,7,8]: #mouse wandering
                                walk_mouse_sprite.x = mouse_sprite.x
                                walk_mouse_sprite.y = mouse_sprite.y

                                walk_mouse_sprite.hidden = False
                                mouse_sprite.hidden = True

                                inAlternateAnim = True
                                alternateAnimType = 2
                                animationLoopTimes = 3
                                frames["mouse"] = 0

                                walkx = walk_mouse_sprite.x
                                walky = walk_mouse_sprite.y

                                CalculateGlideTo(walk_mouse_sprite,randint(0,95),randint(72,108),animationLoopTimes*3)

                                mouse_sprite.hidden = True
                    else: #nothinf happenign, mous slepp
                        sleep_mouse_sprite.x = mouse_sprite.x
                        sleep_mouse_sprite.y = mouse_sprite.y

                        mouse_sprite.hidden = True
                        sleep_mouse_sprite.hidden = False

                        inAlternateAnim = True
                        alternateAnimType = 3
                        frames["mouse"] = 0


            else:
                if alternateAnimType == 1: #itchy mouse
                    itch_mouse_sprite[0] = frames["mouse"]
                    frames["mouse"] = (frames["mouse"] + 1) % (itch_mouse_sheet.width // itch_mouse_sprite.tile_width) 

                    if frames["mouse"] == 0:
                            mouse_sprite.x = itch_mouse_sprite.x
                            mouse_sprite.y = itch_mouse_sprite.y
                            itch_mouse_sprite.hidden = True

                            mouse_sprite.hidden = False
                            inAlternateAnim = False

                            alternateAnimType = 0

                if alternateAnimType in [2,4,5]: #wandering mouse

                    if direction == "right":
                        walk_mouse_sprite.flip_x = False
                    else:
                        walk_mouse_sprite.flip_x = True

                    walk_mouse_sprite[0] = frames["mouse"]
                    frames["mouse"] = (frames["mouse"] + 1) % (walk_mouse_sheet.width // walk_mouse_sprite.tile_width)

                    walkx += glideX
                    walky += glideY

                    walk_mouse_sprite.x = int(walkx)
                    walk_mouse_sprite.y = int(walky)

                    if frames["mouse"] == 0:
                        if animationLoopTimes > 0:
                            animationLoopTimes = animationLoopTimes -1
                        else:
                            if alternateAnimType == 4:
                                goner = foodz[0]
                                del foodz[0]
                                splash.remove(goner)
                                consecutiveEvents = 0
                                mouse_sprite.x = walk_mouse_sprite.x
                                mouse_sprite.y = walk_mouse_sprite.y
                                walk_mouse_sprite.hidden = True

                                mouse_sprite.hidden = False
                                inAlternateAnim = False

                                lastFedCycle += TargetFPS*nutritionalValue
                                alternateAnimType = 0
                            elif alternateAnimType == 5: #Pip arrived at his destenation
                                goner = throwntoys[0]
                                del throwntoys[0]
                                splash.remove(goner)
                                consecutiveEvents = 0
                                play_mouse_sprite.x = walk_mouse_sprite.x-20
                                play_mouse_sprite.y = walk_mouse_sprite.y-20
                                walk_mouse_sprite.hidden = True
                                animationLoopTimes = 3

                                play_mouse_sprite.hidden = False
                                alternateAnimType = 6
                            else:
                                mouse_sprite.x = walk_mouse_sprite.x
                                mouse_sprite.y = walk_mouse_sprite.y
                                walk_mouse_sprite.hidden = True

                                mouse_sprite.hidden = False
                                inAlternateAnim = False
                                alternateAnimType = 0

                if alternateAnimType == 3: #sleepyu mouse
                    sleep_mouse_sprite[0] = frames["mouse"]
                    frames["mouse"] = (frames["mouse"] + 1) % (sleep_mouse_sheet.width // sleep_mouse_sprite.tile_width)

                    if wakeywakey == True:
                            mouse_sprite.x = sleep_mouse_sprite.x
                            mouse_sprite.y = sleep_mouse_sprite.y
                            sleep_mouse_sprite.hidden = True

                            consecutiveEvents = 0

                            mouse_sprite.hidden = False
                            inAlternateAnim = False

                            alternateAnimType = 0

                if alternateAnimType == 6: #mous playing with ball c:
                    if cycleCount % int(TargetFPS/3) == 0:
                        play_mouse_sprite[0] = frames["mouse"]
                        frames["mouse"] = (frames["mouse"] + 1) % (play_mouse_sheet.width // play_mouse_sprite.tile_width) 

                    if frames["mouse"] == 0:
                        if animationLoopTimes > 0:
                            animationLoopTimes -= 1
                        else:
                            mouse_sprite.x = play_mouse_sprite.x+20
                            mouse_sprite.y = play_mouse_sprite.y+20
                            play_mouse_sprite.hidden = True

                            mouse_sprite.hidden = False
                            inAlternateAnim = False

                            lastexerciseCycle += TargetFPS*30

                            alternateAnimType = 0

        if mouse_sprite.x < 0:
            mouse_sprite.x = 0
        elif mouse_sprite.x > 96:
            mouse_sprite.x = 96

        if walk_mouse_sprite.x < 0:
            walk_mouse_sprite.x = 0
        elif walk_mouse_sprite.x > 96:
            walk_mouse_sprite.x = 96

        if cycleCount >= lastFedCycle: # if hunger
            angry_eyebrows_sprite.hidden = mouse_sprite.hidden

            angry_eyebrows_sprite.x = mouse_sprite.x
            angry_eyebrows_sprite.y = mouse_sprite.y - 1
            if cycleCount >= lastFedCycle+(TargetFPS*notFedTime): #oop too hungy
                died = True
                mouse_sprite.hidden = True
                itch_mouse_sprite.hidden = True
                walk_mouse_sprite.hidden = True
                sleep_mouse_sprite.hidden = True
                play_mouse_sprite.hidden = True
                died_mouse_sprite.hidden = False
                angry_eyebrows_sprite.hidden = True

                died_mouse_sprite.x = mouse_sprite.x
                died_mouse_sprite.y = mouse_sprite.y

                animationLoopTimes = 5

                cause = 1
                surviveCycle = cycleCount

                frames["mouse"] = 0
        else:
            angry_eyebrows_sprite.hidden = True
            if lastFedCycle >= cycleCount+(TargetFPS*tooFedTime*nutritionalValue): # oop too uhhh full???
                died = True
                mouse_sprite.hidden = True
                itch_mouse_sprite.hidden = True
                walk_mouse_sprite.hidden = True
                sleep_mouse_sprite.hidden = True
                play_mouse_sprite.hidden = True
                died_mouse_sprite.hidden = False
                angry_eyebrows_sprite.hidden = True

                died_mouse_sprite.x = mouse_sprite.x
                died_mouse_sprite.y = mouse_sprite.y

                animationLoopTimes = 5

                cause = 2
                surviveCycle = cycleCount

                frames["mouse"] = 1

        if cycleCount >= lastexerciseCycle: # if no sport
            if cycleCount >= lastexerciseCycle+(TargetFPS*exerciseNeed): #he needs sport tho
                died = True
                mouse_sprite.hidden = True
                itch_mouse_sprite.hidden = True
                walk_mouse_sprite.hidden = True
                sleep_mouse_sprite.hidden = True
                play_mouse_sprite.hidden = True
                died_mouse_sprite.hidden = False
                angry_eyebrows_sprite.hidden = True

                died_mouse_sprite.x = mouse_sprite.x
                died_mouse_sprite.y = mouse_sprite.y

                animationLoopTimes = 5

                cause = 3
                surviveCycle = cycleCount

                frames["mouse"] = 0
        else:
            if lastexerciseCycle >= cycleCount+(TargetFPS*tooExercise*30): # exhausted
                died = True
                mouse_sprite.hidden = True
                itch_mouse_sprite.hidden = True
                walk_mouse_sprite.hidden = True
                sleep_mouse_sprite.hidden = True
                play_mouse_sprite.hidden = True
                died_mouse_sprite.hidden = False
                angry_eyebrows_sprite.hidden = True

                died_mouse_sprite.x = mouse_sprite.x
                died_mouse_sprite.y = mouse_sprite.y

                animationLoopTimes = 5

                cause = 4
                surviveCycle = cycleCount

                frames["mouse"] = 1

        #all done i think
        if int((lastFedCycle-cycleCount)/TargetFPS) <= 0:
            labels.text = "PIP IS HUNGRY!!!"
            changeUIImage(cheese)
        elif lastFedCycle >= cycleCount+(TargetFPS*(tooFedTime-10)*nutritionalValue): # slow down...
            labels.text = f"TOO MUCH FOOD!!!!!"
            changeUIImage(cheese)
        elif int((lastexerciseCycle-cycleCount)/TargetFPS) <= 0:
            labels.text = "PIP NEEDS EXERCISE!"
            changeUIImage("")
        elif lastexerciseCycle >= cycleCount+(TargetFPS*(tooExercise-10)*30):
            labels.text = "TOO MUCH EXERCISE!"
            changeUIImage("")
        else:
            if int(cycleCount/TargetFPS) % 15 <= 5 or int((lastFedCycle-cycleCount)/TargetFPS) <= 5:
                remaining_time = (lastFedCycle - cycleCount) / TargetFPS
            elif int(cycleCount/TargetFPS) % 15 <= 10 or int((lastexerciseCycle-cycleCount)/TargetFPS) <= 5:
                remaining_time = (lastexerciseCycle - cycleCount) / TargetFPS        
            else:
                remaining_time = cycleCount / TargetFPS

            minutes = int(remaining_time // 60)  # Extract full minutes
            seconds = int(remaining_time % 60)   # Extract remaining seconds

            if int(cycleCount/TargetFPS) % 15 <= 5 or int((lastFedCycle-cycleCount)/TargetFPS) <= 5:
                labels.text = f"Hungry in: {minutes:01} : {seconds:02}"
                changeUIImage(cheese)
            elif int(cycleCount/TargetFPS) % 15 <= 10 or int((lastexerciseCycle-cycleCount)/TargetFPS) <= 5:
                labels.text = f"Exercise in: {minutes:01} : {seconds:02}"   
                changeUIImage(ball)
            else:
                labels.text = f"Time alive: {minutes:01} : {seconds:02}"
                changeUIImage(heart)

    else: # ded xc
        changeUIImage("")
        bg_Sprite2[0] = 4
        if animationLoopTimes == 5 and dialogStage == 0:
            choices = ["oh no...","wait...","is- did he?"]
            labels.text = choices[randint(0,len(choices)-1)]
            dialogStage = 1

        if surviveCycle+1 == cycleCount:
            saveFileWrite()

        if cycleCount % int(TargetFPS) == 0:
            died_mouse_sprite[0] = frames["mouse"]
            frames["mouse"] = (frames["mouse"] + 1) % (died_mouse_sheet.width // died_mouse_sprite.tile_width)

            if frames["mouse"] == 0:
                if animationLoopTimes > 0:
                    animationLoopTimes -= 1
                if animationLoopTimes == 4:
                    choices = ["pip died...","is he okay?","he died...","PIP! ARE YOU OKAY?"]
                    labels.text = choices[randint(0,len(choices)-1)]
                if animationLoopTimes == 3:
                    if cause == 1:
                        choices = ["he starved...","wheres the food?","you gotta feed him!"]
                    elif cause == 2:
                        choices = ["he was overfed...","thats, too much...","too much food..."]
                    elif cause == 3:
                        choices = ["he needs exercise...","he needs to move...","lack of movement..."]
                    elif cause == 4:
                        choices = ["he's exhausted...","too much exercise...","he needs rest..."]
                    else:
                        labels.text = "huh, that's weird..."
                    labels.text = choices[randint(0,len(choices)-1)]
                if animationLoopTimes == 2:
                    if cause == 1:
                        choices = ["give him more food...","please feed him...","can you give food?"]
                    elif cause == 2:
                        choices = ["less food next time...","pip has his limits.","mice eat less..."]
                    elif cause == 3:
                        choices = ["throw a ball to him...","play with him :(","he needs exercise..."]
                    elif cause == 4:
                        choices = ["a small mouse has limits...","pip needs his rest...","maybe let him rest?"]
                    else:
                        choices = ["what happened?"]
                    labels.text = choices[randint(0,len(choices)-1)]
                if animationLoopTimes == 1:
                    choices = ["poor thing...","aw man...","sorry pip..."]
                    labels.text = choices[randint(0,len(choices)-1)]

                    remaining_time = surviveCycle / TargetFPS
                    minutes = int(remaining_time // 60)  # Extract full minutes
                    seconds = int(remaining_time % 60)   # Extract remaining seconds
                    label2.text = f"Time alive: {minutes:01} : {seconds:02}"
                if animationLoopTimes == 0:
                    labels.text = "Press (UP) to restart"
                
        if animationLoopTimes == 0:
            if keys[pygame.K_UP]:
                label2.text = ""
                setup()

    time.sleep(1/TargetFPS) #Should bring us close enough

    if debug:
        debugString = ""
        debugString = debugString + f"cyclecount: {cycleCount} | "
        debugString = debugString + f"last fed: {lastFedCycle} | "
        debugString = debugString + f"consecutiveActions: {consecutiveEvents} | "
        debugString = debugString + f"alternateAnim: {inAlternateAnim} | "
        debugString = debugString + f"animType: {alternateAnimType} | "
        debugString = debugString + f"foods : {len(foodz)} | "
        debugString = debugString + f"animationcycle : {animationLoopTimes} | "
        #debugString = debugString + f"walkHid: {walk_mouse_sprite.hidden} | "
        #debugString = debugString + f"itchHid: {itch_mouse_sprite.hidden} | "
        #debugString = debugString + f"mouseHid: {mouse_sprite.hidden} | "
        #debugString = debugString + f"sleepHid: {sleep_mouse_sprite.hidden} | "
        #debugString = debugString + f"playHid: {play_mouse_sprite.hidden} | "
        #debugString = debugString + f"died: {died} | "

        print(debugString)
