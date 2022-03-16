import pygame
import time
import random

pygame.init()

crash_sound = pygame.mixer.Sound("Crash.wav")
pygame.mixer.music.load("reggae.wav")


# Game dimensions
display_width = 800
display_height = 600

# define colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (220, 0, 0)
lightRed = (255, 100, 0)
block_colour = (120, 250, 250)
green = (0, 200, 0)
lightGreen = (0, 255, 0)

# Set game display
gameDisplay = pygame.display.set_mode((display_width, display_height))

carImg = pygame.image.load('car.png')
carImg = pygame.transform.scale(carImg, (80, 120))
car_width = 80

icon = pygame.image.load("speed.png")

# Game title caption
pygame.display.set_caption('Bizarre Race Car')
pygame.display.set_icon(icon)
# Game clock
clock = pygame.time.Clock()

pause = True


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def things_dodged(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render('Score: ' + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    crash = True
    largeText = pygame.font.Font('Retrow Mentho.ttf', 90)
    textSurf, textRect = text_objects('You Crashed', largeText)
    textRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(textSurf, textRect)

    while crash:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if crash == True:
                        game_loop()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # gameDisplay.fill(white)

        button('Restart', 150, 450, 120, 50, green, lightGreen, game_loop)
        button('Quit', 550, 450, 100, 50, red, lightRed, quitGame)

        pygame.display.update()
        clock.tick(15)


def quitGame():
    pygame.quit()
    quit()


def unPause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def paused():
    pygame.mixer.music.pause()

    largeText = pygame.font.Font('Retrow Mentho.ttf', 90)
    textSurf, textRect = text_objects('Paused', largeText)
    textRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(textSurf, textRect)

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if pause == True:
                        unPause()
                    else:
                        paused()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        button('Continue', 150, 450, 120, 50, green, lightGreen, unPause)
        button('Quit', 550, 450, 100, 50, red, lightRed, quitGame)

        pygame.display.update()
        clock.tick(15)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 25)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)

        largeText = pygame.font.Font('Retrow Mentho.ttf', 90)
        textSurf, textRect = text_objects('Bizarre Race Car', largeText)
        textRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(textSurf, textRect)

        button('GO!', 150, 450, 100, 50, green, lightGreen, game_loop)
        button('Quit', 550, 450, 100, 50, red, lightRed, quitGame)

        pygame.display.update()
        clock.tick(15)


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def game_loop():
    global pause
    pygame.mixer.music.play(-1)
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = 600
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    score = 0
    # Game loop
    gameExit = False
    while not gameExit:

        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_SPACE:
                    pause = True
                    paused()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        # Boundaries
        x += x_change

        gameDisplay.fill(white)
        # things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, block_colour)
        thing_starty += thing_speed

        car(x, y)
        things_dodged(score)

        if x > display_width - car_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width - 100)
            score += 1
            if score % 5 == 0:
                thing_speed += 1

        if y < thing_starty + thing_height:
            # print('y crossover')
            if thing_startx < x < thing_startx + thing_width or thing_startx < x + car_width < thing_startx + thing_width:
                # print('x crossover')
                crash()

        pygame.mixer.music.set_volume(0.5)

        # displays game
        pygame.display.update()
        # update fps
        clock.tick(120)




game_intro()
game_loop()
# quit game
pygame.quit()
quit()
