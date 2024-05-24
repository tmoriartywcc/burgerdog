import pygame, random

#initialize pygame
pygame.init()

#create a display surface
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Burger Dog")

#Set FPS and Clock
FPS = 60
clock = pygame.time.Clock()

#Set Game Values
PLAYER_STARTING_LIVES = 3
PLAYER_NORMAL_VELOCITY = 5
PLAYER_BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL = 100
STARTING_BURGER_VELOCITY = 3
BURGER_ACCELERATION = .25
BUFFER_DISTANCE = 100

score = 0
burger_points = 0
burgers_eaten = 0

player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY

boost_level = STARTING_BOOST_LEVEL
burger_velocity = STARTING_BURGER_VELOCITY


#Set Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (246, 170, 54)

#Set Fonts
font = pygame.font.Font('WashYourHand.ttf', 32)

#Set Text
points_text = font.render('Burger Points: ' + str(burger_points), True, ORANGE)
points_rect = points_text.get_rect()
points_rect.topleft = (10,10)

score_text = font.render('Score: ' + str(score), True, ORANGE)
score_rect = score_text.get_rect()
score_rect.topleft = (10,50)

title_text = font.render('Burger Dog', True, ORANGE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y= 10

eaten_text = font.render('Burgers Eaten: ' + str(burgers_eaten), True, ORANGE)
eaten_rect = eaten_text.get_rect()
eaten_rect.centerx = WINDOW_WIDTH//2
eaten_rect.y = 50

lives_text = font.render('Lives: ' + str(player_lives), True, ORANGE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10,10)

boost_text = font.render('Boost: ' + str(boost_level), True, ORANGE)
boost_rect = boost_text.get_rect()
boost_rect.topright = (WINDOW_WIDTH - 10,50)


game_over_text = font.render('FINAL SCORE: ' + str(score), True, ORANGE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render('Press any key to play again', True, ORANGE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)



#Set Sounds and Music
bark_sound = pygame.mixer.Sound('bark_sound.wav')
miss_sound = pygame.mixer.Sound('miss_sound.wav')
pygame.mixer.music.load('bd_background_music.wav')


#Set Images
player_image_right = pygame.image.load("dog_right.png")
player_image_left = pygame.image.load("dog_left.png")
player_image = player_image_left

player_rect = player_image.get_rect()
player_rect.centerx = WINDOW_WIDTH//2
player_rect.centery = WINDOW_HEIGHT//2



burger_image = pygame.image.load("burger.png")
burger_rect = burger_image.get_rect()
burger_rect.topleft = (random.randint(0, WINDOW_WIDTH-32), -BUFFER_DISTANCE)



#The main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

    #Get a list of all keys currently being pressed down
    #We want continous movement so this will be outside of the game loop
    keys = pygame.key.get_pressed()   
    

    #Move the dog continously
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_rect.left > 0:
        player_rect.x -= player_velocity
        player_image = player_image_left
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_rect.right < WINDOW_WIDTH:
        player_rect.x += player_velocity
        player_image = player_image_right
    if keys[pygame.K_UP] and player_rect.top > 100:
        player_rect.y -= player_velocity
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += player_velocity

    if keys[pygame.K_SPACE] and boost_level > 0:
        player_velocity = PLAYER_BOOST_VELOCITY
        boost_level -= 1
    else:
        player_velocity = PLAYER_NORMAL_VELOCITY


    #Move the burger and update burger points
    burger_rect.y += burger_velocity
    burger_points = int(burger_velocity * (WINDOW_HEIGHT - burger_rect.y + 100))
        
    #player missed the burger
    if burger_rect.y > WINDOW_HEIGHT:
        player_lives -= 1
        miss_sound.play()

        burger_rect.topleft = (random.randint(0, WINDOW_WIDTH-32), -BUFFER_DISTANCE)
        burger_velocity = STARTING_BURGER_VELOCITY

        player_rect.centerx = WINDOW_WIDTH//2
        player_rect.bottom = WINDOW_HEIGHT

        boost_level = STARTING_BOOST_LEVEL

    #Check for collisions
    if player_rect.colliderect(burger_rect):
        score += burger_points
        burgers_eaten += 1
        burger_rect.topleft = (random.randint(0, WINDOW_WIDTH-32), -BUFFER_DISTANCE)
        bark_sound.play()
        burger_velocity += BURGER_ACCELERATION

        boost_level += 50

        if boost_level > STARTING_BOOST_LEVEL:
            boost_level = STARTING_BOOST_LEVEL


    
    #Move the coin
    #if coin_rect.x < 0:
        #player missed coin
    #    player_lives -= 1
    #    miss_sound.play()
        #place coin off the end of the screen again
    #    coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
    #    coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    #else:
    #    coin_rect.x -= coin_velocity
        #move hte coint
    #Check for collison between player and coin
    #if player_rect.colliderect(coin_rect):
    #    score += 1
    #    coin_sound.play()
    #    coin_velocity += COIN_ACCELERATION
    #    coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
    #    coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

    #update HUD
    #score_text = font.render('Score: ' + str(score), True, GREEN, DARKGREEN)
    #lives_text = font.render('Lives: ' + str(player_lives), True, GREEN, DARKGREEN)


    #if player_lives == 0:
    #    display_surface.blit(game_over_text, game_over_rect)
    #    display_surface.blit(continue_text, continue_rect)
    #    pygame.display.update()

        #Pause game until player presses a key, then reset
    #    pygame.mixer.music.stop()
    #    is_paused = True
    #    while is_paused:
    #        for event in pygame.event.get():
                #player wants to play again
    #            if event.type == pygame.KEYDOWN:
    #                score = 0
    #                player_lives = PLAYER_STARTING_LIVES
    #                player_rect.y = WINDOW_HEIGHT // 2
    #                coin_velocity = COIN_STARTING_VELOCITY
    #                pygame.mixer.music.play(-1, 0.0)
    #                is_paused = False
                #player wants to quit
    #            if event.type == pygame.QUIT:
    #                is_paused = False
    #                running = False


    #Fill the display surface to cover old images
    display_surface.fill(BLACK)

    #Draw rectangles to represent rectangles
    #pygame.draw.rect(display_surface, (0,255,0), dragon_rect, 1)
    #pygame.draw.rect(display_surface, (255,0,0), coin_rect, 1)
    
    #Blit the HUD to the screen
    display_surface.blit(points_text, points_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(boost_text, boost_rect)
    display_surface.blit(lives_text, lives_rect)
    pygame.draw.line(display_surface, WHITE, (0,100), (WINDOW_WIDTH, 100), 3)

    
    #Blit (copy) assets to the screen
    display_surface.blit(player_image, player_rect)
    display_surface.blit(burger_image, burger_rect)


    #update display
    pygame.display.update()

    #Tick the clock
    clock.tick(FPS)


#End the game
pygame.quit()