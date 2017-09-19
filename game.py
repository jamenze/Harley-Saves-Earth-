
# We have access to pygame, because we did:
# $ pip install pygame
# it is NOT part of core. This is a 3rd party module.
import pygame, sys, random, time
from pygame.sprite import Group, groupcollide
global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, topscore

# -----CUSTOM CLASSES HERE-----
from Player import Player
from Bad_guy import Bad_guy
from Bullet import Bullet
from Star import Star


# Setup mixer to avoid sound lag
pygame.mixer.pre_init(44100, -16, 2, 2048) 

# Have to init the pygame object so we can use it
pygame.init()
pygame.font.init()
FPSCLOCK = pygame.time.Clock()


points = 0

font = pygame.font.Font(None, 25) 
font2 = pygame.font.Font(None, 30) # Bigger font than font


font_color = (255,255,255)

# Screen size is a tuple
screen_size = (1000,800)

# Load background image
background_image = pygame.image.load('background.png') 
# Scale background image (if applicable)
background_image = pygame.transform.scale(background_image, (1000, 800)) 



# Create a screen for pygame to use to draw on
screen = pygame.display.set_mode(screen_size)

# Display Game Title:
pygame.display.set_caption("Harley Saves Earth!")

the_player = Player('harley.png',100,100,screen)

# Make a bad_guy
bad_guy = Bad_guy(screen)
# make a group for the bad_guys
bad_guys = Group()
# add our bad_guy to the bad_guys group
bad_guys.add(bad_guy)

# Make a star
the_star = Star(screen)
# Make a group for the stars
stars = Group()
# Add our the_star to the stars group
stars.add(the_star)

# Make a new Group called bullets. Group is a pygame "list"
bullets = Group()

# Make a new Group called players
players = Group()
players.add(the_player)

pygame.mixer.music.load('arcade_music.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)


game_on = True
# Set up the main game loop
while game_on: #will run forever (until break)
	# Loop through all the pygame events.
	# This is pygames escape hatch. (Quit)


	for event in pygame.event.get():
		# print event
		if event.type == pygame.QUIT:
			game_on = False
		elif event.type == pygame.KEYDOWN:
			print event.key
			# print "User pressed a key!!!"
			if event.key == 273:
				# user pressed up!
				# the_player.y -= the_player.speed
				the_player.should_move("up",True)
			elif event.key == 274:
				# the_player.y += the_player.speed
				the_player.should_move("down",True)
			if event.key == 275:
				# the_player.x += the_player.speed
				the_player.should_move("right",True)
			elif event.key == 276:
				# the_player.x -= the_player.speed
				the_player.should_move("left",True)
			elif event.key == 32:
				# 32 = SPACE BAR... FIRE!!!!
				new_bullet = Bullet(screen, the_player, 2)
				bullets.add(new_bullet)
				fire = pygame.mixer.Sound("laser.aiff")
				fire.play(0) # Play sound once
				fire.set_volume(.3)



		elif event.type == pygame.KEYUP:
			if event.key == 273:
				the_player.should_move("up",False)
			elif event.key == 274:
				the_player.should_move("down",False)
			if event.key == 275:
				the_player.should_move("right",False)
			elif event.key == 276:
				the_player.should_move("left",False)


	# paint the screen
	# screen.fill(background_color)

	# Place the background image
	screen.blit(background_image, [0,0])

	# Display text at top of page:
	if pygame.font:
		font = pygame.font.Font(None, 25) 
		text1 = font.render("Help Harley save Earth from an alien invasion!", 2, (255,255,255)) # RGB
		text2= font.render("KEYS | Arrows to move, & Space Bar to fire.", 2, (255,255,255)) # RGB
		text3= font.render("Catch the star for extra Health!", 2, (255,255,255)) # RGB

		screen.blit(text1, [280, 30])
		screen.blit(text2, [290, 60])
		screen.blit(text3, [350, 90])
 

	# Make alien chase Harley
	for bad_guy in bad_guys:
		# update the bad guy (based on where the player is)
		bad_guy.update_me(the_player)
		# draw the bad guy
		bad_guy.draw_me()

	# # Must be after fill, or we won't be able to see the hero
	# screen.blit(the_player.image, [the_player.x,the_player.y])
	# the_player.draw_me()

	for bullet in bullets:
		# up date the bullet location
		bullet.update()
		# draw the bullet on the screen
		bullet.draw_bullet()

	for player in players:
		player.draw_me()

	for star in stars:
		star.draw_me()
		

	# ----- CHECK FOR COLLISSONS -----

	# Harley shoots alien
	bullet_hit = groupcollide(bullets,bad_guys,True,True) # Bad guy vanishes after collission with bullet
	if(bullet_hit):
		points += 1# Add another alien after one is killed:
	if len(bad_guys) == 0:
		bad_guys.add(Bad_guy(screen))

	# Alien collides with Harley
	player_hit = groupcollide(players,bad_guys,False, True) # Bad guy sticks around after collision
	if (player_hit):
		bump = pygame.mixer.Sound("bump.aiff")
		bump.play(0) # Play sound once
		bump.set_volume(1)
		player.health -= 2
		print "Harley has %d health points!" % (player.health)
		

	if (player.health < 0):
	 	print "You've lost the game! Try fighting aliens another day!"
	 	# time.sleep(3)
		game_on = False # Close the game

	# Gain 5 health points from star
	power_up = groupcollide(players, stars, False, True) # Player remains after collision
	if (power_up):
		recharge = pygame.mixer.Sound("recharge.wav")
		recharge.play(0) # Play sound once
		recharge.set_volume(1)
		player.health += 3
		print "Harley has %d health points!" % (player.health)


	# Add another star after one disappears
	if len(stars) == 0:
		stars.add(Star(screen))

	# Display health counter:
	text1 = font2.render("HEALTH:  " + str(player.health), True, font_color)
	screen.blit(text1, [770, 50])

	# Display aliens killed counter
	text = font2.render("ALIENS KILLED:  " + str(points), True, font_color)
	screen.blit(text, [770, 80])


	# flip the screen, i.e.clear it so we can draw again... and again... and again
	pygame.display.flip()

