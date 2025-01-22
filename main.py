import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
from random import randint
from random import seed
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap

indieFlower12 = bitmap_font.load_font("fonts/Indie-Flower-11.bdf", Bitmap)

for x in range(randint(0,10)): #This might look dangerous and all, but this is just to make RNG a bit better
    seed(randint(0,9999999+x))

pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
UIlayer = displayio.Group()
mainlayer = displayio.Group()

# Config
debug = False
TargetFPS = 15 # default = 15 (does change the animation speeds, FIXED WHOOOOOO)
cheezesspawnlimit = 5 #for performance and also so it doesnt explod (default = 10)
feedingCooldown = 1 #cooldown inbetween giving food (in seconds, default 1)
notFedTime = 20 #amount of time of unfed before death (in seconds, default 20)
tooFedTime = 50 #amount of food before death (in amounts of food, default 50)
nutritionalValue = 20 #uhhh yeah (default 20)
startHunger = 30 #how much time before mous starts to get hungy (in seconds, default 30)

cheese = displayio.OnDiskBitmap("assets/cheese.bmp")
apple = displayio.OnDiskBitmap("assets/apple_slice.bmp")
peanut = displayio.OnDiskBitmap("assets/peanut.bmp")
grapes = displayio.OnDiskBitmap("assets/grapes.bmp")
foods = [cheese,grapes,peanut,apple]

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

# Background Spritesheet #
background_sheet = displayio.OnDiskBitmap(f"assets/room{randint(1,2)}.bmp")
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

# walk mirrored Mouse Spritesheet #
walkm_mouse_sheet = displayio.OnDiskBitmap("assets/walkmirror_mouse.bmp")
walkm_mouse_sprite = displayio.TileGrid(
    walkm_mouse_sheet,
    pixel_shader=walkm_mouse_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=0,  
    y=display.height - 32 - 10     
)
splash.append(walkm_mouse_sprite)

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

def setup():
    global frames
    global cycleCount
    global inAlternateAnim
    global alternateAnimType
    global walkx
    global walky
    global lastFedCycle
    global direction
    global wakeywakey
    global consecutiveEvents
    global died
    global insertcoolvariablename
    global animationLoopTimes
    global dialogStage
    global surviveCycle
    global foodz

    for x in range(len(foodz)):
        goner = foodz[0]
        del foodz[0]
        splash.remove(goner)
    foodz = []

    surviveCycle = 0

    dialogStage = 0

    animationLoopTimes = 0

    frames = {"background" : 0,
            "mouse" : 0,
            "unused1" : 0,
            "unused2" : 0,}

    cycleCount = 0

    inAlternateAnim = False
    alternateAnimType = 0

    walkx = 0.0
    walky = 0.0

    sprites = [
        itch_mouse_sprite,
        walk_mouse_sprite,
        sleep_mouse_sprite,
        walkm_mouse_sprite,
        died_mouse_sprite,
        angry_eyebrows_sprite
    ]

    # Hide all sprites
    for sprite in sprites:
        sprite.hidden = True

    lastFedCycle = TargetFPS*startHunger # FEED THE MOUS PLEASEEEE

    direction = "right"

    wakeywakey = False
    consecutiveEvents = 0

    died = False
    insertcoolvariablename = 0

    mouse_sprite.hidden = False

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
    y=-128
)
UIlayer.append(bg_Sprite)

bg_Sprite2 = displayio.TileGrid(
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
UIlayer.append(bg_Sprite2)

labels = label.Label( #charlimit = 19, before it goes ofscreen
    font= indieFlower12,
    text="",
    color=0x000000,
    scale=1,
    x=5,
    y=105
)
UIlayer.append(labels)


label2 = label.Label( #charlimit = 19, before it goes ofscreen
    font= indieFlower12,
    text="",
    color=0x000000,
    scale=1,
    x=5,
    y=105
)
UIlayer.append(label2)

mainlayer.append(splash)
mainlayer.append(UIlayer)
display.show(mainlayer)

setup() #for the variables
while True:

    keys = pygame.key.get_pressed()
    # sortiiibnggggg
    sorted_sprites = sorted(splash, key=lambda sprite: sprite.y)

    for sprite in splash[:]:  # im sure this wont cause any problems
        splash.remove(sprite)

    for sprite in sorted_sprites:
        splash.append(sprite)

    cycleCount += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if died == False:
        splash.remove(angry_eyebrows_sprite)
        splash.append(angry_eyebrows_sprite)

        if keys[pygame.K_UP]:
            if not insertcoolvariablename+(TargetFPS*feedingCooldown) > cycleCount:
                giveFood()
                insertcoolvariablename = cycleCount
                if alternateAnimType == 3:
                    wakeywakey = True
                else:
                    wakeywakey = False

        if keys[pygame.K_DOWN]:
            if alternateAnimType == 3:
                wakeywakey = True
            else:
                wakeywakey = False

        if cycleCount % int(TargetFPS/5) == 0: #pip the mouse, like the python pip haha 
            if inAlternateAnim == False:

                mouse_sprite[0] = frames["mouse"]
                frames["mouse"] = (frames["mouse"] + 1) % (mouse_sheet.width // mouse_sprite.tile_width)

                if len(foodz) > 0:

                    itch_mouse_sprite.hidden = True
                    walk_mouse_sprite.hidden = True
                    walkm_mouse_sprite.hidden = True
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

                    if direction == "right":
                        walk_mouse_sprite.hidden = False
                        walkm_mouse_sprite.hidden = True
                    else:
                        walk_mouse_sprite.hidden = True
                        walkm_mouse_sprite.hidden = False

                if frames["mouse"] == 0 and not alternateAnimType == 4: #end of anim cycle! time to roll for an event
                    if not consecutiveEvents >= 5:
                        if randint(1,2) == 1: #50% for fun random event
                            consecutiveEvents += 1
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

                                inAlternateAnim = True
                                alternateAnimType = 2
                                animationLoopTimes = 3
                                frames["mouse"] = 0

                                walkx = walk_mouse_sprite.x
                                walky = walk_mouse_sprite.y

                                CalculateGlideTo(walk_mouse_sprite,randint(0,95),randint(72,108),animationLoopTimes*3)

                                mouse_sprite.hidden = True
                                if direction == "right":
                                    walk_mouse_sprite.hidden = False
                                    walkm_mouse_sprite.hidden = True
                                else:
                                    walk_mouse_sprite.hidden = True
                                    walkm_mouse_sprite.hidden = False
                    else:
                        sleep_mouse_sprite.x = mouse_sprite.x #nothinf happenign, mous slepp
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

                if alternateAnimType in [2,4]: #wandering mouse

                    if direction == "right":
                        walk_mouse_sprite[0] = frames["mouse"]
                        frames["mouse"] = (frames["mouse"] + 1) % (walk_mouse_sheet.width // walk_mouse_sprite.tile_width) 
                    else:
                        walkm_mouse_sprite[0] = frames["mouse"]
                        frames["mouse"] = (frames["mouse"] + 1) % (walkm_mouse_sheet.width // walkm_mouse_sprite.tile_width) 

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
                                walkm_mouse_sprite.hidden = True

                                mouse_sprite.hidden = False
                                inAlternateAnim = False

                                lastFedCycle += TargetFPS*nutritionalValue

                                alternateAnimType = 0
                            else:
                                mouse_sprite.x = walk_mouse_sprite.x
                                mouse_sprite.y = walk_mouse_sprite.y
                                walk_mouse_sprite.hidden = True
                                walkm_mouse_sprite.hidden = True

                                mouse_sprite.hidden = False
                                inAlternateAnim = False

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

        if mouse_sprite.x < 0:
            mouse_sprite.x = 0
        elif mouse_sprite.x > 96:
            mouse_sprite.x = 96

        if walk_mouse_sprite.x < 0:
            walk_mouse_sprite.x = 0
        elif walk_mouse_sprite.x > 96:
            walk_mouse_sprite.x = 96

        if cycleCount >= lastFedCycle: # add +(TargetFPS*1) if ya want it to be time based idk
            angry_eyebrows_sprite.hidden = mouse_sprite.hidden

            angry_eyebrows_sprite.x = mouse_sprite.x
            angry_eyebrows_sprite.y = mouse_sprite.y - 1
            if cycleCount >= lastFedCycle+(TargetFPS*notFedTime): #oop too hungy
                died = True
                mouse_sprite.hidden = True
                itch_mouse_sprite.hidden = True
                walk_mouse_sprite.hidden = True
                sleep_mouse_sprite.hidden = True
                walkm_mouse_sprite.hidden = True
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
                walkm_mouse_sprite.hidden = True
                died_mouse_sprite.hidden = False
                angry_eyebrows_sprite.hidden = True

                died_mouse_sprite.x = mouse_sprite.x
                died_mouse_sprite.y = mouse_sprite.y

                animationLoopTimes = 5

                cause = 2
                surviveCycle = cycleCount

                frames["mouse"] = 1

        walkm_mouse_sprite.x = walk_mouse_sprite.x
        walkm_mouse_sprite.y = walk_mouse_sprite.y

        if lastFedCycle >= cycleCount+(TargetFPS*(tooFedTime-10)*nutritionalValue): # oop too uhhh full???
            labels.text = f"TOO MUCH FOOD!!!!!"
        elif int((lastFedCycle-cycleCount)/TargetFPS)-1 >= 0:
            remaining_time = (lastFedCycle - cycleCount) / TargetFPS
            minutes = int(remaining_time // 60)  # Extract full minutes
            seconds = int(remaining_time % 60)   # Extract remaining seconds

            labels.text = f"Hungry in: {minutes:01} : {seconds:02}"
        else:
            labels.text = "PIP IS HUNGRY!!!"

        remaining_time = cycleCount / TargetFPS
        minutes = int(remaining_time // 60)  # Extract full minutes
        seconds = int(remaining_time % 60)   # Extract remaining seconds
        label2.text = f"Time alive: {minutes:01} : {seconds:02}"
    else: # ded xc
        if animationLoopTimes == 5 and dialogStage == 0:
            choices = ["oh no...","wait...","is- did he?"]
            labels.text = choices[randint(0,len(choices)-1)]
            dialogStage = 1

        if cycleCount % int(TargetFPS) == 0:
            died_mouse_sprite[0] = frames["mouse"]
            frames["mouse"] = (frames["mouse"] + 1) % (died_mouse_sheet.width // died_mouse_sprite.tile_width)

            if frames["mouse"] == 0:
                if animationLoopTimes > 0:
                    animationLoopTimes -= 1
                if animationLoopTimes == 4:
                    choices = ["pip died...","IS HE OKAY?","he died..."]
                    labels.text = choices[randint(0,len(choices)-1)]
                if animationLoopTimes == 3:
                    if cause == 1:
                        choices = ["he starved...","wheres the food?","you gotta feed him!"]
                        labels.text = choices[randint(0,len(choices)-1)]
                    elif cause == 2:
                        choices = ["he was overfed...","thats, too much...","too much food..."]
                        labels.text = choices[randint(0,len(choices)-1)]
                    else:
                        labels.text = "huh, that's weird..."
                if animationLoopTimes == 2:
                    if cause == 1:
                        choices = ["give him more food","please feed him...","can you give food?"]
                        labels.text = choices[randint(0,len(choices)-1)]
                    elif cause == 2:
                        choices = ["less food next time","pip has his limits","mice eat less..."]
                        labels.text = choices[randint(0,len(choices)-1)]
                    else:
                        labels.text = "what happened?"
                if animationLoopTimes == 1:
                    choices = ["poor thing...","aw man...","sorry pip..."]
                    labels.text = choices[randint(0,len(choices)-1)]

                    remaining_time = surviveCycle / TargetFPS
                    minutes = int(remaining_time // 60)  # Extract full minutes
                    seconds = int(remaining_time % 60)   # Extract remaining seconds
                    label2.text = f"Time alive: {minutes:01} : {seconds:02}"
                if animationLoopTimes == 0:
                    labels.text = "(DOWN) to restart"
                
        if animationLoopTimes == 0:
            if keys[pygame.K_DOWN]:
                setup()


    # should happen every tick \/

    if cycleCount % int(TargetFPS/2) == 0: #background
        background_sprite[0] = frames["background"]
        frames["background"] = (frames["background"] + 1) % (background_sheet.width // background_sprite.tile_width)

    if int((lastFedCycle-cycleCount)/TargetFPS) <= 5 or keys[pygame.K_LEFT] or died or lastFedCycle >= cycleCount+(TargetFPS*(tooFedTime-10)*nutritionalValue): # if less than 5 secs left befor hungy
        if not bg_Sprite.y >= -96:
            bg_Sprite.y += 2
    else:
        if not bg_Sprite.y <= -128:
            bg_Sprite.y -= 2

    if (keys[pygame.K_LEFT] and died == False) or (died == True and animationLoopTimes == 1):
        if not bg_Sprite2.y <= 0:
            bg_Sprite2.y -= 2
    else:
        if bg_Sprite2.y <= 32:
            bg_Sprite2.y += 2

    labels.x= bg_Sprite.x+5
    labels.y= bg_Sprite.y+110
    labels.hidden = bg_Sprite.hidden

    label2.x= bg_Sprite2.x+5
    label2.y= bg_Sprite2.y+110
    label2.hidden = bg_Sprite2.hidden

    time.sleep(1/TargetFPS) #Should bring us close enough

    if debug:
        debugString = ""
        debugString = debugString + f"cyclecount: {cycleCount} | "
        debugString = debugString + f"last fed: {lastFedCycle} | "
        debugString = debugString + f"consecutiveActions: {consecutiveEvents} | "
        debugString = debugString + f"alternateAnim: {inAlternateAnim} | "
        debugString = debugString + f"animType: {alternateAnimType} | "
        debugString = debugString + f"foods left : {len(foodz)} | "
        debugString = debugString + f"animationcycle : {animationLoopTimes} | "
        #debugString = debugString + f"walkHid: {walk_mouse_sprite.hidden} | "
        #debugString = debugString + f"itchHid: {itch_mouse_sprite.hidden} | "
        #debugString = debugString + f"mouseHid: {mouse_sprite.hidden} | "
        #ebugString = debugString + f"sleepHid: {sleep_mouse_sprite.hidden} | "
        #debugString = debugString + f"died: {died} | "

        print(debugString)