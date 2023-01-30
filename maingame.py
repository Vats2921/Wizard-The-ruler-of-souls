import pygame
import random
from pygame import mixer
import pygame

#import exp

pygame.init()


mixer.init()
mixer.music.load(r'background music.mp3')
mixer.music.play()


clock = pygame.time.Clock()
fps = 120


#GAME WINDOW

bottom_panel = 185
screen_width = 1000
screen_height = 420 + bottom_panel
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Wizard:Ruler Of Souls')


#pygame variables

current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0

#define fonts

font = pygame.font.SysFont('Times New Roman', 26)


#define colours

red = (255, 0, 0)
green = (0, 255, 0)


#LOAD IMAGES


#background image

background_img = pygame.image.load('img/Background/background.jpg').convert_alpha()

#panel image

panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()

#button images

potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()

#load victory and defeat images

victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()

#wand image

wand_img = pygame.image.load('img/Icons/wand.png').convert_alpha()



#create function for drawing text

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))



#function for drawing background
	
def draw_bg():
	screen.blit(background_img, (0, 0))



#function for drawing panel
	
def draw_panel():
        
	#draw panel rectangle
        
	screen.blit(panel_img, (0, screen_height - bottom_panel))
	
	#show wizard stats
	
	draw_text(f'{Wizard.name} HP: {Wizard.hp}', font, red, 150, screen_height - bottom_panel + 30)
	for count, i in enumerate(enemy_list):
                
		#show name and health
                
		draw_text(f'{i.name} HP: {i.hp}', font, red, 650, (screen_height - bottom_panel + 10) + count * 60)

#button
		
#button class
		
class Button():
        def __init__(self, surface, x, y, image, size_x, size_y):
            self.image = pygame.transform.scale(image, (size_x, size_y))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False
            self.surface = surface

        def draw(self):
            action = False

            #get mouse position
            
            pos = pygame.mouse.get_pos()

            #check mouseover and clicked conditions
            
            if self.rect.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                            action = True
                            self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

            #draw button
                    
            self.surface.blit(self.image, (self.rect.x, self.rect.y))

            return action


#fighter class
        
class Fighter():
	def __init__(self, x, y, name, max_hp, strength, potions):
                
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.start_potions = potions
		self.potions = potions
		self.alive = True
		self.animation_list = [] #Animation
		self.frame_index = 0
		self.action = 0#0:idle, 1:attack, 2:hurt, 3:dead
		self.update_time = pygame.time.get_ticks()
		
		#load idle images
		
		temp_list = []
		for i in range(8): #range =0,1,2,3,4,5,6,7
			img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		
		#load attack images
		
		temp_list = []
		for i in range(8): #range =0,1,2,3,4,5,6,7
			img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		
		#load hurt images
		
		temp_list = []
		for i in range(3):#range= 0,1,2
			img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		
		#load death images
		
		temp_list = []
		for i in range(8):#range = 0,1,2,3,4,5,6,7
			img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, 210)


	def update(self):
		animation_cooldown = 100
		
		#handle animation
		
		#update image
		
		self.image = self.animation_list[self.action][self.frame_index]
		
		#check if enough time has passed since the last update
		
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
			
		#if the animation has run out then reset back to the start
			
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.idle()
	
	def idle(self):
                
		#set variables to idle animation
                
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def attack(self, target):
                
		#deal damage to enenmy
                
		rand = random.randint(-5, 5)
		damage = self.strength + rand
		target.hp -= damage
		
		#run enemy hurt animation
		
		target.hurt()
		
		#check if target has died
		
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()

	    #damage text
			
		damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
		damage_text_group.add(damage_text)
		
		#set variables to attack animation
		
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()


	def hurt(self):
                
		#set variables to hurt animation
                
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def death(self):
                
		#set variables to death animation
                
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def reset (self):
		self.alive = True
		self.potions = self.start_potions
		self.hp = self.max_hp
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()


	def draw(self):
		screen.blit(self.image, self.rect)

class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp

	def draw(self, hp):
                
		#update with new health
                
		self.hp = hp
		
		#calculate health ratio
		
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))



#class damage to show how much damage the character has taken

class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0


	def update(self):
                
		#move damage text up
                
		self.rect.y -= 1
		
		#delete the text after a few seconds
		
		self.counter += 1
		if self.counter > 30:
			self.kill()


#spirite group
			
damage_text_group = pygame.sprite.Group()


#hero

Wizard = Fighter(300, 360, 'Wizard', 80, 20, 3)


#bandit

enemy1 = Fighter(500, 270, 'Enemy', 60, 6, 1)
enemy2 = Fighter(600, 270, 'Enemy', 60, 6, 1)

enemy_list = []
enemy_list.append(enemy1)
enemy_list.append(enemy2)

Wizard_health_bar = HealthBar(150, screen_height - bottom_panel + 60, Wizard.hp, Wizard.max_hp)
enemy1_health_bar = HealthBar(650, screen_height - bottom_panel + 40, enemy1.hp, enemy1.max_hp)
enemy2_health_bar = HealthBar(650, screen_height - bottom_panel + 100, enemy2.hp, enemy2.max_hp)



#create buttons

potion_button = Button(screen, 50, screen_height - bottom_panel + 60, potion_img, 64, 64)
restart_button = Button(screen, 430, 120, restart_img, 120, 30)


run = True
while run:

	clock.tick(fps)

	#draw background
	
	draw_bg()

	#draw panel
	
	draw_panel()
	Wizard_health_bar.draw(Wizard.hp)
	enemy1_health_bar.draw(enemy1.hp)
	enemy2_health_bar.draw(enemy2.hp)

	#draw fighters
	
	Wizard.update()
	Wizard.draw()
	for enemy in enemy_list:
		enemy.update()
		enemy.draw()

	#draw the damage text
		
	damage_text_group.update()
	damage_text_group.draw(screen)

	#control player actions
	
	#reset action variables
	
	attack = False
	potion = False
	target = None
	
	#make sure mouse is visible
	
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	for count, enemy in enumerate(enemy_list):
		if enemy.rect.collidepoint(pos):
                        
			#hide mouse
                        
			pygame.mouse.set_visible(False)
			
			#show wand in place of mouse cursor
			
			screen.blit(wand_img, pos)
			if clicked == True and enemy.alive == True:
				attack = True
				target = enemy_list[count]
	if potion_button.draw():
		potion = True
		
	#show number of potions remaining
		
	draw_text(str(Wizard.potions), font, red, 105, screen_height - bottom_panel + 60)





	if game_over == 0:
                
		#player action
                
		if Wizard.alive == True:
			if current_fighter == 1:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
                                        
					#look for player action
                                        
					#attack
                                        
					if attack == True and target != None:
						Wizard.attack(target)
						current_fighter += 1
						action_cooldown = 0


                                        #potion
						
					if potion == True:
						if Wizard.potions > 0:
                                                        
							#check if the potion would heal the player beyond max health
                                                        
							if Wizard.max_hp - Wizard.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = Wizard.max_hp - Wizard.hp
							Wizard.hp += heal_amount
							Wizard.potions -= 1
							damage_text = DamageText(Wizard.rect.centerx, Wizard.rect.y, str(heal_amount), green)
							damage_text_group.add(damage_text)
							current_fighter += 1
							action_cooldown = 0

		else:
			mixer.music.load(r'defeat music.mp3')
			mixer.music.play()
			game_over = -1


		#enemy action
			
		for count, enemy in enumerate(enemy_list):
			if current_fighter == 2 + count:
				if enemy.alive == True:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:
                                                
						#check if enemy needs to heal first
                                                
						if (enemy.hp / enemy.max_hp) < 0.5 and enemy.potions > 0:
                                                        
							#check if the potion would heal the enemy beyond max health
                                                        
							if enemy.max_hp - enemy.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = enemy.max_hp - enemy.hp
							enemy.hp += heal_amount
							enemy.potions -= 1
							damage_text = DamageText(enemy.rect.centerx, enemy.rect.y, str(heal_amount), green)
							damage_text_group.add(damage_text)
							current_fighter += 1
							action_cooldown = 0
							
						#attack
							
						else:
							enemy.attack(Wizard)
							current_fighter += 1
							action_cooldown = 0
				else:
					current_fighter += 1


		#if all fighters have had a turn then reset
					
		if current_fighter > total_fighters:
			current_fighter = 1




	#check if all enemies are dead
			
	alive_enemies = 0
	for enemy in enemy_list:
		if enemy.alive == True:
			alive_enemies += 1
	if alive_enemies == 0:
		game_over = 1


	#check if game is over
		
	if game_over != 0:
		if game_over == 1:
			screen.blit(victory_img, (350, 50))
		if game_over == -1:
			screen.blit(defeat_img, (350, 50))
		if restart_button.draw():
			Wizard.reset()
			for enemy in enemy_list:
				mixer.music.load(r'background music.mp3')
				mixer.music.play()
				enemy.reset()
			current_fighter = 1
			action_cooldown
			game_over = 0




	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True

		else:
			clicked = False


	pygame.display.update()

pygame.quit()


					

