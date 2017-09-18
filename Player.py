import pygame
from pygame.sprite import Sprite

class Player(Sprite):
	# Classes always contain 2 parts:
	# 1. the __init__ section where you define all attributes. 
	# Init, only runs once. When the object is instantiated
	# Because this is a subclass, we need to call the parent's (Sprite) __init__
	def __init__(self,image,start_x,start_y,screen):
		super(Player,self).__init__()
		self.image = pygame.image.load(image)
		self.image = pygame.transform.scale(self.image,(200,200))
		self.x = start_x
		self.y = start_y
		self.speed = 10
		self.health = 15
		self.screen = screen
		self.should_move_up = False
		self.should_move_down = False
		self.should_move_left = False
		self.should_move_right = False
		self.rect = self.image.get_rect()

	# 2. The methods where you define all the class functions (methods)

	def draw_me(self):
		if(self.should_move_up):
			self.y -= self.speed
		elif(self.should_move_down):
			self.y += self.speed
		if(self.should_move_left):
			self.x -= self.speed
		elif(self.should_move_right):
			self.x += self.speed
		self.screen.blit(self.image, [self.x,self.y])
		self.rect.left = self.x # Update the rectangle that pygame thinks of as the player
		self.rect.top = self.y

	def should_move(self,direction,yes_or_no):
		if(direction == "up"):
			# the up key is down. update self.
			self.should_move_up = yes_or_no
		if(direction == "down"):
			# the up key is down. update self.
			self.should_move_down = yes_or_no
		if(direction == "left"):
			# the up key is down. update self.
			self.should_move_left = yes_or_no
		if(direction == "right"):
			# the up key is down. update self.
			self.should_move_right = yes_or_no


