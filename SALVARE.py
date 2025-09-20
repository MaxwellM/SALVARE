import pygame, os
from pygame.constants import QUIT, USEREVENT, KEYUP, K_ESCAPE, KEYDOWN, K_q, K_r, K_SPACE, K_RETURN, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_s, FULLSCREEN, K_EQUALS, K_PLUS, K_MINUS, K_UNDERSCORE, RLEACCEL, SRCALPHA
from math import sqrt, pi, atan2, cos, sin
from random import randint, randrange, choice


# os.environ["SDL_VIDEODRIVER"] = "x11"

# This area is setting up some variables that will be used throughout the program



screenx = 1440                      #horizontal screen size
screeny = 900                       #verticle screen size
shazbot = 0                         #shazbot, look it up...
clock = pygame.time.Clock()
textupdate = pygame.time.Clock()
repeatrate = 25
probex = 0                          #probe x location
probey = 0                          #porbe y location
xvelocity = 0                       #variables used to help calculate the pyhsics
yvelocity = 0
score = 0                           #How good you are at this kind of thing
powermultiplier = 0.01              #This is the variable used to determine the power level of launching the probe                   #Tells when to start keeping score
bodiesdrawn = 0                     #Used to tell when the planets have been drawn onto the screen
drawingbodies = 0                   #Used to tell when to draw the planets onto the screen
gameframerate = 60                  #Target framerate, currently, while the probe is on the screen it is difficult to to maintain more than 60FPS average
close = 0

blackholepos = []
probepos = []
update = []
update2 = []
menurects = []
menurects2 = []
proberects = []
barralrects = []
powerrects = []
endrects = []
masterrects = []
planetrect = []

#Colours
black = (0, 0, 0)
white = (255, 255, 255)
verylightblue = (100, 100, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
gasplanet = (216, 148, 36)

flags1 = FULLSCREEN
flags = RLEACCEL

randombodies = 1                 #The current and only 'working' game mode

fuel = 500                           #How many times you can 'nudge' the probe
r2 = 20
r = 5                               #Beginning radius of the planets, used to calculate collision
blackholebodyies = 1
blackholedrawing = 0
blackholebodyiesdrawn = 0
numberofbodies = 3                  #Number of planets that get drawn, can be changed to either a random range, or to any number you can dream of...
bodycenters = []                #Used to store the X and Y coordinates of planet locations
bodycenters2 = []
massofbodies = choice([20, 25, 50])  #The range of mass that is randomly chosen for the planets, individually
blackmass = 10000
gravitationalconstant = 15          #Used with physics
numer = massofbodies * gravitationalconstant #Used with physics
numer2 = blackmass * gravitationalconstant

start_time = 60
frame_count = 0

#This is used to load commonly used data that is required throughout the game
def initiatepygame():
    global screen, channel5, channel4, satmanR, satmanAR, jupiterA, marsA, plutoA, bjupiterA, bearthA, satmanA, earth, jupiter, mars, pluto, bearth, bjupiter, background, screen5, screen6, beep, scan, crash, launch, thrust, empty, satman, soundtrack, newbutton, sunpic2, blackhole, whoosh, screen9, warning
    pygame.init()
    screen = pygame.display.set_mode((screenx, screeny), flags1, 32)
    screen6 = pygame.Surface((150, 150), flags, 32).convert_alpha()
    screen5 = pygame.Surface((20, 20), flags, 32).convert_alpha()
    pygame.display.set_caption('Salvare')
    satman = pygame.image.load('satman6.png').convert_alpha()
    earth = pygame.image.load('testearth.png').convert_alpha()
    jupiter = pygame.image.load('testjupiter.png').convert_alpha()
    jupiterA = pygame.image.load('jupiterA.png').convert_alpha()
    mars = pygame.image.load('testmars.png').convert_alpha()
    marsA = pygame.image.load('mars2A.png').convert_alpha()
    pluto = pygame.image.load('testpluto.png').convert_alpha()
    plutoA = pygame.image.load('pluto2A.png').convert_alpha()
    sunpic2 = pygame.image.load('testbackground22.png').convert_alpha()
    blackhole = pygame.image.load('blackhole.png').convert_alpha()
    bearth = pygame.image.load('bearth2.png').convert_alpha()
    bearthA = pygame.image.load('bearthA.png').convert_alpha()
    bjupiter = pygame.image.load('bjupiter.png').convert_alpha()
    bjupiterA = pygame.image.load('bjupiterA.png').convert_alpha()
    satmanA = pygame.image.load('satmanAT.png').convert_alpha()
    background = sunpic2
    background = background.convert_alpha(background)
    satmanR = satman.get_rect()
    satmanAR = satmanA.get_rect()
    pygame.mixer.init()
    whoosh = pygame.mixer.Sound('whoosh.wav')
    beep = pygame.mixer.Sound('beep2.wav')
    scan = pygame.mixer.Sound('scansound.wav')
    crash = pygame.mixer.Sound('crash.wav')
    launch = pygame.mixer.Sound('launch.wav')
    thrust = pygame.mixer.Sound('truster.wav')
    empty = pygame.mixer.Sound('empty.wav')
    warning = pygame.mixer.Sound('warning.wav')
    channel4 = pygame.mixer.Channel(4)
    channel5 = pygame.mixer.Channel(5)
    thrust.set_volume(0.3)
    empty.set_volume(0.2)
    warning.set_volume(1)
    # soundtrack = pygame.mixer.music.load('song11.ogg')
    newbutton = pygame.image.load('newbutton.png').convert_alpha()
    #Let's randomly choose a song.
    check_if_song_finished()
    # pygame.mixer.music.play()
    pygame.display.update()


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height()), SRCALPHA).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


#Eventhandling, and a whole lot of it
def eventhandler(playing):
    global shazbot, drawingbodies, bodiesdrawn, bodycenters, gameframerate, yvelocity, xvelocity, fuel, blackholedrawing, blackholebodyiesdrawn, update2, bodycenters2
    for e in pygame.event.get():
        if (e.type == QUIT) or (e.type == KEYUP and e.key == K_ESCAPE):
            if playing:
                endgame()
            pygame.display.quit()
            shazbot = 1
            break
        elif e.type == KEYDOWN:
            if playing:
                if e.key == K_EQUALS or e.key == K_PLUS:
                    gameframerate *= 1.1
                    pygame.time.set_timer(USEREVENT + 5, 500)
                elif e.key == K_MINUS or e.key == K_UNDERSCORE:
                    if gameframerate >= 50:
                        gameframerate *= 0.9
                        pygame.time.set_timer(USEREVENT + 6, 500)
        elif e.type == USEREVENT + 5:
            pygame.time.set_timer(USEREVENT + 5, repeatrate * 4)
            gameframerate *= 1.1
        elif e.type == USEREVENT + 6:
            if gameframerate >= 50:
                pygame.time.set_timer(USEREVENT + 6, repeatrate * 4)
                gameframerate *= 0.9
        elif e.type == KEYUP:
            if e.key == K_EQUALS or e.key == K_PLUS:
                pygame.time.set_timer(USEREVENT + 5, 0)
            elif e.key == K_MINUS or e.key == K_UNDERSCORE:
                pygame.time.set_timer(USEREVENT + 6, 0)
            elif e.key == K_q and not playing and not bodiesdrawn:
                screen.blit(background, (0, 0))
                pygame.display.update()
                blackholedrawing = 0
                mainmenu()
            elif e.key == K_r and not playing and not bodiesdrawn:
                screen.blit(background, (0, 0))
                pygame.display.update()
                blackholebodyiesdrawn = 0
                blackholedrawing = 0
                update = []
                update2 = []
                for x, y in bodycenters:
                    update.append(drawonebody((x, y), r, gasplanet))
                bodiesdrawn = 1
                pygame.display.update(update)
            elif e.key == K_SPACE and not playing and not bodiesdrawn:
                screen.blit(background, (0, 0))
                pygame.display.update()
                blackholedrawing = 0
                blackholebodyiesdrawn = 0
                bodycenters = []
                bodycenters2 = []
                drawbodies()
            elif e.key == K_RETURN and not playing and bodiesdrawn:
                screen.blit(background, (0, 0))
                pygame.display.update()
                blackholedrawing = 0
                blackholebodyiesdrawn = 0
                bodycenters = []
                bodycenters2 = []
                drawbodies()
            elif e.key == K_SPACE and not playing and bodiesdrawn:
                playing = 1
                drawingbodies = 0
                blackholedrawing = 0
                blackholebodyiesdrawn = 0
                fireprobe()
            elif e.key == K_q and playing:
                playing = 0
                bodiesdrawn = 0
                blackholedrawing = 0
                endgame(True)
            elif e.key == K_UP and fuel > 0 and playing:
                yvelocity -= 1.5
                fuel -= 1
                thrust.play()
            elif e.key == K_DOWN and fuel > 0 and playing:
                yvelocity += 1.5
                fuel -= 1
                thrust.play()
            elif e.key == K_RIGHT and fuel > 0 and playing:
                xvelocity += 1.5
                fuel -= 1
                thrust.play()
            elif e.key == K_LEFT and fuel > 0 and playing:
                xvelocity -= 1.5
                fuel -= 1
                thrust.play()
            elif e.key == K_UP or e.key == K_DOWN or e.key == K_RIGHT or e.key == K_LEFT and fuel <= 0 and playing:
                empty.set_volume(0.2)
                empty.play()
    return playing


#This is the function called to determine the location, mass, size, and draw the planets onto the screen
def drawbodies():
    global bodycenters, bodiesdrawn, drawingbodies, massofbodies, r, ranx, rany
    drawingbodies = 1
    screen.blit(background, (0, 0))
    pygame.display.update()
    for counter in range(numberofbodies):
        correct = 0
        while not correct:
            ranx = randrange(100, screenx - 200, 100)
            rany = randrange(100, screeny - 100, 100)
            if not (ranx >= (screenx - 75) and rany <= 75) and not (ranx != ranx and rany != rany) in bodycenters:
                correct = 1
            massofbodies = choice([20, 25, 50])
            if massofbodies == 20:
                r = 30
            if massofbodies == 25:
                r = 30
            if massofbodies == 50:
                r = 33
        bodycenters.append((int(ranx), int(rany)))
        for xx in range(r * 2 + 1):
            if massofbodies == 20:
                blit_alpha(screen, plutoA, (int(ranx - 42), int(rany - 42)), 10)
                screen.blit(pluto, (int(ranx - 29), int(rany - 30)))
            if massofbodies == 25:
                blit_alpha(screen, marsA, (int(ranx - 42), int(rany - 42)), 10)
                screen.blit(mars, (int(ranx - 29), int(rany - 30)))
            if massofbodies == 50:
                blit_alpha(screen, jupiterA, (int(ranx - 40), int(rany - 42)), 10)
                screen.blit(jupiter, (int(ranx - 33), int(rany - 33)))
        update.append((ranx - r, rany - r, ranx + r, rany + r))
    pygame.display.update()
    bodiesdrawn = 1


def blackholebody():
    global blackmass, blackholedrawing, blackholebodyiesdrawn, r2, ranx, rany
    blackholedrawing = 1
    for counter in range(blackholebodyies):
        correct = 0
        while not correct:
            ranx = randint(275, screenx - 75)
            rany = randint(175, screeny - 75)
            if not (ranx >= (screenx - 100) and rany <= 100):
                correct = 1
            blackmass = 10000
            if blackmass == 10000:
                r2 = 95
        bodycenters2.append((int(ranx), int(rany)))
        for xx in range(r2 * 2 + 1):
            if blackmass == 10000:
                screen.blit(blackhole, (int(ranx - 96), int(rany - 96)))
        update2.append((ranx - r2, rany - r2, ranx + r2, rany + r2))
    pygame.display.update()
    blackholebodyiesdrawn = 1
    whoosh.play()


#Passed to redraw the planets onto the screen when the game is done and the player hits 'r' - needs to be fixed
def drawonebody(loc, radius, colour):
    xoff, yoff = loc
    for counter in range(radius * 2 + 1):
        x = -radius + counter + xoff
        y = sqrt(radius ** 2 - (-radius + counter) ** 2)
        pygame.draw.line(screen, colour, (x, y + yoff), (x, -y + yoff))
    update = (xoff - r, yoff - r, xoff + r, yoff + r)
    return update


#Draws what you see in the main menu
def drawmainmenu(font, fontemphasis):
    menurects.append(screen.blit(background, (0, 0)))
    font2 = pygame.font.SysFont('arial', 100)
    height = fontemphasis.get_height()
    xoffset = screenx / 2 - 470
    buttononetext1 = 'If you wish to play a '
    buttononeemphasis = 'S'
    buttononetext2 = 'tandard game, press '
    buttontwotext1 = 'If you wish to '
    buttontwoemphasis = 'Q'
    buttontwotext2 = ' uit press '
    title = 'SALVARE'
    b1t1w, ignore = font.size(buttononetext1)
    b1ew, ignore = fontemphasis.size(buttononeemphasis)
    b1t2w, ignore = font.size(buttononetext2)
    b2t1w, ignore = font.size(buttontwotext1)
    b2ew, ignore = fontemphasis.size(buttontwoemphasis)
    b2t2w, ignore = font.size(buttontwotext2)
    menurects.append(blit_alpha(screen, bjupiterA, (-87, -70), 128))
    menurects.append(screen.blit(bjupiter, (-70, -50)))
    menurects.append(blit_alpha(screen, marsA, (-17, 845), 128))
    menurects.append(screen.blit(mars, (-5, 860)))
    menurects.append(blit_alpha(screen, plutoA, (338, 738), 128))
    menurects.append(screen.blit(pluto, (350, 750)))

    menurects.append(screen.blit(newbutton, (200, 50)))
    menurects.append(screen.blit(newbutton, (200, 130)))
    menurects.append(blit_alpha(screen, bearthA, (820, -290), 128))
    menurects.append(screen.blit(bearth, (850, -250)))

    menurects.append(screen.blit(font2.render(title, 1, red), (550, 800)))
    menurects.append(screen.blit(font.render(buttononetext1, 1, white), (xoffset, 50 + (70 - height) / 2)))
    menurects.append(
        screen.blit(fontemphasis.render(buttononeemphasis, 1, red), (xoffset + b1t1w, 50 + (70 - height) / 2)))
    menurects.append(
        screen.blit(font.render(buttononetext2, 1, white), (xoffset + b1t1w + b1ew, 50 + (70 - height) / 2)))
    menurects.append(screen.blit(fontemphasis.render(buttononeemphasis, 1, red),
                                 (xoffset + b1t1w + b1ew + b1t2w, 50 + (70 - height) / 2)))

    menurects.append(screen.blit(font.render(buttontwotext1, 1, white), (xoffset, 130 + (70 - height) / 2)))
    menurects.append(
        screen.blit(fontemphasis.render(buttontwoemphasis, 1, red), (xoffset + b2t1w, 130 + (70 - height) / 2)))
    menurects.append(
        screen.blit(font.render(buttontwotext2, 1, white), (xoffset + b2t1w + b2ew, 130 + (70 - height) / 2)))
    menurects.append(screen.blit(fontemphasis.render(buttontwoemphasis, 1, red),
                                 (xoffset + b2t1w + b2ew + b2t2w, 130 + (70 - height) / 2)))
    clock.tick(30)


def drawmainmenu2(font, fontemphasis, xm, ym):
    font2 = pygame.font.SysFont('arial', 100)
    height = fontemphasis.get_height()
    xoffset = screenx / 2 - 470
    buttononetext1 = 'If you wish to play a '
    buttononeemphasis = 'S'
    buttononetext2 = 'tandard game, press '
    buttontwotext1 = 'If you wish to '
    buttontwoemphasis = 'Q'
    buttontwotext2 = ' uit press '
    title = 'SALVARE'
    b1t1w, ignore = font.size(buttononetext1)
    b1ew, ignore = fontemphasis.size(buttononeemphasis)
    b1t2w, ignore = font.size(buttononetext2)
    b2t1w, ignore = font.size(buttontwotext1)
    b2ew, ignore = fontemphasis.size(buttontwoemphasis)
    b2t2w, ignore = font.size(buttontwotext2)

    menurects.append(screen5.blit(background, (-int(xm), -int(ym))))
    menurects.append(screen5.blit(satman, (6, 4)))
    menurects.append(screen.blit(screen5, (int(xm), int(ym))))

    menurects.append(screen.blit(newbutton, (200, 50)))
    menurects.append(screen.blit(newbutton, (200, 130)))

    menurects.append(screen.blit(font2.render(title, 1, red), (550, 800)))
    menurects.append(screen.blit(font.render(buttononetext1, 1, white), (xoffset, 50 + (70 - height) / 2)))
    menurects.append(
        screen.blit(fontemphasis.render(buttononeemphasis, 1, red), (xoffset + b1t1w, 50 + (70 - height) / 2)))
    menurects.append(
        screen.blit(font.render(buttononetext2, 1, white), (xoffset + b1t1w + b1ew, 50 + (70 - height) / 2)))
    menurects.append(screen.blit(fontemphasis.render(buttononeemphasis, 1, red),
                                 (xoffset + b1t1w + b1ew + b1t2w, 50 + (70 - height) / 2)))

    menurects.append(screen.blit(font.render(buttontwotext1, 1, white), (xoffset, 130 + (70 - height) / 2)))
    menurects.append(
        screen.blit(fontemphasis.render(buttontwoemphasis, 1, red), (xoffset + b2t1w, 130 + (70 - height) / 2)))
    menurects.append(
        screen.blit(font.render(buttontwotext2, 1, white), (xoffset + b2t1w + b2ew, 130 + (70 - height) / 2)))
    menurects.append(screen.blit(fontemphasis.render(buttontwoemphasis, 1, red),
                                 (xoffset + b2t1w + b2ew + b2t2w, 130 + (70 - height) / 2)))
    clock.tick(30)

#The Eventhandler that is used while the player is at the MainMenu
def menuevents(e):
    global shazbot, chosen
    chosen = 0
    key = None
    if e.type == QUIT or (e.type == KEYUP and (e.key == K_ESCAPE or e.key == K_q)):
        shazbot = 1
        chosen = 1
        key = 'q'
        pygame.quit()
    elif e.type == KEYUP:
        if e.key == K_s:
            chosen = 1
            key = 's'
    return chosen, key


#The main menu
def mainmenu():
    global randombodies, numberofbodies, key
    step = 0
    AMPLITUDE = 6
    pygame.mixer.music.set_volume(0.2)
    font = pygame.font.SysFont('arial', 18)
    fontemphasis = pygame.font.SysFont('arial', 20)
    drawmainmenu(font, fontemphasis)
    chosen = 0
    xm = 190
    ym = 480
    pygame.display.update(menurects)
    del menurects[:]
    while not chosen:
        xm += cos(step) * AMPLITUDE
        ym += -1 * sin(step) * AMPLITUDE
        step += 0.02
        step %= 2 * pi
        for e in pygame.event.get():
            chosen, key = menuevents(e)
        drawmainmenu2(font, fontemphasis, xm, ym)
        pygame.display.update(menurects)
        del menurects[:]
    if key == 's':
        numberofbodies = 3
        screen.fill(black)
        #pygame.display.update()
        pygame.mixer.music.set_volume(1.0)
        font = pygame.font.SysFont('arial', 22)
        font1 = pygame.font.SysFont('arial', 20)
        font2 = pygame.font.SysFont('arial', 40)
        font3 = pygame.font.SysFont('arial', 16)
        size = font.get_linesize()
        line1 = "It is the year 2240. Earth's rotation has nearly come to a halt, and several unexplainable changes have occurred in our solar system (e.g., planets have been known to move spontaneously)."
        line2 = "Disasters are appearing all over the world. Birds are behaving erratically,the climate has shifted, and volcanic activity has increased significantly."
        line3 = "Human existence as we know it has ceased. People are living in bomb shelters, mass suicides are occurring, people are calling it the end of the world."
        line4 = "Earth's last chance to survive lies with you, a seasoned pilot who has been on seven space missions to date."

        line5 = "Here is your mission..."

        line6 = "Given the widespread devastation,looting, and depletion of resources, the United States government used the last remaining materials to develop a specialized probe."
        line7 = "This probe has one mission:search for the rare element Pythonium. Several years ago astro physicist Hans Leikemburg identified this new element in the atmosphere"
        line8 = "of foreign celestial bodies, and believes that it has the power to fuel the massive thrusters fixed to undisclosed locations on Earth. Should these thrusters be activated"
        line9 = "for long enough, it is possible that the speed of Earth's rotation can be restored. Be careful, don't let the probe venture out too far or you might lose it."

        line10 = "You will be stationed at NASA's Houston, Texas naval base. There, you will be responsible for piloting the probe across the solar system to find any trace of Pythonium."
        line11 = "It is your mission to orbit available planets to search for this precious material; however, be careful. If you get too close, you may run out of fuel, crash into another planet, or worse..."

        line12 = "To begin your piloted mission, press the SPACEBAR. A blank screen with three randomly placed planets will appear. You have the opportunity to change the configuration of these planets by pressing ENTER."
        line13 = "Once you are ready to begin, press the SPACEBAR. You will notice Earth in the top right corner, the area in which the probe is launched."
        line14 = "To direct the probe towards the planets and determine initial velocity of the probe, use the ARROW KEYS. Press the SPACEBAR once you are ready to release the probe."
        line15 = "Notably, to aim the probe during flight, you can use the ARROW KEYS. Be careful though, aiming the probe uses fuel, and there is only a limited reserve on board. Good luck, and god speed..."
        blit_alpha(screen, jupiterA, (142, 642), 128)
        screen.blit(jupiter, (150, 650))
        line16 = "= Heavy weight"
        blit_alpha(screen, marsA, (537, 637), 128)
        screen.blit(mars, (550, 650))
        line17 = "= Medium weight"
        blit_alpha(screen, plutoA, (937, 637), 128)
        screen.blit(pluto, (950, 650))
        line18 = "= Low weight"
        line19 = "?"
        line20 = "= Mass unkown..."
        line21 = "These are the possible celestrial bodies you may encounter..."
        screen.blit(font.render(line21, 0, white, black), (450, 575))
        screen.blit(font2.render(line19, 0, verylightblue, black), (620, 750))
        screen.blit(font1.render(line20, 0, white, black), (645, 765))
        screen.blit(font1.render(line16, 0, white, black), (228, 665))
        screen.blit(font1.render(line17, 0, white, black), (624, 665))
        screen.blit(font1.render(line18, 0, white, black), (1024, 665))
        screen.blit(font3.render(line1, 0, white, black), (20, 50 + size * 1))
        screen.blit(font3.render(line2, 0, white, black), (20, 50 + size * 2))
        screen.blit(font3.render(line3, 0, white, black), (20, 50 + size * 3))
        screen.blit(font3.render(line4, 0, white, black), (20, 50 + size * 4))
        screen.blit(font3.render(line5, 0, white, black), (20, 50 + size * 6))
        screen.blit(font3.render(line6, 0, white, black), (20, 50 + size * 8))
        screen.blit(font3.render(line7, 0, white, black), (20, 50 + size * 9))
        screen.blit(font3.render(line8, 0, white, black), (20, 50 + size * 10))
        screen.blit(font3.render(line9, 0, white, black), (20, 50 + size * 11))
        screen.blit(font3.render(line10, 0, white, black), (20, 50 + size * 13))
        screen.blit(font3.render(line11, 0, white, black), (20, 50 + size * 14))
        screen.blit(font3.render(line12, 0, white, black), (20, 50 + size * 15))
        screen.blit(font3.render(line13, 0, white, black), (20, 50 + size * 16))
        screen.blit(font3.render(line14, 0, white, black), (20, 50 + size * 17))
        screen.blit(font3.render(line15, 0, white, black), (20, 50 + size * 18))
        pygame.display.update()

#Used to determine if the probe has crashed into the planets
def checkforcollision():
    global score, death, close
    close = 0
    collision = 0
    if blackholebodyiesdrawn:
        for bodyx, bodyy in bodycenters2:
            distance = sqrt(abs(probex - bodyx) ** 2 + abs(probey - bodyy) ** 2)
            score += 4000 / distance ** 2
            if distance <= r2 + 7:
                scan.stop()
                whoosh.stop()
                crash.play()
                collision = 1
    else:
        for bodyx, bodyy in bodycenters:
            distance = sqrt(abs(probex - bodyx) ** 2 + abs(probey - bodyy) ** 2)
            score += 1000 / distance ** 2
            if distance <= r + 100:
                close = 1
            if distance <= r + 6:
                scan.stop()
                crash.play()
                collision = 1
            if score > 750 and not blackholedrawing:
                death = randint(1, 5000)
                if death == 666:
                    blackholebody()
    return collision

#Where physics and magic play...
def calculatenewvelocity():
    global xvelocity, yvelocity
    if randombodies:
        if blackholebodyiesdrawn:
            for x, y in bodycenters2:
                gforce = numer2 / (abs(x - probex) ** 2.0 + abs(y - probey) ** 2.0)
                angle = atan2(x - probex, y - probey)
                if angle <= (-pi / 2):
                    yvelocity -= ((-angle - pi / 2) / (pi / 2) * gforce) + 1
                    xvelocity -= ((pi + angle) / (pi / 2) * gforce) + 1
                elif angle <= 0:
                    yvelocity += ((pi / 2 + angle) / (pi / 2) * gforce) + 1
                    xvelocity -= ((-angle) / (pi / 2) * gforce) + 1
                elif angle <= (pi / 2):
                    yvelocity += ((pi / 2 - angle) / (pi / 2) * gforce) + 1
                    xvelocity += (angle / (pi / 2) * gforce) + 1
                else:
                    yvelocity -= ((angle - pi / 2) / (pi / 2) * gforce) + 1
                    xvelocity += ((pi - angle) / (pi / 2) * gforce) + 1
        else:
            for x, y in bodycenters:
                gforce = numer / (abs(x - probex) ** 2.0 + abs(y - probey) ** 2.0)
                angle = atan2(x - probex, y - probey)
                if angle <= (-pi / 2):
                    yvelocity -= ((-angle - pi / 2) / (pi / 2) * gforce) * 2
                    xvelocity -= ((pi + angle) / (pi / 2) * gforce) * 2
                elif angle <= 0:
                    yvelocity += ((pi / 2 + angle) / (pi / 2) * gforce) * 2
                    xvelocity -= ((-angle) / (pi / 2) * gforce) * 2
                elif angle <= (pi / 2):
                    yvelocity += ((pi / 2 - angle) / (pi / 2) * gforce) * 2
                    xvelocity += (angle / (pi / 2) * gforce) * 2
                else:
                    yvelocity -= ((angle - pi / 2) / (pi / 2) * gforce) * 2
                    xvelocity += ((pi - angle) / (pi / 2) * gforce) * 2


#This is where the calculations come to determine how the probe moves baised on the simulated gratitational pull from the drawn planets
def drawprobepath():
    global probex, probey, oldx, oldy, frame_count
    xv = abs(xvelocity)
    yv = abs(yvelocity)
    oldx = probex
    oldy = probey
    if xv > 8 or yv > 8:
        probex += xvelocity / 5
        probey += yvelocity / 5
    elif xv > 7 or yv > 7:
        probex += xvelocity / 4.5
        probey += yvelocity / 4.5
    elif xv > 6 or yv > 6:
        probex += xvelocity / 4
        probey += yvelocity / 4
    elif xv > 5 or yv > 5:
        probex += xvelocity / 3.5
        probey += yvelocity / 3.5
    elif xv > 4 or yv > 4:
        probex += xvelocity / 3
        probey += yvelocity / 3
    elif xv > 3 or yv > 3:
        probex += xvelocity / 2.5
        probey += yvelocity / 2.5
    elif xv > 2 or yv > 2:
        probex += xvelocity / 1.9
        probey += yvelocity / 1.9
    elif xv > 1 or yv > 1:
        probex += xvelocity / 1.5
        probey += yvelocity / 1.5
    else:
        probex += xvelocity
        probey += yvelocity
    if 1440 >= probex >= 0 and 900 >= probey >= 0:
        channel5.stop()
        masterrects.append(screen.blit(background, (1300, 680), pygame.Rect(1300, 680, 200, 50)))
        frame_count = 0
    if close:
        scan.play()
        #masterrects.append(screen.blit(dirtyrect2, (int(oldx-6),int(oldy-6))))
        masterrects.append(
            screen.blit(background, (int(oldx - 6), int(oldy - 6)), pygame.Rect(int(oldx - 6), int(oldy - 6), 16, 16)))
        masterrects.append(screen.blit(satmanA, (int(probex - 6), int(probey - 6))))
    if not close:
        scan.stop()
        #masterrects.append(screen.blit(dirtyrect, (int(oldx-3),int(oldy-3))))
        masterrects.append(
            screen.blit(background, (int(oldx - 3), int(oldy - 3)), pygame.Rect(int(oldx - 3), int(oldy - 3), 10, 10)))
        masterrects.append(screen.blit(satman, (int(probex - 3), int(probey - 3))))

        #Draws the 'gun' that is used to launch the probe


def drawbarrel(d):
    masterrects.append(screen.blit(background, (1408, 0), pygame.Rect(1408, 0, 50, 40)))
    masterrects.append(pygame.draw.aaline(screen, white, (screenx - 2, 1),
                                          (((screenx - 22) + (100.0 - d) ** 2 / 500) - 10, (21 - d ** 2 / 500) + 10)))
    masterrects.append(screen.blit(earth, (int(screenx - 14), int(-26))))

#Draws the power text and bar onto the screen
def drawpower(power):
    font1 = pygame.font.SysFont('arial', 16)
    powertext = 'Power = '
    width, ignore = font1.size(powertext)
    masterrects.append(screen.blit(background, (1340, 200), pygame.Rect(1340, 200, 100, 200)))
    masterrects.append(pygame.draw.rect(screen, white, (screenx - 20, 205, 20, 180), 1))
    masterrects.append(pygame.draw.rect(screen, red, (screenx - 19, 384 - power * 3.525, 18, (power * 3.525))))
    masterrects.append(screen.blit(font1.render(powertext, 1, white), (screenx - 100, 370)))
    masterrects.append(screen.blit(font1.render(str(power), 1, verylightblue), (screenx - 103 + width, 370)))

#Just wait a minute
def waitforit():
    return pygame.event.wait()

#This is the eventhandler while the player is aiming the gun but hasn't fired it yet
def checkingkeys(e, power, d, fired):
    global shazbot
    if (e.type == QUIT) or (e.type == KEYUP and e.key == K_ESCAPE):
        shazbot = 1
        fired = 1
        pygame.mixer.music.stop()
    elif e.type == KEYDOWN:
        if e.key == K_RIGHT:
            if d > 0:
                d -= 1
                pygame.time.set_timer(USEREVENT + 1, 500)
        elif e.key == K_LEFT:
            if d < 100:
                d += 1
                pygame.time.set_timer(USEREVENT + 2, 500)
        elif e.key == K_UP:
            if power < 50:
                power += 1
                pygame.time.set_timer(USEREVENT + 3, 500)
        elif e.key == K_DOWN:
            if power > 1:
                power -= 1
                pygame.time.set_timer(USEREVENT + 4, 500)
    elif e.type == KEYUP:
        if e.key == K_RIGHT:
            pygame.time.set_timer(USEREVENT + 1, 0)
        elif e.key == K_LEFT:
            pygame.time.set_timer(USEREVENT + 2, 0)
        elif e.key == K_UP:
            pygame.time.set_timer(USEREVENT + 3, 0)
        elif e.key == K_DOWN:
            pygame.time.set_timer(USEREVENT + 4, 0)
        elif e.key == K_SPACE:
            fired = 1
            launch.play()
            beep.set_volume(0.2)
            beep.play(loops=-1, fade_ms=1000)
    elif e.type == USEREVENT + 1:
        pygame.time.set_timer(USEREVENT + 1, repeatrate)
        if d > 0:
            d -= 1
    elif e.type == USEREVENT + 2:
        pygame.time.set_timer(USEREVENT + 2, repeatrate)
        if d < 100:
            d += 1
    elif e.type == USEREVENT + 3:
        pygame.time.set_timer(USEREVENT + 3, repeatrate * 2)
        if power < 50:
            power += 1
    elif e.type == USEREVENT + 4:
        pygame.time.set_timer(USEREVENT + 4, repeatrate * 2)
        if power > 1:
            power -= 1
    return power, d, fired

#This controls the function for aiming/firing the probe
def fireprobe():
    global probex, probey, xvelocity, yvelocity, d, shazbot, power
    d = 50.0
    power = 25
    drawbarrel(d)
    drawpower(power)
    fired = 0
    while not fired:
        for e in pygame.event.get():
            power, d, fired = checkingkeys(e, power, d, fired)
        drawbarrel(d)
        drawpower(power)
        pygame.display.update()
    probex = ((screenx - 22) + (100.0 - d) ** 2 / 500) - 10
    probey = (21 - d ** 2 / 500) + 10
    xvelocity = (-((d / 100) * power * powermultiplier)) * 3
    yvelocity = ((((100 - d) / 100) * power * powermultiplier)) * 3
    printlabels()
    drawprobepath()

#Called once the player ends a game
def endgame(suicide=0):
    global score, fuel
    beep.stop()
    warning.stop()
    scan.stop()
    font = pygame.font.SysFont('arial', 32)
    font2 = pygame.font.SysFont('arial', 48)
    size = font.get_linesize()
    firstline = 'Probe no longer transmitting.'
    if suicide:
        firstline = 'Probe self-destructs.'
    secondline = 'Your final score was: '
    secondline2 = str(int(score))
    thirdline = 'Hit Q to return to the main menu.'
    fourthline = '   Or [SPACE] to play again.'
    secondlinewidth, ignore = font.size(secondline)
    screen.blit(font.render(firstline, 1, white), (screenx / 2 - 250, screeny / 2 - size * 2))
    screen.blit(font.render(secondline, 1, white), (screenx / 2 - 250, screeny / 2))
    screen.blit(font2.render(secondline2, 1, red),
                (screenx / 2 - 250 + secondlinewidth, screeny / 2 - font2.get_linesize() / 4))
    screen.blit(font.render(thirdline, 1, white), (screenx / 2 - 250, screeny / 2 + size * 2))
    screen.blit(font.render(fourthline, 1, white), (screenx / 2 - 250, screeny / 2 + size * 3))
    pygame.display.update()
    score = 0
    fuel = 500

#Prints the score type onto the screen while the probe is flying around
def printvalues():
    xoffset = screenx - 100
    yoffset = 380
    font = pygame.font.SysFont('arial', 16)
    size = font.get_linesize() + 5
    scoretext = str(int(score))
    currentxvelocity = str(round(xvelocity, 2))
    currentyvelocity = str(round(yvelocity, 2))
    currentx = str(int(probex))
    currenty = str(int(probey))
    currentframes = str(int(gameframerate))
    currentpyframes = str(int(clock.get_fps()))
    currentfuel = str(int(fuel))
    masterrects.append(screen.blit(background, (1340, 405), pygame.Rect(1340, 405, 100, 195)))
    masterrects.append(screen.blit(font.render(scoretext, 0, white), ((xoffset + 15) + scorelength, yoffset + size)))
    masterrects.append(
        screen.blit(font.render(currentxvelocity, 0, white), ((xoffset + 5) + xvelocitylength, yoffset + size * 2)))
    masterrects.append(
        screen.blit(font.render(currentyvelocity, 0, white), ((xoffset + 5) + yvelocitylength, yoffset + size * 3)))
    masterrects.append(screen.blit(font.render(currentx, 0, white), ((xoffset + 5) + xlength, yoffset + size * 4)))
    masterrects.append(screen.blit(font.render(currenty, 0, white), ((xoffset + 5) + ylength, yoffset + size * 5)))
    masterrects.append(
        screen.blit(font.render(currentframes, 0, white), ((xoffset + 5) + frameslength, yoffset + size * 6)))
    masterrects.append(
        screen.blit(font.render(currentpyframes, 0, white), ((xoffset + 5) + pyframeslength, yoffset + size * 7)))
    masterrects.append(
        screen.blit(font.render(currentfuel, 0, white), ((xoffset + 5) + fuellength, yoffset + size * 8)))

#Prints the labels onto the screen for the score type information while the probe is launched
def printlabels():
    global scorelength, xvelocitylength, yvelocitylength, xlength, ylength, frameslength, pyframeslength, fuellength
    font = pygame.font.SysFont('arial', 14)
    font2 = pygame.font.SysFont('arial', 16)
    size = font2.get_linesize() + 5
    scoretext = 'Score '
    currentxvelocity = 'X Speed '
    currentyvelocity = 'Y Speed '
    currentx = 'Probe X '
    currenty = 'Probe Y '
    currentframes = 'FPS     ='
    currentpyframes = 'PyFPS ='
    currentfuel = 'Fuel     ='
    scorelength, ignore = font.size(scoretext)
    xvelocitylength, ignore = font.size(currentxvelocity)
    yvelocitylength, ignore = font.size(currentyvelocity)
    xlength, ignore = font.size(currentx)
    ylength, ignore = font.size(currenty)
    frameslength, ignore = font.size(currentframes)
    pyframeslength, ignore = font.size(currentpyframes)
    fuellength, ignore = font.size(currentfuel)
    masterrects.append(screen.blit(font.render(scoretext, 0, white), (screenx - 100, 380 + size)))
    masterrects.append(screen.blit(font.render(currentxvelocity, 0, white), (screenx - 100, 380 + size * 2)))
    masterrects.append(screen.blit(font.render(currentyvelocity, 0, white), (screenx - 100, 380 + size * 3)))
    masterrects.append(screen.blit(font.render(currentx, 0, white), (screenx - 100, 380 + size * 4)))
    masterrects.append(screen.blit(font.render(currenty, 0, white), (screenx - 100, 380 + size * 5)))
    masterrects.append(screen.blit(font.render(currentframes, 0, white), (screenx - 100, 380 + size * 6)))
    masterrects.append(screen.blit(font.render(currentpyframes, 0, white), (screenx - 100, 380 + size * 7)))
    masterrects.append(screen.blit(font.render(currentfuel, 0, white), (screenx - 100, 380 + size * 8)))


#This is the minimap that draws on the lower left and shows the direction of the probe
def printarrow():
    arrowtext = 'DIRECTION'
    font = pygame.font.SysFont('arial', 20)
    masterrects.append(screen.blit(font.render(arrowtext, 0, white), (1305, 730)))
    masterrects.append(screen6.blit(background, (0, 0), pygame.Rect(1290, 750, 150, 150)))
    masterrects.append(pygame.draw.line(screen6, white, (1, 1), (1, 149), 2))
    masterrects.append(pygame.draw.line(screen6, white, (1, 1), (149, 1), 2))
    masterrects.append(pygame.draw.line(screen6, white, (148, 1), (148, 148), 2))
    masterrects.append(pygame.draw.line(screen6, white, (148, 148), (1, 148), 2))
    masterrects.append(pygame.draw.aaline(screen6, verylightblue, (75, 75), (probex - 1290, probey - 750)))
    masterrects.append(screen.blit(screen6, (1290, 750)))


def countdown():
    global frame_count, bodiesdrawn, total_seconds
    collision = 0
    font = pygame.font.SysFont('arial', 18)
    font2 = pygame.font.SysFont('arial', 16)
    if probex >= 1440 or probex <= 0 or probey > 900 or probey <= 0:
        if not channel5.get_busy():
            channel5.play(warning, -1)
        total_seconds = start_time - (frame_count // gameframerate)
        if total_seconds <= 0:
            collision = 1
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)
        output_string2 = 'Signal out of range!'
        text = font.render(output_string, True, white)
        text2 = font2.render(output_string2, True, white)
        masterrects.append(screen.blit(background, (1300, 680), pygame.Rect(1300, 680, 200, 50)))
        masterrects.append(screen.blit(text, [1300, 700]))
        masterrects.append(screen.blit(text2, [1300, 680]))
        frame_count += 1
    return collision


#Handles the whole ordeal about the probe crashing
def collisioncourse(playing):
    global bodiesdrawn
    if checkforcollision():
        endgame()
        bodiesdrawn = 0
        playing = 0
    if countdown():
        endgame()
        bodiesdrawn = 0
        playing = 0
    return playing

#Where we check if the music is still playing
def check_if_song_finished():
    if pygame.mixer.music.get_busy():
        pass
    else:
        randSongChoice = randrange(1,5,1)
        pygame.mixer.music.unload()
        match randSongChoice:
            case 1:
                song1 = pygame.mixer.music.load('song11.ogg')
            case 2:
                song2 = pygame.mixer.music.load('Song1.ogg')
            case 3:
                song3 = pygame.mixer.music.load('Song2.ogg')
            case 4:
                song4 = pygame.mixer.music.load('Song3.ogg')
            case 5:
                song5 = pygame.mixer.music.load('Song4.ogg')
        pygame.mixer.music.play()

#Where the magic happens
def main():
    global massofbodies
    shazbot = 0
    initiatepygame()
    playing = 0
    mainmenu()
    #counter = 0
    counter2 = 0
    while not shazbot:
        playing = eventhandler(playing)
        if playing:
            #screen.blit(background, (0,0))
            #counter += textupdate.tick()
            #counter = 0
            printvalues()
            printlabels()
            drawpower(power)
            drawbarrel(d)
            printarrow()
            #if counter >= 150:
            #counter = 0
            #printvalues()
            #printlabels()
            #drawpower(power)
            #drawbarrel(d)
            #printarrow()
            if counter2 >= 10:
                clock.tick(int(gameframerate))
            counter2 += 1
            drawprobepath()
            playing = collisioncourse(playing)
            calculatenewvelocity()
            check_if_song_finished()
        else:
            pygame.event.post(waitforit())
            #playing = eventhandler(playing)
        pygame.display.update(masterrects)
        del masterrects[:]
        if shazbot:
            break

#This is a clean way to quit without throwing errors
if __name__ == '__main__':
    main()
    #    try:
    #        main()
    #    except Exception,e:\
    #    tb = sys.exc_info()[2]
    #    pygame.quit()
    #pygame.quit()

    #cProfile.run('main()', 'ProfiledCode')